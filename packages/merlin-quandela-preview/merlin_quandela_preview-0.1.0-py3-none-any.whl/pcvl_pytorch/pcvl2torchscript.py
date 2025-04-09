"""
This module provides functionality to convert Perceval quantum circuits to PyTorch tensors
with fixed parameter mapping for TorchScript compatibility.
"""

import numbers
from typing import List, Dict, Tuple, Union, Optional

import perceval as pcvl
import sympy as sp
import torch
import torch.fx as fx
import torch.nn as nn


def _get_complex_dtype_for_float(dtype):
    """Helper function to get the corresponding complex dtype for a float dtype."""
    if dtype == torch.float16 and hasattr(torch, 'complex32'):
        return torch.complex32
    elif dtype == torch.float:
        return torch.complex64
    elif dtype == torch.float64:
        return torch.cdouble
    else:
        raise ValueError(f"Unsupported dtype: {dtype}. Must be torch.float16, torch.float, or torch.float64")


def _get_float_dtype_for_complex(dtype):
    """Helper function to get the corresponding float dtype for a complex dtype."""
    if dtype == torch.complex32:
        return torch.float16
    elif dtype == torch.cfloat:
        return torch.float
    elif dtype == torch.cdouble:
        return torch.float64
    else:
        raise ValueError(f"Unsupported complex dtype: {dtype}. Must be torch.complex32, torch.cfloat, or torch.cdouble")


# Define helper functions outside
def _get_tensor_at_index(x: List[torch.Tensor], idx: int):
    """Extract a tensor at a specific index from a list of tensors"""
    return x[idx]

def _get_batch_size(tensor):
    """Get the batch size (first dimension) of a tensor"""
    return tensor.shape[0]

def _get_device(tensor):
    """Get the device of a tensor"""
    return tensor.device

def _create_eye_matrix(batch_size: int, circuit_size: int, dtype: Optional[torch.dtype], device: Optional[torch.device] = None):
    """Create an identity matrix with batch dimension"""
    return torch.eye(
        circuit_size,
        dtype=dtype,
        device=device
    ).unsqueeze(0).expand(batch_size, -1, -1)

def _extract_parameter(tensor, idx: int):
    """Extract a parameter at a specific index from a batched tensor"""
    return tensor[:, idx]

def _unsqueeze_dim1(x):
    """Add a dimension at position 1"""
    return x.unsqueeze(1)

def _shape_0(x):
    """Get the shape of the first dimension of a tensor"""
    return x.shape[0]

def _device(x):
    """Get the device of a tensor"""
    return x.device

def _torch_full_float(batch_size: int, value: float, dtype: torch.dtype, device: torch.device):
    """Create a float tensor filled with a specific value"""
    return torch.full((batch_size,), value, dtype=dtype, device=device)

def _torch_full_complex(batch_size: int, value: complex, dtype: torch.dtype, device: torch.device):
    """Create a complex tensor filled with a specific value"""
    return torch.full((batch_size,), value, dtype=dtype, device=device)


 # Mapping function for converting sympy expressions to torch operations
