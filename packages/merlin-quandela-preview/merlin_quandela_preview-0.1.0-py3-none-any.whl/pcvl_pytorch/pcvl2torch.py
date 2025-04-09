"""
This module provides functionality to convert Perceval quantum circuits to PyTorch tensors
for differentiable quantum computing.

Author: Jean Senellart

The symbolic function mapping logic is inspired by SympyTorch: https://github.com/patrick-kidger/sympytorch
    Copyright 2021 Patrick Kidger
    Licensed under the Apache License, Version 2.0 (function mapping section)
"""

import functools as ft
import numbers
from typing import Any, Callable, TypeVar, Union, Dict

import perceval as pcvl
import sympy as sp
import torch
import torch.fx as fx

# Type variable for generic function typing
T = TypeVar("T")


# Helper function to reduce multiple arguments using a binary function
def _reduce(fn: Callable[..., T]) -> Callable[..., T]:
    """
    Creates a reduction function that applies a binary operation repeatedly.
    Useful for converting n-ary Sympy operations to binary PyTorch operations.
    """

    def fn_(*args: Any) -> T:
        return ft.reduce(fn, args)

    return fn_


# Helper function to create imaginary unit tensor
def _imaginary_fnc(*_: Any) -> torch.Tensor:
    """Returns the imaginary unit as a PyTorch tensor"""
    return torch.tensor(1j)


# Mapping between Sympy operations and their PyTorch equivalents
SYMPY_TO_TORCH_OPS = {
    # Basic arithmetic
    sp.Mul: _reduce(torch.mul),
    sp.Add: _reduce(torch.add),
    sp.div: torch.div,
    sp.Pow: torch.pow,

    # Basic mathematical functions
    sp.Abs: torch.abs,
    sp.sign: torch.sign,
    sp.ceiling: torch.ceil,
    sp.floor: torch.floor,
    sp.log: torch.log,
    sp.exp: torch.exp,
    sp.sqrt: torch.sqrt,

    # Trigonometric functions
    sp.cos: torch.cos,
    sp.sin: torch.sin,
    sp.tan: torch.tan,
    sp.acos: torch.acos,
    sp.asin: torch.asin,
    sp.atan: torch.atan,
    sp.atan2: torch.atan2,

    # Hyperbolic functions
    sp.cosh: torch.cosh,
    sp.sinh: torch.sinh,
    sp.tanh: torch.tanh,
    sp.acosh: torch.acosh,
    sp.asinh: torch.asinh,
    sp.atanh: torch.atanh,

    # Complex operations
    sp.re: torch.real,
    sp.im: torch.imag,
    sp.arg: torch.angle,
    sp.core.numbers.ImaginaryUnit: _imaginary_fnc,
    sp.conjugate: torch.conj,

    # Special functions
    sp.erf: torch.erf,
    sp.loggamma: torch.lgamma,

    # Comparison operations
    sp.Eq: torch.eq,
    sp.Ne: torch.ne,
    sp.StrictGreaterThan: torch.gt,
    sp.StrictLessThan: torch.lt,
    sp.LessThan: torch.le,
    sp.GreaterThan: torch.ge,

    # Logical operations
    sp.And: torch.logical_and,
    sp.Or: torch.logical_or,
    sp.Not: torch.logical_not,

    # Min/Max operations
    sp.Max: torch.max,
    sp.Min: torch.min,

    # Matrix operations
    sp.MatAdd: torch.add,
    sp.HadamardProduct: torch.mul,
    sp.Trace: torch.trace,
    sp.Determinant: torch.det,
}


