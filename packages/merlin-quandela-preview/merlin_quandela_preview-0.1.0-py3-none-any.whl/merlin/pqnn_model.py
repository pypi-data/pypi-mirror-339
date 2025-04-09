import warnings
from enum import Enum
from typing import List, Optional, Callable, Tuple, Dict

import perceval as pcvl
import torch
import torch.nn.functional as F
from torch import nn

from pcvl_pytorch import (
    build_circuit_unitary_computegraph,
    build_slos_distribution_computegraph
)


class OutputMappingStrategy(Enum):
    LINEAR = 'linear'
    GROUPING = 'grouping'
    NONE = 'none'


class QuantumLayer(nn.Module):
    """

    Quantum Neural Network Layer implemented using photonic circuits.

    The layer consists of a parameterized quantum photonic circuit where:
    - Some circuit parameters (in Perceval terminology) are trainable parameters (theta)
    - Others are inputs (x) fed during the forward pass
    - The output is a probability distribution over possible photonic states

    Parameter Ranges:
    - Input parameters (x) should be in range [0, 1]. These values are internally scaled
      by 2π when setting phase shifters to utilize their full range.
    - Trainable parameters (theta) are initialized in range [0, π] and will adapt during training
      to optimize the circuit's behavior.

    The output mapping strategy determines how the quantum probability distribution
    is mapped to the final output:
    - 'linear': Applies a trainable linear layer
    - 'grouping': Groups distribution values into equal-sized buckets
    - 'none': No mapping (requires matching sizes between probability distribution and output)

    Args:
        input_size (int): Number of input variables for the circuit
        output_size (int): Dimension of the final layer output
        circuit (pcvl.Circuit): Perceval quantum circuit to be used - this circuit can be changed dynamically but the
            size and parameters shall remain identical
        input_state (List[int]): Initial photonic state configuration - the input state can be changed dynamically but
            the number of photons shall remain identical
        trainable_parameters (List[str]], optional): list of parameter name pattern to make trainable.
            Parameters are initialized in [0, π].
        input_parameters (List[str], optional): List of input parameter name patterns.
            These parameters are fed during the forward
        output_map_func (Callable, optional): Function to map output states
        output_mapping_strategy (OutputMappingStrategy): Strategy for mapping quantum output
        device (torch.device, optional): Device to run computations on
        dtype (torch.dtype, optional): Numerical precision for computations

    Raises:
        ValueError: If input state size doesn't match circuit modes
        ValueError: If output_mapping_strategy is 'none' and distribution size != output_size

    Note:
        Input parameters (x) shall be normalized to [0, 1] range. The layer internally scales
        these values by 2π when applying them to phase shifters. This ensures full coverage
        of the phase shifter range while maintaining a normalized input interface.

    Example:
        >>> layer = QuantumLayer(
        ...     input_size=4,
        ...     output_size=4,
        ...     circuit=pcvl.Circuit(2)//pcvl.BS()//pcvl.PS(pcvl.P('theta1'))//pcvl.BS()//pcvl.PS(pcvl.P('x1'))//pcvl.BS(),
        ...     input_state=[1, 1, 1],
        ...     trainable_parameters=["theta", "phi"],
        ...     input_parameters=["x"],
        ...     output_mapping_strategy=OutputMappingStrategy.LINEAR
        ... )
        >>> x = torch.tensor([0.5])  # Input in [0, 1] range, will be scaled by 2π
     """

    @staticmethod
    def get_output_size(circuit: pcvl.Circuit,
                              input_state: List[int],
                              output_map_func: Optional[Callable] = None,
                              no_bunching: bool = False) -> int:
        """
        Calculate the expected output distribution size for a given circuit and input state.

        This helper method allows users to determine the correct output_size when using
        OutputMappingStrategy.NONE, which requires the output_size to match exactly the
        size of the quantum circuit's output distribution.

        Args:
            circuit (pcvl.Circuit): The quantum circuit
            input_state (List[int]): The input state configuration
            output_map_func (Callable, optional): Function to map output states
            no_bunching (bool, optional): Whether to use no-bunching simulation

        Returns:
            int: The size of the output distribution

        Example:
            >>> circuit = pcvl.Circuit(4)
            >>> circuit.add(0, pcvl.BS()//pcvl.PS(pcvl.P("theta1"))//pcvl.BS(), merge=True)
            >>> input_state = [1, 0, 1, 0]
            >>> output_size = QuantumLayer.get_distribution_size(circuit, input_state)
            >>> print(f"Required output_size for NONE strategy: {output_size}")
            >>> # Now create the layer with the correct size
            >>> layer = QuantumLayer(
            ...     input_size=1,
            ...     output_size=output_size,  # Use the calculated size
            ...     circuit=circuit,
            ...     input_state=input_state,
            ...     trainable_parameters=["theta1"],
            ...     input_parameters=["x1"],
            ...     output_mapping_strategy=OutputMappingStrategy.NONE
            ... )
        """
        # Create temporary computation graphs to calculate the distribution size
        # Use default dtype for quick calculation
        temp_unitary_graph = build_circuit_unitary_computegraph(circuit, [""], dtype=torch.float32)

        # Determine appropriate real dtype
        real_dtype = torch.float32

        temp_simulation_graph = build_slos_distribution_computegraph(
            input_state,
            output_map_func=output_map_func,
            no_bunching=no_bunching,
            dtype=real_dtype
        )

        # Generate a dummy unitary and compute distribution
        n_parameters = temp_unitary_graph._param_info
        dummy_unitary = temp_unitary_graph(torch.zeros((len(n_parameters["spec_mappings"]['']),)))
        _, distribution = temp_simulation_graph.compute(dummy_unitary)

        return distribution.shape[-1]

    def __init__(self,
                 input_size: int,
                 circuit: pcvl.Circuit,
                 input_state: List[int],
                 output_size: Optional[int] = None,
                 trainable_parameters: List[str] = [],
                 input_parameters: List[str] = [],
                 no_bunching: bool = False,
                 output_map_func: Callable[[Tuple[int, ...]], Optional[Tuple[int, ...]]] = None,
                 output_mapping_strategy: OutputMappingStrategy = OutputMappingStrategy.NONE,
                 device: Optional[torch.device] = None,
                 dtype: Optional[torch.dtype] = None,
                 shots: int = 0,
                 sampling_method: str = 'multinomial'):
        super().__init__()

        # Store circuit
        self.circuit = circuit
        self.device = device
        # Determine appropriate complex dtype based on input dtype
        if dtype is None or dtype == torch.complex64:
            self.dtype = torch.float32
        elif dtype == torch.complex128:
            self.dtype = torch.float64
        elif dtype == torch.complex32:
            self.dtype = torch.float16
        else:
            self.dtype = torch.float32  # Default to complex64

        self.output_map_func = output_map_func
        self.no_bunching = no_bunching

        self.circuit_parameters = self.circuit.get_parameters()
        self.n_circuit_parameters = len(self.circuit_parameters)
        self.circuit_parameter_names = [p.name for p in self.circuit_parameters]

        # Validate input state
        self.input_state = input_state
        if len(self.input_state) != self.circuit.m:
            raise ValueError(
                "Input state size must match number of modes in the circuit"
            )

        # Setup trainable parameters and inputs
        self.input_size = input_size
        self.output_mapping_strategy = output_mapping_strategy

        self.unitary_graph = build_circuit_unitary_computegraph(self.circuit, trainable_parameters+input_parameters,
                                                            dtype=self.dtype)

        param_info = self.unitary_graph._param_info
        self.thetas = []
        self.theta_names = []
        self.n_thetas = 0
        for tp in trainable_parameters:
            theta_list = param_info["spec_mappings"][tp]
            self.n_thetas += len(theta_list)
            self.theta_names += theta_list
            parameter = nn.Parameter(torch.randn((len(theta_list),), device=device) * torch.pi)
            self.register_parameter(tp, parameter)
            self.thetas.append(parameter)

        self.x_names = []
        self.x_dim = []
        self.n_xs = 0
        self.input_parameters = input_parameters
        for xp in input_parameters:
            x_list = param_info["spec_mappings"][xp]
            self.x_names += x_list
            self.x_dim += [len(x_list)]
            self.n_xs += len(x_list)

        if self.n_xs != input_size:
            raise ValueError(
                f"Number of circuit inputs ({self.n_xs}) "
                f"must match input_size ({input_size})"
            )

        # Build computation graph for output distribution calculation
        # Convert complex dtype to corresponding real dtype
        if self.dtype == torch.complex64:
            real_dtype = torch.float32
        elif self.dtype == torch.complex128:
            real_dtype = torch.float64
        else:
            real_dtype = torch.float32

        self.simulation_graph = build_slos_distribution_computegraph(
            self.input_state,
            output_map_func=output_map_func,
            no_bunching=no_bunching,
            device=device,
            dtype=real_dtype
        )

        # Initialize output mapping
        # First, create dummy input tensors
        dummy_xs = [torch.zeros((si,)) for si in self.x_dim]

        unitary = self.unitary_graph(*(self.thetas+dummy_xs))
        _, distribution = self.simulation_graph.compute(unitary)

        # Get the calculated distribution size
        calculated_output_size = distribution.shape[-1]

        # Handle output_size based on strategy
        if output_size is None:
            if output_mapping_strategy == OutputMappingStrategy.NONE:
                # Only auto-set for NONE strategy
                self.output_size = calculated_output_size
                print(f"Auto-setting output_size to {calculated_output_size} for NONE strategy")
            else:
                # For LINEAR and GROUPING, output_size must be specified
                raise ValueError(
                    f"output_size must be specified when using {output_mapping_strategy.value} strategy. "
                    f"This parameter defines the dimension of the layer's output."
                )
        else:
            # User provided a specific output_size
            self.output_size = output_size

            # Validate for NONE strategy
            if output_mapping_strategy == OutputMappingStrategy.NONE and output_size != calculated_output_size:
                raise ValueError(
                    f"For OutputMappingStrategy.NONE, output_size must match the distribution size ({calculated_output_size}). "
                    f"Use QuantumLayer.get_output_size(circuit, input_state) to calculate the correct size."
                )

        # Setup output mapping based on strategy
        self.setup_output_mapping(distribution)

        # Add sampling parameters
        self.shots = None
        self.sampling_method = None
        self.set_sampling_config(shots=shots, method=sampling_method)

    def describe_inputs(self) -> List[Dict[str, any]]:
        """
        Provides a description of the expected inputs for this quantum layer.

        Returns:
            List[Dict[str, any]]: A list of dictionaries containing information about each expected input:
                - name: The parameter name or pattern
                - dimension: The dimension of this input
                - index: The position in the input list
                - matching_params: Circuit parameters that match this input
        """
        input_descriptions = []

        for i, (pattern, dim) in enumerate(zip(self.input_parameters, self.x_dim)):
            matching_params = self.unitary_graph._param_info["spec_mappings"][pattern] if hasattr(self,
                                                                                                  "unitary_graph") else []
            input_descriptions.append({
                "name": pattern,
                "dimension": dim,
                "index": i,
                "matching_params": matching_params
            })

        return input_descriptions

    def extra_repr(self) -> str:
        """
        Return a string with the extra representation of the module.

        This method follows PyTorch's standard way of extending module representation.
        It includes detailed information about the quantum circuit, its parameters,
        and expected inputs.
        """
        # Get input descriptions
        inputs = self.describe_inputs()

        # Prepare representation strings
        lines = []

        # Basic configuration
        lines.append(f"input_size={self.input_size}, output_size={self.output_size}")
        lines.append(f"input_state={self.input_state}")
        lines.append(f"output_mapping_strategy={self.output_mapping_strategy.value}")

        # Circuit information
        if hasattr(self, 'circuit'):
            lines.append(f"circuit={self.circuit.name if hasattr(self.circuit, 'name') else 'Custom Circuit'}")
            lines.append(f"circuit_modes={self.circuit.m}")

        # Parameter information
        trainable_params = ', '.join(self.theta_names) if hasattr(self, 'theta_names') and self.theta_names else 'None'
        lines.append(f"trainable_parameters={trainable_params}")

        # Input parameters
        if inputs:
            input_details = []
            for info in inputs:
                param_str = f"{info['name']}(dim={info['dimension']})"
                if info['matching_params']:
                    param_str += f" → {', '.join(info['matching_params'])}"
                input_details.append(param_str)

            lines.append(f"input_parameters=[{', '.join(input_details)}]")

        # Device and dtype information
        if hasattr(self, 'device') and self.device is not None:
            lines.append(f"device={self.device}")
        if hasattr(self, 'dtype'):
            lines.append(f"dtype={self.dtype}")

        # Add sampling information
        if self.shots > 0:
            sampling_repr = f"shots={self.shots}, sampling_method='{self.sampling_method}'"
        else:
            sampling_repr = "sampling=disabled (exact distribution)"
        lines.append(sampling_repr)

        return ', '.join(lines)

    def change_input_state(self, new_input_state: List[int]) -> None:
        """
        Change the input state while keeping the same number of modes and photons.

        Args:
            new_input_state (List[int]): New input state configuration

        Raises:
            ValueError: If the new input state doesn't match the number of modes
            ValueError: If the new input state has a different number of photons
        """
        if len(new_input_state) != self.circuit.m:
            raise ValueError("New input state must match the number of modes in the circuit")

        if sum(new_input_state) != sum(self.input_state):
            raise ValueError("New input state must have the same number of photons")

        self.input_state = new_input_state

        # Determine appropriate real dtype based on complex dtype
        if self.dtype == torch.complex64:
            real_dtype = torch.float32
        elif self.dtype == torch.complex128:
            real_dtype = torch.float64
        else:
            real_dtype = torch.float32

        # Rebuild simulation computation graph with the new input state
        self.simulation_graph = build_slos_distribution_computegraph(
            self.input_state,
            output_map_func=self.output_map_func,
            no_bunching=self.no_bunching,
            device=self.device,
            dtype=real_dtype
        )

        # Get a dummy distribution to ensure output mapping is set up correctly
        dummy_xs = [torch.zeros((si,), device=self.device) for si in self.x_dim]
        unitary = self.unitary_graph(*(self.thetas + dummy_xs))
        _, distribution = self.simulation_graph.compute(unitary)

        # Update output mapping if needed
        if distribution.shape[-1] != self.probability_distribution_size:
            self.setup_output_mapping(distribution)

    def apply_sampling(self, distribution: torch.Tensor, shots: Optional[int] = None) -> torch.Tensor:
        """
        Apply sampling noise to a probability distribution.

        Args:
            distribution (torch.Tensor): Exact probability distribution
            shots (Optional[int]): Override default shot count if provided

        Returns:
            torch.Tensor: Probability distribution with sampling noise
        """
        # Use provided shots or fall back to class default
        shot_count = shots if shots is not None else self.shots

        # If shots is 0 or negative, return exact distribution
        if shot_count <= 0:
            return distribution

        method = self.sampling_method

        if method == 'multinomial':
            # Multinomial sampling (direct sampling from distribution)
            if distribution.dim() == 1:
                # Handle single sample case
                sampled_counts = torch.multinomial(
                    distribution,
                    num_samples=shot_count,
                    replacement=True
                )
                noisy_dist = torch.zeros_like(distribution)
                for idx in sampled_counts:
                    noisy_dist[idx] += 1
                return noisy_dist / shot_count

            else:
                # Handle batched case
                batch_size = distribution.shape[0]
                noisy_dists = []

                for i in range(batch_size):
                    sampled_counts = torch.multinomial(
                        distribution[i],
                        num_samples=shot_count,
                        replacement=True
                    )
                    noisy_dist = torch.zeros_like(distribution[i])
                    for idx in sampled_counts:
                        noisy_dist[idx] += 1
                    noisy_dists.append(noisy_dist / shot_count)

                return torch.stack(noisy_dists)

        elif method == 'binomial':
            # Binomial sampling (independent sampling for each outcome)
            return torch.distributions.Binomial(
                shot_count, distribution
            ).sample() / shot_count

        elif method == 'gaussian':
            # Gaussian approximation (valid for large shots)
            std_dev = torch.sqrt(distribution * (1 - distribution) / shot_count)
            noise = torch.randn_like(distribution) * std_dev
            noisy_dist = distribution + noise

            # Ensure valid probabilities (between 0 and 1)
            noisy_dist = torch.clamp(noisy_dist, 0, 1)

            # Renormalize if needed
            noisy_dist = noisy_dist / noisy_dist.sum(dim=-1, keepdim=True)
            return noisy_dist

        else:
            raise ValueError(f"Unknown sampling method: {method}")

    def set_sampling_config(self, shots: Optional[int] = None, method: Optional[str] = None):
        """
        Update the sampling configuration for this layer.

        Args:
            shots (int): Number of measurement shots (0 for exact distribution)
            method (Optional[str]): Sampling method to use
        """
        if shots is not None:
            self.shots = shots
        if method is not None:
            if method not in ['multinomial', 'binomial', 'gaussian']:
                raise ValueError(f"Unknown sampling method: {method}")
            self.sampling_method = method

    def disable_sampling(self):
        """
        Disable sampling and use exact distributions.

        This is a convenience method equivalent to set_sampling_config(shots=0).
        """
        self.set_sampling_config(shots=0)

    def enable_sampling(self, shots=1000, method=None):
        """
        Enable sampling with specified shots and method.

        This is a convenience method to quickly turn on sampling.

        Args:
            shots (int): Number of measurement shots
            method (Optional[str]): Sampling method to use (if None, uses current method)
        """
        self.set_sampling_config(shots=shots, method=method)

    def setup_output_mapping(self, initial_output_distribution):
        """Initialize output mapping based on selected strategy"""
        self.probability_distribution_size = initial_output_distribution.shape[-1]

        if self.output_mapping_strategy == OutputMappingStrategy.LINEAR:
            self.output_mapping = nn.Linear(self.probability_distribution_size, self.output_size)
        elif self.output_mapping_strategy == OutputMappingStrategy.GROUPING:
            self.group_size = self.probability_distribution_size // self.output_size
            self.output_mapping = self.group_probabilities
        elif self.output_mapping_strategy == OutputMappingStrategy.NONE:
            if self.probability_distribution_size != self.output_size:
                raise ValueError(
                    f"Distribution size ({self.probability_distribution_size}) must equal "
                    f"output size ({self.output_size}) when using 'none' strategy"
                )
            self.output_mapping = nn.Identity()
        else:
            raise ValueError(f"Unknown output mapping strategy: {self.output_mapping_strategy}")

    def group_probabilities(self, probability_distribution: torch.Tensor) -> torch.Tensor:
        """Group probability distribution into equal-sized buckets"""
        pad_size = (self.output_size - (self.probability_distribution_size % self.output_size)) % self.output_size

        if pad_size > 0:
            padded = F.pad(probability_distribution, (0, pad_size))
        else:
            padded = probability_distribution

        if probability_distribution.dim() == 2:
            return padded.view(probability_distribution.shape[0], self.output_size, -1).sum(dim=-1)
        else:
            return padded.view(self.output_size, -1).sum(dim=-1)

    def prepare_parameters(self, input_parameters: List[torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Prepare parameter dictionary for circuit evaluation.

        Args:
            x (torch.Tensor): Input tensor [input_size] or [batch_size, input_size]

        Returns:
            Dict[str, torch.Tensor]: Parameter dictionary for circuit evaluation
        """

        # Add input parameters (x) to dict if provided
        if input_parameters is not None and input_parameters[0].dim() != 1:
            # Handle batched inputs - we need to properly prepare parameter dict
            batch_size = input_parameters[0].shape[0]
            params = [theta.expand(batch_size, theta.shape[0]) for theta in self.thetas]
        else:
            params = [theta for theta in self.thetas]

        params += [x * 2 * torch.pi for x in input_parameters]

        return params

    def get_quantum_output(self, *input_parameters: List[torch.Tensor],
                          apply_sampling: bool = True,
                          shots: Optional[int] = None) -> torch.Tensor:
        """
        Process inputs through the quantum circuit with optional sampling.

        Args:
            input_parameters: Input tensors for the quantum circuit
            apply_sampling (bool): Whether to apply sampling noise
            shots (Optional[int]): Override default shot count

        Returns:
            torch.Tensor: Probability distribution (exact or noisy)

        Note:
            During training, when gradients are required (backpropagation), sampling is
            automatically disabled regardless of other settings. This ensures stable
            gradient computation while still allowing realistic noise during forward inference.

            You can check if sampling was applied by comparing the output with:
            `layer(x, apply_sampling=False)` vs `layer(x, apply_sampling=True)`
        """
        # Prepare parameter dictionary
        params = self.prepare_parameters(input_parameters)

        # Compute unitary using computation graph
        unitaries = self.unitary_graph(params)

        # Compute output distribution using simulation graph
        _, distribution = self.simulation_graph.compute(unitaries)

        # Apply sampling if requested and we're not in training mode with requires_grad
        # This ensures we use exact distributions when computing gradients
        needs_gradient = self.training and torch.is_grad_enabled() and any(p.requires_grad for p in self.parameters())

        if shots is None:
            shots = self.shots

        if apply_sampling and not needs_gradient and shots:
            return self.apply_sampling(distribution, shots)

        return distribution

    def forward(self, *input_parameters: List[torch.Tensor],
                apply_sampling: bool = None,
                shots: Optional[int] = None) -> torch.Tensor:
        """
        Forward pass through the quantum layer.

        Args:
            x (torch.Tensor): Input tensor [input_size] or [batch_size, input_size]

        Returns:
            torch.Tensor: Output tensor [output_size] or [batch_size, output_size]
        """
        # Check if gradients are being computed
        needs_gradient = self.training and torch.is_grad_enabled() and any(p.requires_grad for p in self.parameters())

        # If we need gradients, warn if user explicitly requested sampling
        if needs_gradient and (apply_sampling or shots):
            warnings.warn(
                "Sampling was requested (apply_sampling=True/shots) but is disabled because "
                "gradients are being computed. Sampling during gradient computation "
                "would lead to incorrect gradients. Use apply_sampling=False for clarity "
                "or wrap with torch.no_grad() to enable sampling.",
                UserWarning
            )
            apply_sampling = False
            shots = None
        else:
            # Use provided value or default
            apply_sampling = apply_sampling if apply_sampling is not None else (shots or self.shots > 0)
        quantum_output = self.get_quantum_output(*input_parameters,
                                                 apply_sampling=apply_sampling,
                                                 shots=shots)
        return self.output_mapping(quantum_output)

    def __str__(self) -> str:
        """Returns a string representation of the quantum layer architecture."""
        sections = []

        sections.append("Quantum Neural Network Layer:")
        sections.append(f"  Input Size: {self.input_size}")
        sections.append(f"  Output Size: {self.output_size}")

        sections.append("Quantum Circuit Configuration:")
        sections.append(f"  Circuit: {self.circuit.describe()}")
        sections.append(f"  Number of Modes: {self.circuit.m}")
        sections.append(
            f"  Number of Trainable Parameters (theta): {self.n_thetas} - {', '.join(self.theta_names) if self.theta_names else 'None'}")
        sections.append(f"  Number of Inputs (x) Parameters: {self.input_size} - {', '.join(self.x_names)}")
        sections.append(f"  Input State: {self.input_state}")
        sections.append(f"  Device: {self.device}")
        sections.append(f"  Data Type: {self.dtype}")

        sections.append("\nOutput Configuration:")
        sections.append(f"  Distribution Size: {self.probability_distribution_size}")
        sections.append(f"  Output Mapping: {self.output_mapping_strategy.value}")
        if self.output_mapping_strategy == OutputMappingStrategy.GROUPING:
            sections.append(f"  Group Size: {self.group_size}")

        # Add sampling information section
        sections.append("\nSampling Configuration:")
        if self.shots <= 0:
            sections.append(f"  Sampling: Disabled (using exact distribution)")
        else:
            sections.append(f"  Sampling: Enabled")
            sections.append(f"  Shot Count: {self.shots}")
            sections.append(f"  Sampling Method: {self.sampling_method}")
            sections.append(f"  Note: Sampling is automatically disabled during gradient computation")

        return "\n".join(sections)


def estimate_sampling_error(self, distribution=None, shots=None, n_trials=100, method=None):
    """
    Estimate the expected sampling error for a given distribution and shot count.

    This method helps users understand the statistical uncertainty in their quantum measurements
    by simulating multiple sampling trials and calculating the expected deviation.

    Args:
        distribution (torch.Tensor, optional): Probability distribution to sample from.
            If None, a uniform distribution is used.
        shots (int, optional): Number of measurement shots. If None, uses the layer's shots value.
        n_trials (int): Number of sampling trials to run
        method (str, optional): Sampling method to use. If None, uses the layer's method.

    Returns:
        dict: Dictionary containing error statistics:
            - mean_abs_error: Mean absolute error
            - max_abs_error: Maximum absolute error
            - std_error: Standard deviation of error
    """

    # Use provided values or defaults
    shots = shots if shots is not None else self.shots
    method_save = self.sampling_method
    if method is not None:
        self.sampling_method = method

    # If no distribution provided, use uniform
    if distribution is None:
        distribution = torch.ones(self.probability_distribution_size) / self.probability_distribution_size

    # Handle zero shots case
    if shots <= 0:
        self.sampling_method = method_save
        return {
            'mean_abs_error': 0.0,
            'max_abs_error': 0.0,
            'std_error': 0.0,
            'message': 'No sampling error with shots=0 (exact distribution)'
        }

    # Run multiple sampling trials
    errors = []
    for _ in range(n_trials):
        noisy_dist = self.apply_sampling(distribution, shots)
        abs_error = torch.abs(noisy_dist - distribution)
        errors.append(abs_error)

    # Calculate error statistics
    errors_tensor = torch.stack(errors)
    mean_abs_error = errors_tensor.mean().item()
    max_abs_error = errors_tensor.max().item()
    std_error = errors_tensor.std().item()

    # Restore original method
    self.sampling_method = method_save

    return {
        'mean_abs_error': mean_abs_error,
        'max_abs_error': max_abs_error,
        'std_error': std_error,
        'message': f'Statistics from {n_trials} trials with {shots} shots using {self.sampling_method} sampling'
    }


# Example usage:
if __name__ == "__main__":
    # Create a simple circuit
    c = pcvl.Circuit(4)
    c.add(0, pcvl.BS() // pcvl.PS(pcvl.P("theta1")) // pcvl.BS(), merge=True)
    c.add(2, pcvl.BS() // pcvl.PS(pcvl.P("theta2")) // pcvl.BS() // pcvl.PS(pcvl.P("theta3")), merge=True)
    c.add(1, pcvl.BS() // pcvl.PS(pcvl.P("x1")) // pcvl.BS(), merge=True)

    # Create quantum layer
    qlayer = QuantumLayer(
        input_size=1,  # One input (x1)
        output_size=10,
        circuit=c,
        trainable_parameters=["theta1", "theta2", "theta3"],
        input_parameters=["x"],
        input_state=[1, 0, 1, 0],
        output_mapping_strategy=OutputMappingStrategy.LINEAR
    )

    print("--- Model description:")
    print(qlayer)

    print("--- Model parameters:")
    for name, param in qlayer.named_parameters():
        print(f"Parameter {name}: {param.shape}")

    # Test forward pass
    print("\n--- Forward Pass Example:")
    x = torch.tensor([1.0])
    print("qlayer(x)=", qlayer(x))

    # Test forward and backward pass
    x = torch.tensor([[1.0], [2.0], [3.0]])  # Batch of 3 inputs
    y = torch.tensor([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])  # Target outputs

    # Initialize optimizer
    optimizer = torch.optim.Adam(qlayer.parameters(), lr=0.01)

    # Training loop
    print("\n--- Training Example:")
    for epoch in range(5):
        optimizer.zero_grad()

        # Forward pass
        output = qlayer(x)

        # Compute loss
        loss = F.mse_loss(output, y)

        # Backward pass
        loss.backward()

        # Print gradients
        print(f"\nEpoch {epoch + 1}")
        print(f"Loss: {loss.item():.4f}")
        print("Gradients:")
        for name, param in qlayer.named_parameters():
            if param.grad is not None:
                print(f"{name}: {param.grad.norm():.4f}")

        # Update parameters
        optimizer.step()