def sympy2torch_node(graph, sympy_obj, input_tensors, param_mapping, batch_size_node, device_node,
                     complex_dtype, float_dtype):
    """
    Create a subgraph that evaluates a sympy expression using torch operations.

    Args:
        graph: FX graph to add nodes to
        sympy_obj: Sympy expression to convert
        input_tensors: List of input tensor nodes
        param_mapping: Dictionary mapping parameter names to (tensor_idx, param_idx)
        batch_size_node: Node representing batch size
        device_node: Node representing device

    Returns:
        FX node representing the converted expression
    """
    # Handle Perceval's matrix type
    if isinstance(sympy_obj, pcvl.utils.matrix.Matrix):
        rows = []
        for i in range(sympy_obj.shape[0]):
            row_elements = []
            for j in range(sympy_obj.shape[1]):
                element_node = sympy2torch_node(
                    graph, sympy_obj[i, j], input_tensors, param_mapping,
                    batch_size_node, device_node, complex_dtype, float_dtype
                )
                row_elements.append(element_node)

            # Stack elements horizontally to form a row
            if len(row_elements) > 1:
                row_node = graph.call_function(
                    torch.stack,
                    (tuple(row_elements),),
                    {"dim": 1}
                )
            else:
                row_node = graph.call_function(
                    _unsqueeze_dim1,
                    (row_elements[0],)
                )
            rows.append(row_node)

        # Stack rows vertically to form the matrix
        if len(rows) > 1:
            matrix_node = graph.call_function(
                torch.stack,
                (tuple(rows),),
                {"dim": 1}
            )
        else:
            matrix_node = graph.call_function(
                _unsqueeze_dim1,
                (rows[0],)
            )

        return matrix_node

    # Handle symbolic parameters
    elif isinstance(sympy_obj, sp.Symbol):
        param_name = sympy_obj.name

        if param_name in param_mapping:
            tensor_idx, param_idx = param_mapping[param_name]

            # Extract parameter value from the appropriate input tensor
            return graph.call_function(
                _extract_parameter,
                (input_tensors[tensor_idx], param_idx)
            )
        else:
            raise ValueError(f"Parameter '{param_name}' not found in mapping")

    # Handle numerical values
    elif isinstance(sympy_obj, sp.Number) or isinstance(sympy_obj, numbers.Number):
        value = complex(sympy_obj)

        # Create a tensor with the constant value
        if value.imag == 0:
            # Real value
            return graph.call_function(
                _torch_full_float,
                (batch_size_node, value.real, float_dtype, device_node)
            )
        else:
            # Complex value
            return graph.call_function(
                _torch_full_complex,
                (batch_size_node, value, complex_dtype, device_node)
            )

    # Handle operations by recursively processing arguments
    else:
        # Use imported SYMPY_TO_TORCH_OPS from pcvl2torch module
        from pcvl_pytorch import SYMPY_TO_TORCH_OPS

        if sympy_obj.func not in SYMPY_TO_TORCH_OPS:
            raise ValueError(f"Unsupported Sympy function: {sympy_obj.func}")

        # Process arguments recursively
        arg_nodes = []
        for arg in sympy_obj.args:
            arg_node = sympy2torch_node(
                graph, arg, input_tensors, param_mapping,
                batch_size_node, device_node, complex_dtype, float_dtype
            )
            arg_nodes.append(arg_node)
        num_args = len(arg_nodes)

        # Apply the operation
        op_func = SYMPY_TO_TORCH_OPS[sympy_obj.func]
        # PytorchScript does not handle variable arguments for reduce function
        if sympy_obj.func == sp.Mul or sympy_obj.func == sp.Add:
            op_func =  sympy_obj.func == sp.Mul and torch.mul or torch.add
            # Special handling for Mul and Add to support multiple arguments
            result_node = arg_nodes[0]
            for i in range(1, num_args):
                result_node = graph.call_function(op_func, (result_node, arg_nodes[i]))
        elif sympy_obj.func == sp.core.numbers.ImaginaryUnit:
            result_node = graph.call_function(
                _torch_full_complex,
                (batch_size_node, 1j, complex_dtype, device_node)
            )
        else:
            result_node = graph.call_function(op_func, tuple(arg_nodes))

        return result_node

def embed_operator_into_unitary(full_unitary, operator, indices: List[int]):
    """Embeds a k×k operator into an n×n unitary at specified indices"""
    result = full_unitary.clone()
    n = full_unitary.shape[1]

    # First, create index mapping tensors for the embedding
    idx_helper = torch.arange(n)
    mask = torch.ones(n, dtype=torch.bool)

    # Mark positions where we'll insert the operator
    for idx in indices:
        mask[idx] = False

    # For each operator element, update the corresponding full unitary element
    for i, row_idx in enumerate(indices):
        for j, col_idx in enumerate(indices):
            result[:, row_idx, col_idx] = operator[:, i, j]

    # For operator-identity cross terms, zero out the corresponding elements
    for i, row_idx in enumerate(indices):
        # Zero out the rest of the row
        idx_mask = torch.ones(n, dtype=torch.bool)
        for col_idx in indices:
            idx_mask[col_idx] = False
        result[:, row_idx, idx_mask] = 0

    for j, col_idx in enumerate(indices):
        # Zero out the rest of the column
        idx_mask = torch.ones(n, dtype=torch.bool)
        for row_idx in indices:
            idx_mask[row_idx] = False
        result[:, idx_mask, col_idx] = 0

    return result