def sympy2torch(sympy_object, map_params, batch_size, dtype=torch.complex64):
    """
    Converts recursively a Sympy expression to a PyTorch tensor, expect a batch of parameters mapped in map_params.

    Args:
        sympy_object: A Sympy expression, matrix, or number
        map_params: Dictionary mapping parameter names to their PyTorch values
        batch_size: Number of samples in the batch
        dtype: PyTorch complex data type (torch.complex64 or torch.complex128)

    Returns:
        torch.Tensor: The PyTorch equivalent of the input
    """
    # Check that dtype is a complex dtype
    if dtype not in [torch.complex64, torch.complex128]:
        raise ValueError(f"Unsupported dtype: {dtype}. Must be torch.complex64 or torch.complex128")

    # Determine the corresponding float dtype for the complex dtype
    if dtype == torch.complex64:
        float_dtype = torch.float32
    else:  # dtype == torch.complex128
        float_dtype = torch.float64

    # Handle Perceval's matrix type
    if isinstance(sympy_object, pcvl.utils.matrix.Matrix):
        t_object = torch.empty((batch_size, *sympy_object.shape), dtype=dtype)
        for i in range(sympy_object.shape[0]):
            for j in range(sympy_object.shape[1]):
                t_object[:, i, j] = sympy2torch(sympy_object[i, j], map_params, batch_size, dtype)

    # Handle symbolic parameters: return the corresponding tensor from map_params
    elif isinstance(sympy_object, sp.Symbol):
        t_object = map_params[sympy_object.name]
        # Ensure the tensor is of the correct dtype
        if t_object.is_complex():
            t_object = t_object.to(dtype)
        else:
            t_object = t_object.to(float_dtype)

    # Handle numerical values
    elif isinstance(sympy_object, sp.Number) or isinstance(sympy_object, numbers.Number):
        if (isinstance(sympy_object, sp.Number) and sympy_object.is_real) or not isinstance(sympy_object, complex):
            t_object = torch.full((batch_size,), float(sympy_object), dtype=float_dtype)
        else:
            t_object = torch.full((batch_size,), complex(sympy_object), dtype=dtype)

    # Handle operations (functions, operators) with a recursive call on the arguments
    else:
        t_object = SYMPY_TO_TORCH_OPS[sympy_object.func](
            *[sympy2torch(arg, map_params, batch_size=1, dtype=dtype) for arg in sympy_object.args]
        )
        if t_object.dim() == 0:
            t_object = t_object.unsqueeze(0).repeat(batch_size)

        # Ensure correct dtype
        if t_object.is_complex():
            t_object = t_object.to(dtype)
        elif t_object.is_floating_point():
            t_object = t_object.to(float_dtype)

    return t_object


def pcvl_circuit_to_pytorch_unitary_legacy(circuit: pcvl.Circuit,
                                         circuit_parameters: Union[torch.Tensor, Dict[str, torch.Tensor]],
                                         dtype=torch.complex64):
    """
    Converts a parameterized Perceval circuit to a PyTorch unitary matrix.
    Supports batch processing if torch_parameters is a 2D tensor.

    Args:
        circuit: Perceval Circuit object
        circuit_parameters: either PyTorch parameters for the circuit. Can be a 2D tensor for batch processing.
                          or map name->tensor (again can be a 2D tensor)
        dtype: PyTorch complex data type (torch.complex64 or torch.complex128)

    Returns:
        tuple: (parameters, unitary_matrix)
            - parameters: PyTorch parameters of the circuit (or batch of parameters)
            - unitary_matrix: PyTorch tensor representing the circuit's unitary (or batch of unitaries)

    Raises:
        ValueError: If dtype is not torch.complex64 or torch.complex128
    """
    # Validate dtype
    if dtype not in [torch.complex64, torch.complex128]:
        raise ValueError(f"Unsupported dtype: {dtype}. Must be torch.complex64 or torch.complex128")

    # Determine the corresponding float dtype for the complex dtype
    float_dtype = torch.float32 if dtype == torch.complex64 else torch.float64

    if isinstance(circuit_parameters, torch.Tensor):
        torch_parameters = circuit_parameters
        if torch_parameters.dim() > 2:
            raise ValueError("torch_parameters must be a 1D or 2D tensor")

        # Get circuit parameters
        circuit_params = circuit.get_parameters()

        # Check if we have the correct number of parameters
        if torch_parameters.dim() == 0:
            if len(circuit_params) != 0:
                raise ValueError(f"Circuit requires {len(circuit_params)} parameters, but torch_parameters has none")
        elif torch_parameters.shape[-1] != len(circuit_params):
            raise ValueError(f"Circuit requires {len(circuit_params)} parameters, but torch_parameters has {torch_parameters.shape[-1]}")

        # Initialize parameters if not provided
        is_batch = False
        if torch_parameters.dim() == 1:
            torch_parameters = torch_parameters.unsqueeze(0)  # Ensure it's a 2D tensor
        else:
            is_batch = True

        batch_size = torch_parameters.size(0)

        # Create parameter mapping and ensure correct dtype
        map_params = {p.name: torch_parameters[:, idx].to(dtype=float_dtype)
                      for idx, p in enumerate(circuit_params)}
    elif isinstance(circuit_parameters, dict):
        is_batch = False
        batch_size = 1
        map_params = {}
        for name, tensor in circuit_parameters.items():
            # Convert to the appropriate dtype
            if tensor.is_complex():
                map_params[name] = tensor.to(dtype=dtype)
            else:
                map_params[name] = tensor.to(dtype=float_dtype)

            if tensor.dim() == 1:
                is_batch = True
                batch_size = tensor.shape[0]
    else:
        raise AttributeError("torch_parameters must be a map or a PyTorch tensor")

    # Build unitary matrix by composing component unitaries
    u = None
    for r, c in circuit._components:
        # TODO: we should handle recursively the case where c is a circuit, otherwise sympy unitary will be too complex

        if c.name in map_params:
            cU_torch = map_params[c.name].unsqueeze(0) if len(map_params[c.name].shape) == 2 else map_params[c.name]
        else:
            # Get component's unitary in symbolic form
            cU = c.compute_unitary(use_symbolic=True)
            # Convert to PyTorch, returns a batch of torch unitaries
            cU_torch = sympy2torch(cU, map_params, batch_size=batch_size, dtype=dtype)

        # Handle components that don't span all modes
        if len(r) != circuit.m:
            nU = torch.eye(circuit.m, dtype=dtype).unsqueeze(0).repeat(batch_size, 1, 1)
            nU[:, r[0]:(r[-1] + 1), r[0]:(r[-1] + 1)] = cU_torch
            cU_torch = nU

        # Compose unitaries
        if u is None:
            u = cU_torch
        else:
            u = cU_torch @ u

    if not is_batch:
        u = u.squeeze(0)

    return u