def optimized_circuit_compilation(circuit, graph, input_tensors, param_mapping,
                                  batch_size_node, complex_dtype, float_dtype, device_node, input_specs, spec_mappings):
    """
    Optimized circuit compiler that flattens the circuit and batches non-overlapping operations.

    This implementation properly handles both constraints:
    1. Operations in a batch don't overlap with each other
    2. Operations in a batch don't operate on modes affected by excluded operations

    Args:
        circuit: The photonic circuit to compile
        graph: The computation graph
        input_tensors: List of input tensor nodes
        param_mapping: Mapping of parameters
        batch_size_node: Node representing batch size
        complex_dtype: Data type for tensors
        device_node: Node representing device
        input_specs: List of input specifications
        spec_mappings: Mapping of component names to specs

    Returns:
        Node representing the compiled unitary
    """

    # Start with identity matrix
    circuit_size = circuit.m

    # Flatten the circuit and collect all operations
    flattened_ops = []

    def flatten_circuit(rec_circuit, parent_indices=None):
        for idx, (r, c) in enumerate(rec_circuit._components):
            # Map indices if we're in a sub-circuit
            actual_indices = r if parent_indices is None else [parent_indices[i] for i in r]

            if hasattr(c, 'name') and c.name in spec_mappings:
                # For named sub-circuits that match an input spec
                spec_idx = input_specs.index(c.name)
                cU_torch_node = input_tensors[spec_idx]
                flattened_ops.append((actual_indices, cU_torch_node))
            elif hasattr(c, "_components"):
                # For embedded sub-circuits, flatten recursively
                flatten_circuit(c, actual_indices)
            else:
                # Get component's unitary in symbolic form and convert to computation graph
                try:
                    sympy_unitary = c.compute_unitary(use_symbolic=True)
                    cU_torch_node = sympy2torch_node(
                        graph, sympy_unitary, input_tensors, param_mapping,
                        batch_size_node, device_node, complex_dtype, float_dtype
                    )
                    flattened_ops.append((actual_indices, cU_torch_node))
                except Exception as e:
                    # Fallback to identity if symbolic computation fails
                    component_size = len(actual_indices)
                    print(
                        f"Warning: Failed to compute symbolic unitary for component {getattr(c, 'name', 'unnamed')}: {e}")
                    # Skip adding identity operations as they don't change the result

    # Flatten the circuit
    flatten_circuit(circuit)

    # Track which modes have been modified by operations
    # Group operations considering both non-overlap and sequential dependency constraints
    batched_ops = []

    while flattened_ops:
        current_batch = []
        current_batch_indices = set()  # Indices affected by current batch
        exclusion_indices = set()  # Modes that can't be used in this batch

        # Go through all remaining operations - not super efficient, but it is only done in compilation
        i = 0
        while i < len(flattened_ops):
            op_indices = set(flattened_ops[i][0])

            # Check if this operation can be included in the current batch:
            # 1. No overlap with current batch operations
            # 2. No operation on modes that from excluded operations
            if (not op_indices.intersection(current_batch_indices) and
                    not op_indices.intersection(exclusion_indices)):
                # Can add to current batch
                current_batch.append(flattened_ops.pop(i))
                current_batch_indices.update(op_indices)
            else:
                # Can't add to current batch
                exclusion_indices.update(op_indices)
                i += 1

        batched_ops.append(current_batch)

    u_node = graph.call_function(
        _create_eye_matrix,
        (batch_size_node, circuit_size, complex_dtype, device_node)
    )

    # Apply each batch of operations
    for batch in batched_ops:
        # Create a single combined unitary (start with identity)
        combined_unitary = graph.call_function(
            _create_eye_matrix,
            (batch_size_node, circuit_size, complex_dtype, device_node)
        )

        # Insert each operation's unitary into the combined unitary
        for indices, op_unitary in batch:
            # Embed this operator into the combined unitary
            combined_unitary = graph.call_function(
                embed_operator_into_unitary,
                (combined_unitary, op_unitary, indices)
            )

        # Apply the combined unitary to U in a single matrix multiplication
        u_node = graph.call_function(
            torch.matmul,
            (combined_unitary, u_node)
        )

    return u_node


# Python-side function to build FX graph
def _build_circuit_to_unitary_fx(circuit, input_specs, device=None, dtype=torch.float):
    """
    Builds an FX module for circuit unitary computation.

    Args:
        circuit: Perceval Circuit object
        input_specs: List of parameter specs (names/prefixes)
        device: PyTorch device
        dtype: PyTorch float dtype

    Returns:
        fx_module: FX GraphModule for computation
        param_info: Dict with parameter mapping information
    """

    # Convert float dtype to complex dtype
    complex_dtype = _get_complex_dtype_for_float(dtype)

    # Determine the corresponding float dtype (this should match input dtype)
    float_dtype = dtype

    # Get circuit parameters and map to input specs
    circuit_params = circuit.get_parameters()
    param_names = [p.name for p in circuit_params]

    # Create parameter mapping
    param_mapping = {}
    spec_mappings = {}  # Track parameters for each spec

    # First identify sub-circuits
    sub_circuits = {}
    for _, comp in circuit._components:
        if hasattr(comp, 'name') and comp.name and hasattr(comp, '_components'):
            sub_circuits[comp.name] = comp

    # Now create the mappings for parameters
    for i, spec in enumerate(input_specs):
        # Skip if this is a known sub-circuit name
        if spec in sub_circuits:
            spec_mappings[spec] = []  # Empty list for sub-circuits
            continue

        # Find parameters that match this spec
        matching_params = [p for p in param_names if p.startswith(spec)]
        spec_mappings[spec] = matching_params

        for j, param in enumerate(matching_params):
            param_mapping[param] = (i, j)

    # Check if all parameters are covered
    for param in param_names:
        if param not in param_mapping:
            raise ValueError(f"Parameter '{param}' not covered by any input spec")

    # Update param_info with sub-circuit info
    param_info = {
        "circuit_size": circuit.m,
        "num_inputs": len(input_specs),
        "params": param_mapping,
        "input_specs": input_specs,
        "spec_mappings": spec_mappings,
        "sub_circuits": sub_circuits,
        "dtype": dtype
    }
    # Create FX graph
    graph = fx.Graph()

    # Add placeholder for inputs (as a list)
    inputs_node = graph.placeholder("inputs", type_expr=List[torch.Tensor])

    # Extract individual input tensors
    input_tensors = []
    for i in range(len(input_specs)):
        input_tensors.append(
            graph.call_function(_get_tensor_at_index, (inputs_node, i))
        )

    # Get batch size from first input
    batch_size_node = graph.call_function(
        _shape_0,
        (input_tensors[0],)
    )

    # Get device from first input
    device_node = graph.call_function(
        _device,
        (input_tensors[0],)
    )

    # Call the recursive compilation function with the top-level circuit
    u_node = optimized_circuit_compilation(
        circuit, graph, input_tensors, param_mapping,
        batch_size_node, complex_dtype, float_dtype, device_node, input_specs, spec_mappings
    )

    # Register output
    graph.output(u_node)

    # Create module
    fx_module = fx.GraphModule(nn.Module(), graph)

    return fx_module, param_info


import json
import os


def _create_circuit_function(scripted_module, input_specs, param_info=None):
    """
    Create a circuit function that wraps a TorchScript module.

    This function is used internally by both compile_circuit_to_unitary and
    load_circuit_unitary to create a consistent interface.

    Args:
        scripted_module: The TorchScript module that computes the unitary
        input_specs: List of parameter specifications
        param_info: Optional dictionary with parameter mapping information

    Returns:
        A function that computes the circuit unitary when called with parameters
    """

    def get_input_specs():
        """
        Returns detailed information about expected input tensor specifications.

        Returns:
            List of dictionaries, each containing:
            - 'spec': The input specification name
            - 'parameters': List of parameter names matching this spec
            - 'expected_dim': Expected tensor dimensions
            - 'expected_size': Expected tensor size for each dimension
        """
        if not param_info:
            return []

        # Retrieve spec mappings and sub-circuits from param_info
        spec_mappings = param_info.get('spec_mappings', {})
        sub_circuits = param_info.get('sub_circuits', {})

        input_details = []
        for spec in input_specs:
            detail = {
                'spec': spec,
                'parameters': [],
                'expected_dim': None,
                'expected_size': []
            }

            # Check if this is a sub-circuit
            if spec in sub_circuits:
                sub_circuit = sub_circuits[spec]
                detail.update({
                    'parameters': [],
                    'expected_dim': 3,  # Batch of matrices
                    'expected_size': [None, sub_circuit.m, sub_circuit.m]  # [batch_size, matrix_rows, matrix_cols]
                })
            elif spec in spec_mappings:
                # Regular parameter group
                matching_params = spec_mappings[spec]

                if matching_params:
                    detail.update({
                        'parameters': matching_params,
                        'expected_dim': 2,  # Batched parameters
                        'expected_size': [None, len(matching_params)]  # [batch_size, num_parameters]
                    })
                else:
                    # Spec with no parameters
                    detail.update({
                        'parameters': [],
                        'expected_dim': 1,  # Single tensor
                        'expected_size': [1]  # Placeholder
                    })

            input_details.append(detail)

        return input_details

    def circuit_function(*args, device=None):
        """
        Compute the unitary matrix for the circuit.

        Args:
            *args: Either:
                - A list of input tensors, one for each input_spec
                - Individual tensors, one for each input_spec
            device: Optional device to place tensors on

        Returns:
            Unitary matrix for the circuit
        """
        # Check arguments
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]

        # Ensure we have the correct number of inputs
        if len(args) != len(input_specs):
            raise ValueError(f"Expected {len(input_specs)} inputs, got {len(args)}")

        # Process each input tensor
        inputs = []
        batch_dimensions = []

        for i, arg in enumerate(args):
            if not isinstance(arg, torch.Tensor):
                raise TypeError(f"Input {i} must be a tensor, got {type(arg)}")

            # Get the expected shape for this input
            spec = input_specs[i]

            # Check if this is a sub-circuit
            if param_info and spec in param_info.get("sub_circuits", {}):
                # This is a sub-circuit unitary
                sub_circuit = param_info["sub_circuits"][spec]
                sub_circuit_size = sub_circuit.m

                # Check dimensions for sub-circuit unitary
                if arg.dim() == 2:
                    # Non-batched square matrix
                    if arg.shape[0] != sub_circuit_size or arg.shape[1] != sub_circuit_size:
                        raise ValueError(
                            f"Input {i} ({spec}) should be a {sub_circuit_size}x{sub_circuit_size} matrix, "
                            f"got shape {arg.shape}"
                        )
                    arg = arg.unsqueeze(0)  # Add batch dimension
                    batch_dimensions.append(False)
                elif arg.dim() >= 3:
                    # Batched matrix
                    if arg.shape[1] != sub_circuit_size or arg.shape[2] != sub_circuit_size:
                        raise ValueError(
                            f"Input {i} ({spec}) should be a batch of {sub_circuit_size}x{sub_circuit_size} matrices, "
                            f"got shape {arg.shape}"
                        )
                    batch_dimensions.append(True)
                else:
                    raise ValueError(
                        f"Input {i} ({spec}) should be a matrix or batch of matrices, got dim={arg.dim()}"
                    )
            elif param_info and spec in param_info.get("spec_mappings", {}):
                # Regular parameter group
                expected_params = param_info["spec_mappings"][spec]
                expected_dim = len(expected_params)

                # Check dimensions
                if expected_dim == 0:
                    # This spec doesn't match any parameters (should be rare)
                    print(f"Warning: Spec '{spec}' matches no parameters")
                    if arg.dim() == 0:
                        arg = arg.unsqueeze(0).unsqueeze(0)
                        batch_dimensions.append(False)
                    elif arg.dim() == 1:
                        arg = arg.unsqueeze(0)
                        batch_dimensions.append(False)
                    else:
                        batch_dimensions.append(True)
                elif arg.dim() == 0:
                    # Scalar input (only valid if expecting 1 parameter)
                    if expected_dim != 1:
                        raise ValueError(f"Input {i} ({spec}) should have {expected_dim} parameters, got scalar")
                    arg = arg.unsqueeze(0).unsqueeze(0)  # Add batch and param dimensions
                    batch_dimensions.append(False)
                elif arg.dim() == 1:
                    # Vector input (must match expected_dim)
                    if arg.shape[0] != expected_dim:
                        raise ValueError(
                            f"Input {i} ({spec}) should have {expected_dim} parameters, got {arg.shape[0]}")
                    arg = arg.unsqueeze(0)  # Add batch dimension
                    batch_dimensions.append(False)
                else:  # arg.dim() >= 2
                    # Batched input (second dimension must match expected_dim)
                    if arg.shape[1] != expected_dim:
                        raise ValueError(
                            f"Input {i} ({spec}) should have {expected_dim} parameters, got {arg.shape[1]}")
                    batch_dimensions.append(True)
            else:
                # Unknown spec or missing param_info - do basic checks
                if arg.dim() == 0:
                    arg = arg.unsqueeze(0).unsqueeze(0)
                    batch_dimensions.append(False)
                elif arg.dim() == 1:
                    arg = arg.unsqueeze(0)
                    batch_dimensions.append(False)
                else:
                    batch_dimensions.append(True)

            inputs.append(arg)

        # Fail if some inputs are batched and others aren't
        if len(set(batch_dimensions)) > 1:
            batched_inputs = [i for i, is_batched in enumerate(batch_dimensions) if is_batched]
            unbatched_inputs = [i for i, is_batched in enumerate(batch_dimensions) if not is_batched]
            raise ValueError(
                f"Inconsistent batching: inputs {batched_inputs} are batched, but inputs {unbatched_inputs} are not. "
                f"Either batch all inputs or none of them."
            )

        # Get consistent batching state
        input_was_batched = any(batch_dimensions)

        # Check that all batched inputs have the same batch size
        batch_sizes = [inp.shape[0] for inp in inputs]
        if len(set(batch_sizes)) > 1:
            raise ValueError(f"All inputs must have the same batch size, got {batch_sizes}")

        # Move to specified device if needed
        if device is not None:
            inputs = [inp.to(device=device) for inp in inputs]

        # Run the module
        result = scripted_module(inputs)

        # Remove batch dimension if input wasn't batched
        if not input_was_batched and result.dim() > 2:
            result = result.squeeze(0)

        return result

    # Add attributes to the function
    circuit_function._scripted_module = scripted_module
    circuit_function._param_info = param_info
    circuit_function._input_specs = input_specs
    circuit_function.get_input_specs = get_input_specs

    # Add save method
    def save(path):
        """
        Save the circuit function to a file.

        Args:
            path: Path to save the model to
        """
        # Create directory if it doesn't exist
        dir_path = os.path.dirname(path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Save TorchScript module
        scripted_module.save(f"{path}")

        # Save param_info and input_specs as JSON
        # Filter out any non-serializable objects from param_info
        if param_info:
            serializable_info = {}
            for key, value in param_info.items():
                # Skip any torch tensors or modules
                if isinstance(value, (torch.Tensor, torch.nn.Module)):
                    continue
                # Handle some common nested structures
                if key == "spec_mappings":
                    serializable_info[key] = {k: v for k, v in value.items()}
                elif key == "params":
                    serializable_info[key] = {k: list(v) for k, v in value.items()}
                elif isinstance(value, (dict, list, str, int, float, bool, type(None))):
                    serializable_info[key] = value

            with open(f"{path}.info", "w") as f:
                json.dump({
                    "param_info": serializable_info,
                    "input_specs": input_specs
                }, f)

    circuit_function.save = save

    return circuit_function


def load_circuit_unitary_computegraph(path):
    """
    Load a previously saved circuit unitary model.

    Args:
        path: Path to the saved TorchScript module

    Returns:
        A function that computes the circuit unitary when called with parameters

    Example:
        >>> # Save a compiled circuit
        >>> circuit_function, param_info = build_circuit_unitary_computegraph(circuit, input_specs)
        >>> circuit_function.save("circuit_unitary.pt")
        >>>
        >>> # Later, load the saved circuit
        >>> loaded_function = load_circuit_unitary_computegraph("circuit_unitary.pt")
        >>>
        >>> # Use the loaded function
        >>> params = torch.tensor([0.1, 0.2])
        >>> unitary = loaded_function(params)
    """
    # Load the TorchScript module
    try:
        scripted_module = torch.jit.load(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load TorchScript module from {path}: {e}")

    # Try to load param_info and input_specs
    param_info = None
    input_specs = None

    info_path = f"{path}.info"
    if os.path.exists(info_path):
        try:
            with open(info_path, "r") as f:
                info_data = json.load(f)
                param_info = info_data.get("param_info")
                input_specs = info_data.get("input_specs")
        except Exception as e:
            print(f"Warning: Failed to load parameter info from {info_path}: {e}")
            print("Proceeding with limited functionality.")

    # If we couldn't load input_specs, try to infer from the module
    if input_specs is None:
        # For TorchScript modules, we can try to get the number of expected inputs
        # But we can't get their names, so we'll use generic names
        try:
            # This is a bit of a hack - we create a dummy input and see where it fails
            dummy_input = [torch.zeros(1, 1) for _ in range(10)]  # Try with 10 inputs
            for i in range(1, 11):
                try:
                    scripted_module(dummy_input[:i])
                    input_specs = [f"input_{j}" for j in range(i)]
                    break
                except Exception:
                    continue
        except Exception:
            # If all fails, assume a single input
            input_specs = ["input_0"]
            print(f"Warning: Could not determine input structure, assuming {len(input_specs)} inputs")

    # Create and return the circuit function
    return _create_circuit_function(scripted_module, input_specs, param_info)


def build_circuit_unitary_computegraph(circuit, input_specs, dtype=torch.float):
    """
    Compiles a quantum circuit to an optimized function for computing unitaries.

    This function takes a quantum circuit and creates a TorchScript-optimized function
    that can compute its unitary matrix given input parameters. The function is optimized
    for inference and can be saved and loaded for deployment.

    Args:
        circuit: Perceval Circuit object to convert
        input_specs: List of parameter specifications, where each spec is either:
                    - A prefix that matches one or more circuit parameters
                    - A full parameter name
                    - A sub-circuit name
        dtype: PyTorch float data type

    Returns:
        Tuple of (circuit_function, param_info):
            - circuit_function: A function that takes parameters and returns a unitary matrix
            - param_info: Dictionary with parameter mapping information

    Notes:
        - The returned function handles input preprocessing (batching if needed)
        - The function also handles output postprocessing (removing batch dimension if input wasn't batched)
        - Under the hood, it uses a TorchScript module when possible for performance

    Example:
        >>> circuit = pcvl.Circuit(2)
        >>> circuit.add(0, pcvl.BS())
        >>> circuit.add(0, pcvl.PS(pcvl.P("phi1")))
        >>> circuit.add(0, pcvl.BS())
        >>> circuit.add(0, pcvl.PS(pcvl.P("phi2")))
        >>>
        >>> input_specs = ["phi"]
        >>> circuit_function, param_info = build_circuit_unitary_computegraph(circuit, input_specs)
        >>>
        >>> # Use as a function
        >>> phi_params = torch.tensor([0.1, 0.2])
        >>> unitary = circuit_function(phi_params)
        >>>
        >>> # Save for deployment
        >>> circuit_function.save("circuit_unitary.pt")
    """
    # Validate dtype
    if dtype not in [torch.float, torch.float64, torch.float16]:
        raise ValueError(f"Unsupported dtype: {dtype}. Must be torch.float, torch.float64, or torch.float16")
    # Get corresponding complex dtype for unitaries
    complex_dtype = _get_complex_dtype_for_float(dtype)

    # Build FX module and get param info
    fx_module, param_info = _build_circuit_to_unitary_fx(circuit, input_specs, dtype=dtype)

    # Store both dtypes in param_info
    param_info["dtype"] = dtype
    param_info["complex_dtype"] = complex_dtype

    # Create the TorchScript-compatible module
    class UnitaryModule(nn.Module):
        def __init__(self, fx_module, circuit_size, num_inputs, dtype_str):
            super().__init__()
            self.fx_module = fx_module
            self.circuit_size = circuit_size
            self.num_inputs = num_inputs
            self.dtype_str = dtype_str

        # Explicitly annotate the input type for TorchScript compatibility
        def forward(self, input_list: List[torch.Tensor]) -> torch.Tensor:
            """
            Compute the unitary matrix for the circuit.

            Args:
                input_list: List of input tensors, each with shape [batch_size, ...]

            Returns:
                Unitary matrix with shape [batch_size, circuit_size, circuit_size]
            """
            # Validate input
            if len(input_list) != self.num_inputs:
                raise ValueError(f"Expected {self.num_inputs} input tensors, got {len(input_list)}")

            # Use the FX module directly
            return self.fx_module(input_list)

    # Convert dtype to string for TorchScript compatibility
    dtype_str = "complex64" if dtype == torch.complex64 else "complex128"

    # Create the unified module
    module = UnitaryModule(
        fx_module=fx_module,
        circuit_size=circuit.m,
        num_inputs=len(input_specs),
        dtype_str=dtype_str
    )

    # Try to script the module
    param_info["scripted"] = False

    scripted_module = torch.jit.script(module)

    # Test the module with dummy inputs to verify it works
    example_inputs = []
    for spec in input_specs:
        if spec in param_info.get("sub_circuits", {}):
            # This is a sub-circuit - create a unitary matrix of appropriate size
            sub_circuit = param_info["sub_circuits"][spec]
            sub_circuit_size = sub_circuit.m
            example_inputs.append(torch.eye(sub_circuit_size, dtype=dtype).unsqueeze(0))
        elif spec in param_info["spec_mappings"]:
            # Regular parameter group
            n_params = len(param_info["spec_mappings"][spec])
            if n_params > 0:  # Skip empty parameter lists
                example_inputs.append(torch.zeros(1, n_params, dtype=torch.float32))
            else:
                # Handle the case where a spec matches no parameters
                # This shouldn't happen with your improved parameter mapping
                print(f"Warning: Spec '{spec}' matches no parameters")
                example_inputs.append(torch.zeros(1, 1, dtype=torch.float32))  # Default placeholder
        else:
            # This shouldn't happen
            raise ValueError(f"Unknown input spec: {spec}")

    # Run a test forward pass

    _ = scripted_module(example_inputs)
    param_info["scripted"] = True

    # Create the circuit function
    circuit_function = _create_circuit_function(scripted_module, input_specs, param_info)

    def compute(*args):
        return circuit_function(*args)

    circuit_function.compute = compute

    return circuit_function

# Prepare input tensors for a model
def _prepare_circuit_inputs(circuit, input_specs, param_values, batch_size=1):
    """
    Prepare input tensors for a circuit unitary module.

    Args:
        circuit: Perceval Circuit object
        input_specs: List of parameter specs (names/prefixes)
        param_values: Dict mapping parameter names to values
        batch_size: Batch size for input tensors

    Returns:
        List of input tensors
    """
    circuit_params = circuit.get_parameters()
    param_names = [p.name for p in circuit_params]

    # Create mapping from spec to parameters
    spec_to_params = {}
    for spec in input_specs:
        spec_to_params[spec] = [p for p in param_names if p.startswith(spec)]

    # Create input tensors
    inputs = []
    for spec in input_specs:
        matching_params = spec_to_params[spec]
        values = []

        for param in matching_params:
            if param in param_values:
                values.append(param_values[param])
            else:
                values.append(0.0)  # Default value

        # Create tensor with batch dimension
        tensor = torch.tensor(values, dtype=torch.float32).unsqueeze(0)

        # Expand to batch size if needed
        if batch_size > 1:
            tensor = tensor.expand(batch_size, -1)

        inputs.append(tensor)

    return inputs


def compute_circuit_unitary(
        circuit: pcvl.Circuit,
        circuit_parameters: Union[torch.Tensor, Dict[str, torch.Tensor]],
        device=None,
        dtype=torch.float
):
    """
    Converts a parameterized Perceval circuit to a PyTorch unitary matrix.

    This is a reimplementation of the legacy function using the new TorchScript-compatible approach.
    Supports batch processing if torch_parameters is a 2D tensor or contains 2D tensors.

    Args:
        circuit: Perceval Circuit object
        circuit_parameters: Either a PyTorch tensor with parameter values, or
                          a dictionary mapping parameter names to tensor values
        device: PyTorch device (optional)
        dtype: PyTorch float dtype

    Returns:
        PyTorch tensor representing the circuit's unitary (or batch of unitaries)
    """
    # Validate dtype
    if dtype not in [torch.float, torch.float64, torch.float16]:
        raise ValueError(f"Unsupported dtype: {dtype}. Must be torch.float, torch.float64, or torch.float16")

    # Get corresponding complex dtype for unitaries
    complex_dtype = _get_complex_dtype_for_float(dtype)

    if isinstance(circuit_parameters, dict):
        # For dictionary input, create parameter mapping based on exact names
        input_specs = list(circuit_parameters.keys())

        # Detect parameters that aren't provided
        circuit_param_names = [p.name for p in circuit.get_parameters()]
        missing_params = [p for p in circuit_param_names if not any(p.startswith(spec) for spec in input_specs)]

        if missing_params:
            raise ValueError(f"Parameters not covered by input dictionary: {missing_params}")

        # Prepare inputs for the TorchScript module
        inputs = []
        for spec in input_specs:
            # Check if this is a parameter or sub-circuit
            if hasattr(circuit_parameters[spec], 'shape') and len(circuit_parameters[spec].shape) >= 2:
                # This looks like a sub-circuit unitary (matrix)
                if circuit_parameters[spec].dim() == 2:
                    # Add batch dimension for non-batched input
                    inputs.append(circuit_parameters[spec].unsqueeze(0))
                else:
                    inputs.append(circuit_parameters[spec])
            else:
                # This is a parameter or group of parameters
                matching_params = [p for p in circuit_param_names if p.startswith(spec)]
                if not matching_params:
                    # This might be a sub-circuit name with a tensor that's not a matrix
                    inputs.append(circuit_parameters[spec].unsqueeze(0) if circuit_parameters[spec].dim() == 0 else
                                  circuit_parameters[spec])
                else:
                    # For parameters, ensure they're in a batch
                    tensor = circuit_parameters[spec]
                    if tensor.dim() == 0:
                        # Scalar to batch of size 1 with 1 parameter
                        inputs.append(tensor.unsqueeze(0).unsqueeze(0))
                    elif tensor.dim() == 1:
                        # Vector to batch of size 1
                        inputs.append(tensor.unsqueeze(0))
                    else:
                        # Already batched
                        inputs.append(tensor)
    else:
        # For tensor input, use parameter names as input specs
        circuit_params = circuit.get_parameters()
        param_names = [p.name for p in circuit_params]

        # Group parameters by prefix (this is a simple approach - adjust as needed)
        param_prefixes = set()
        for name in param_names:
            prefix = name.split('_')[0] if '_' in name else name
            param_prefixes.add(prefix)

        input_specs = sorted(list(param_prefixes))

        # Convert tensor to batched form if needed
        if circuit_parameters.dim() == 1:
            # Add batch dimension for non-batched input
            circuit_parameters = circuit_parameters.unsqueeze(0)

        # Split the tensor into groups based on parameter prefixes
        inputs = []
        current_idx = 0
        for prefix in input_specs:
            matching_params = [i for i, p in enumerate(param_names) if p.startswith(prefix)]
            n_params = len(matching_params)

            if current_idx + n_params > circuit_parameters.shape[1]:
                raise ValueError(
                    f"Not enough values in parameters tensor. Expected at least {current_idx + n_params}, got {circuit_parameters.shape[1]}")

            # Extract the relevant slice of the tensor
            prefix_params = circuit_parameters[:, current_idx:current_idx + n_params]
            inputs.append(prefix_params)
            current_idx += n_params

    # Create scriptable module
    scripted_module = build_circuit_unitary_computegraph(
        circuit,
        input_specs,
        dtype=dtype
    )

    # Move inputs to specified device if needed and ensure they have the correct dtype
    if device is not None or inputs[0].dtype != dtype:
        inputs = [inp.to(device=device, dtype=dtype) for inp in inputs]

    # Use the module to compute the unitary (scripted or non-scripted)
    try:
        # For TorchScript modules
        unitary = scripted_module(inputs)
    except Exception as e:
        # In case we got a fallback Python module
        print(f"Warning: Using fallback module: {e}")
        unitary = scripted_module.forward(inputs)

    # For backward compatibility, if input wasn't batched, remove batch dimension
    if (isinstance(circuit_parameters, torch.Tensor) and circuit_parameters.dim() == 1) or \
            (isinstance(circuit_parameters, dict) and all(tensor.dim() <= 1 for tensor in circuit_parameters.values())):
        unitary = unitary.squeeze(0)

    return unitary


# Example usage
if __name__ == "__main__":
    dtype = torch.float

    # Create a simple circuit
    circuit = pcvl.Circuit(2)
    circuit.add(0, pcvl.BS())
    circuit.add(0, pcvl.PS(pcvl.P("theta_1")))
    circuit.add(1, pcvl.PS(pcvl.P("phi_1")))
    circuit.add(0, pcvl.BS())

    # Define input specs
    input_specs = ["theta", "phi"]

    # Create scriptable module
    scripted_module = build_circuit_unitary_computegraph(circuit, input_specs, dtype=dtype)
    param_info = scripted_module._param_info

    # Print parameter mapping info
    print("Parameter mapping:")
    for param, (tensor_idx, param_idx) in param_info["params"].items():
        spec = input_specs[tensor_idx]
        print(f"  {param} -> input[{tensor_idx}][{param_idx}] (spec: {spec})")

    # Print dtype info
    print(f"Parameter dtype: {param_info['dtype']}")
    print(f"Unitary dtype: {param_info['complex_dtype']}")

    # Prepare input tensors
    param_values = {"theta_1": 0.1, "phi_1": 0.2}
    inputs = _prepare_circuit_inputs(circuit, input_specs, param_values)

    # Use the scripted module
    unitary = scripted_module(inputs)
    print(f"Unitary shape: {unitary.shape}")

    # Save scripted module
    #try:
    if True:
        scripted_module.save("circuit_unitary.pt")
        print("Saved scripted module to circuit_unitary.pt")

        # Load and use the saved module
        loaded_module = torch.jit.load("circuit_unitary.pt")
        unitary_loaded = loaded_module(inputs)
        print(f"Loaded module unitary shape: {unitary_loaded.shape}")
    else:
        #except AttributeError:
        print("Module is not scripted, cannot save directly.")
        print("To save, explicitly use torch.jit.script() first.")