if __name__ == '__main__':

    c_bs = pcvl.Circuit(2)//pcvl.BS()//pcvl.PS(pcvl.P("x"))//(1, pcvl.PS(pcvl.P("y")))
    bs_fx = build_circuit_to_unitary_fx(c_bs)
    print(">>>>>>", bs_fx.code)
    params = {"x": torch.tensor(0.1, requires_grad=True), "y": torch.tensor(0.2, requires_grad=True)}
    print("Unitary matrix:", bs_fx(params))
    print("Unitary matrix legacy:", pcvl_circuit_to_pytorch_unitary_legacy(c_bs, params))

    # Test with different dtypes
    print("\nTesting with different dtypes:")
    for dtype in [torch.complex64, torch.complex128]:
        print(f"\nUsing {dtype}:")
        bs_fx_typed = build_circuit_to_unitary_fx(c_bs, dtype=dtype)
        unitary = bs_fx_typed(params, dtype=dtype)
        print(f"Unitary dtype: {unitary.dtype}")
        print(f"Unitary shape: {unitary.shape}")

    # Create a simple quantum circuit: Mach-Zehnder interferometer
    circuit = pcvl.Circuit(2)
    circuit.add(0, pcvl.BS())  # First beam splitter
    circuit.add(0, pcvl.PS(pcvl.P("phi1")))  # Phase shifter with parameter phi1
    circuit.add(0, pcvl.BS())  # Second beam splitter
    circuit.add(0, pcvl.PS(pcvl.P("phi2")))  # Phase shifter with parameter phi2
    Unitary = pcvl.Circuit(2, name="U1")
    print(Unitary.name)
    circuit.add(0, Unitary)
    pcvl.pdisplay(circuit, recursive=True)

    # Convert to PyTorch
    params = torch.tensor([0.1, 0.2], dtype=torch.float32, requires_grad=True)
    unitary = pcvl_circuit_to_pytorch_unitary_legacy(circuit, params)
    unitary_fx = build_circuit_to_unitary_fx(circuit)
    print(unitary_fx.code)
    unitary_bis = unitary_fx(params)

    print("Circuit parameters:", params)
    print("\nUnitary matrix:")
    print(unitary)
    print("\nUnitary matrix bis:")
    print(unitary_bis)

    # Test differentiability
    try:
        loss = torch.abs(unitary_bis[0, 0]) ** 2
        loss.backward()
        print("\nGradients exist:", params.grad is not None)
        print("Gradients:", params.grad)
    except Exception as e:
        print("\nError testing differentiability:", e)

    # Check speed of fx module
    import timeit

    circuit = pcvl.GenericInterferometer(16,
                                        lambda i: pcvl.BS() // pcvl.PS(pcvl.P(f"theta_ri{i}")) // \
                                                  pcvl.BS() // pcvl.PS(pcvl.P(f"theta_ro{i}")),
                                        shape=pcvl.InterferometerShape.RECTANGLE)
    n_params = len(circuit.get_parameters())
    fx_module = build_circuit_to_unitary_fx(circuit)

    for batch_size in [1, 8, 32]:
        params = torch.randn((batch_size, n_params), requires_grad=True)
        print(f"\nBatch size: {batch_size}")
        print("Time FX:", timeit.timeit(lambda: fx_module(params), number=100))
        print("Time Legacy:", timeit.timeit(lambda: pcvl_circuit_to_pytorch_unitary_legacy(circuit, params), number=100))