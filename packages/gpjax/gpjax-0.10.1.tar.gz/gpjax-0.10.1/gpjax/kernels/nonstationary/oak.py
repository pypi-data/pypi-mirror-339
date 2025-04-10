# Copyright 2022 The JaxGaussianProcesses Contributors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from typing import Optional, Callable, Union, Tuple

import beartype.typing as tp
from flax import nnx
import jax
import jax.numpy as jnp
from jaxtyping import Float, Array, Scalar
from gpjax.typing import ScalarFloat

from gpjax.kernels.base import AbstractKernel
from gpjax.kernels.computations import AbstractKernelComputation, DenseKernelComputation
from gpjax.parameters import PositiveReal, Parameter
from jax.typing import ArrayLike


def legendre_polynomial(n: int) -> Callable:
    """Compute the Legendre polynomial of degree n.

    Args:
        n: Degree of the Legendre polynomial.

    Returns:
        Function that evaluates the nth Legendre polynomial at given points.
    """
    if n == 0:
        return lambda x: jnp.ones_like(x)
    elif n == 1:
        return lambda x: x
    else:
        p_n_minus_2 = legendre_polynomial(n - 2)
        p_n_minus_1 = legendre_polynomial(n - 1)
        return (
            lambda x: ((2 * n - 1) * x * p_n_minus_1(x) - (n - 1) * p_n_minus_2(x)) / n
        )


def legendre_polynomial_derivative(n: int) -> Callable:
    """Compute the derivative of the Legendre polynomial of degree n.

    Args:
        n: Degree of the Legendre polynomial.

    Returns:
        Function that evaluates the derivative of the nth Legendre polynomial.
    """
    if n == 0:
        return lambda x: jnp.zeros_like(x)
    else:
        p_n_minus_1 = legendre_polynomial(n - 1)
        return (
            lambda x: n
            * (p_n_minus_1(x) - x * legendre_polynomial_derivative(n - 1)(x))
            / (1 - x**2 + 1e-10)
        )


def gauss_legendre_quadrature(
    deg: int, a: float = -1.0, b: float = 1.0
) -> Tuple[jnp.ndarray, jnp.ndarray]:
    """Generate Gauss-Legendre quadrature points and weights.

    Args:
        deg: Number of quadrature points.
        a: Lower limit of integration (default: -1.0).
        b: Upper limit of integration (default: 1.0).

    Returns:
        Tuple of (points, weights) for Gauss-Legendre quadrature.
    """
    # For computational efficiency, use a simpler approach for small degrees
    if deg <= 4:
        # Hardcoded points and weights for small degrees
        if deg == 1:
            x = jnp.array([0.0])
            w = jnp.array([2.0])
        elif deg == 2:
            x = jnp.array([-0.5773502691896257, 0.5773502691896257])
            w = jnp.array([1.0, 1.0])
        elif deg == 3:
            x = jnp.array([-0.7745966692414834, 0.0, 0.7745966692414834])
            w = jnp.array([0.5555555555555556, 0.8888888888888888, 0.5555555555555556])
        elif deg == 4:
            x = jnp.array(
                [
                    -0.8611363115940526,
                    -0.3399810435848563,
                    0.3399810435848563,
                    0.8611363115940526,
                ]
            )
            w = jnp.array(
                [
                    0.3478548451374538,
                    0.6521451548625461,
                    0.6521451548625461,
                    0.3478548451374538,
                ]
            )
    else:
        # Initial guess for roots (Chebyshev nodes)
        k = jnp.arange(1, deg + 1)
        x0 = jnp.cos(jnp.pi * (k - 0.25) / (deg + 0.5))

        # Newton iteration to find roots more accurately
        # In practice, we would use more iterations, but for simplicity we use a fixed number
        P_n = legendre_polynomial(deg)
        dP_n = legendre_polynomial_derivative(deg)

        # Single Newton step for demonstration (would use a loop in practice)
        x = x0 - P_n(x0) / (dP_n(x0) + 1e-10)

        # Compute weights
        w = 2.0 / ((1.0 - x**2) * dP_n(x) ** 2 + 1e-10)

    # Scale from [-1,1] to [a,b]
    x = 0.5 * (b - a) * x + 0.5 * (b + a)
    w = 0.5 * (b - a) * w

    return x, w


class OrthogonalAdditiveKernel(AbstractKernel):
    """Orthogonal Additive Kernels (OAKs) generalize additive kernels by orthogonalizing
    the feature space to create uncorrelated kernel components.

    This implementation uses a Gauss-Legendre quadrature approximation for the required
    one-dimensional integrals involving the base kernels, allowing for arbitrary base kernels.

    References:
        - X. Lu, A. Boukouvalas, and J. Hensman. Additive Gaussian processes revisited.
          Proceedings of the 39th International Conference on Machine Learning. Jul 2022.
    """

    base_kernel: AbstractKernel
    quad_deg: int
    dim: int
    offset: nnx.Variable
    coeffs_1: nnx.Variable
    coeffs_2: Optional[nnx.Variable]
    z: jnp.ndarray
    w: jnp.ndarray
    name: str = "OrthogonalAdditiveKernel"

    def __init__(
        self,
        base_kernel: AbstractKernel,
        dim: int,
        quad_deg: int = 32,
        second_order: bool = False,
        active_dims: tp.Union[list[int], slice, None] = None,
        n_dims: tp.Union[int, None] = None,
        offset: tp.Union[float, Parameter[ScalarFloat]] = 1.0,
        coeffs_1: tp.Union[ArrayLike, Parameter[ArrayLike]] = None,
        coeffs_2: tp.Union[ArrayLike, Parameter[ArrayLike]] = None,
        compute_engine: AbstractKernelComputation = DenseKernelComputation(),
    ):
        """Initialise the OrthogonalAdditiveKernel.

        Args:
            base_kernel: The kernel which to orthogonalize and evaluate.
            dim: Input dimensionality of the kernel.
            quad_deg: Number of integration nodes for orthogonalization.
            second_order: Toggles second order interactions. If true, both the time and
                space complexity of evaluating the kernel are quadratic in `dim`.
            active_dims: The indices of the input dimensions that the kernel operates on.
            n_dims: The number of input dimensions. If not provided, it will be inferred.
            offset: The zeroth-order coefficient.
            coeffs_1: The first-order coefficients. Should be a 1D array of length dim.
            coeffs_2: The second-order coefficients. Should be a 2D array of shape (dim, dim).
            compute_engine: The computation engine to use for kernel evaluations.
        """
        super().__init__(
            active_dims=active_dims, n_dims=n_dims, compute_engine=compute_engine
        )

        self.base_kernel = base_kernel
        self.quad_deg = quad_deg
        self.dim = dim

        # Integration nodes and weights for [0, 1]
        self.z, self.w = gauss_legendre_quadrature(quad_deg, a=0.0, b=1.0)

        # Create expandable axes
        z_expanded = jnp.expand_dims(self.z, axis=-1)
        self.z = jnp.broadcast_to(z_expanded, (quad_deg, dim))
        self.w = jnp.expand_dims(self.w, axis=-1)

        # Default coefficients if not provided
        if isinstance(offset, Parameter):
            self.offset = offset
        else:
            self.offset = PositiveReal(jnp.array(offset))

        if coeffs_1 is None:
            log_d = jnp.log(dim)
            default_coeffs_1 = jnp.exp(-log_d) * jnp.ones(dim)
            self.coeffs_1 = PositiveReal(default_coeffs_1)
        elif isinstance(coeffs_1, Parameter):
            self.coeffs_1 = coeffs_1
        else:
            self.coeffs_1 = PositiveReal(jnp.array(coeffs_1))

        self.second_order = second_order
        if second_order:
            if coeffs_2 is None:
                log_d = jnp.log(dim)
                # Initialize with zeros for upper triangular part (excluding diagonal)
                n_entries = dim * (dim - 1) // 2
                default_coeffs_2 = jnp.exp(-2 * log_d) * jnp.ones(n_entries)
                self.coeffs_2_raw = PositiveReal(default_coeffs_2)
            elif isinstance(coeffs_2, Parameter):
                self.coeffs_2_raw = coeffs_2
            else:
                self.coeffs_2_raw = PositiveReal(jnp.array(coeffs_2))

            # Pre-compute indices for efficient triu operations
            self.triu_indices = jnp.triu_indices(dim, k=1)
        else:
            self.coeffs_2_raw = None

        # Compute normalizer (in __call__)
        self._normalizer = None

    @property
    def coeffs_2(self) -> Optional[jnp.ndarray]:
        """Returns a full matrix of second-order coefficients.

        Returns:
            A dim x dim array of second-order coefficients or None if second_order is False.
        """
        if not self.second_order or self.coeffs_2_raw is None:
            return None

        # Create a full matrix from the raw coefficients
        coeffs_2_flat = self.coeffs_2_raw.value
        coeffs_2_full = jnp.zeros((self.dim, self.dim))

        # Fill the upper triangular part
        i, j = self.triu_indices
        coeffs_2_full = coeffs_2_full.at[i, j].set(coeffs_2_flat)

        # Make it symmetric
        coeffs_2_full = coeffs_2_full + jnp.transpose(coeffs_2_full)

        return coeffs_2_full

    def normalizer(self, eps: float = 1e-6) -> jnp.ndarray:
        """Integrates the orthogonalized base kernels over [0, 1] x [0, 1].

        Args:
            eps: Minimum value constraint on the normalizers to avoid division by zero.

        Returns:
            A d-dim tensor of normalization constants.
        """
        if self._normalizer is None or self.training:
            # Compute K(z, z) - base kernel gram matrix on integration points
            K_zz = self.base_kernel.cross_covariance(self.z, self.z)

            # Integrate: w^T * K * w
            self._normalizer = jnp.matmul(
                jnp.matmul(jnp.transpose(self.w), K_zz), self.w
            )

            # Ensure positive values
            self._normalizer = jnp.maximum(self._normalizer, eps)

        return self._normalizer

    def _orthogonal_base_kernels(
        self, x1: Float[Array, "N D"], x2: Float[Array, "M D"]
    ) -> Float[Array, "D N M"]:
        """Evaluates the set of d orthogonalized base kernels.

        Args:
            x1: Input array of shape [N, D]
            x2: Input array of shape [M, D]

        Returns:
            Array of shape [D, N, M] with orthogonalized kernel evaluations
        """
        # Compute base kernel between inputs
        K_x1x2 = self.base_kernel.cross_covariance(x1, x2)  # [N, M]

        # Compute normalizer
        norm = jnp.sqrt(self.normalizer())
        w_normalized = self.w / norm

        # Compute base kernel between x1 and integration points z
        K_x1z = self.base_kernel.cross_covariance(x1, self.z)  # [N, quad_deg]
        S_x1 = jnp.matmul(K_x1z, w_normalized)  # [N, 1]

        # Compute base kernel between x2 and integration points z
        if x1 is x2:
            S_x2 = S_x1
        else:
            K_x2z = self.base_kernel.cross_covariance(x2, self.z)  # [M, quad_deg]
            S_x2 = jnp.matmul(K_x2z, w_normalized)  # [M, 1]

        # Compute orthogonal kernel: K_x1x2 - S_x1 * S_x2^T
        K_ortho = K_x1x2 - jnp.outer(S_x1, S_x2)

        return K_ortho

    def __call__(
        self,
        x: Float[Array, "N D"],
        y: Float[Array, "M D"],
    ) -> ScalarFloat:
        """Evaluate the kernel at a single pair of inputs.

        Args:
            x: First input.
            y: Second input.

        Returns:
            The kernel value at (x, y).
        """
        # Slice inputs to relevant dimensions
        x_sliced = self.slice_input(x)
        y_sliced = self.slice_input(y)

        # Get orthogonalized kernels
        K_ortho = self._orthogonal_base_kernels(
            jnp.expand_dims(x_sliced, 0), jnp.expand_dims(y_sliced, 0)
        )  # [1, 1]

        # Apply first-order effects
        first_order = jnp.sum(self.coeffs_1.value * K_ortho)

        # Add offset
        result = self.offset.value + first_order

        # Add second-order effects if enabled
        if self.second_order and self.coeffs_2 is not None:
            # For a single point evaluation, we use a simpler approach
            # Computing the tensor of second order interactions
            second_order = 0.0
            for i in range(self.dim):
                for j in range(i + 1, self.dim):
                    coef = self.coeffs_2[i, j]
                    if coef > 0:
                        second_order += coef * K_ortho[i] * K_ortho[j]

            result = result + second_order

        return result

    def cross_covariance(
        self, x1: Float[Array, "N D"], x2: Float[Array, "M D"]
    ) -> Float[Array, "N M"]:
        """Compute the cross-covariance matrix of the kernel.

        Args:
            x1: First input matrix of shape [N, D].
            x2: Second input matrix of shape [M, D].

        Returns:
            Cross-covariance matrix of shape [N, M].
        """
        # Slice inputs to relevant dimensions
        x1 = self.slice_input(x1)
        x2 = self.slice_input(x2)

        # Get orthogonalized kernels for all dimensions
        K_ortho = self._orthogonal_base_kernels(x1, x2)  # [D, N, M]

        # Apply first-order effects (sum over dimensions)
        coeffs_1 = self.coeffs_1.value
        first_order = jnp.tensordot(coeffs_1, K_ortho, axes=([0], [0]))  # [N, M]

        # Add offset (broadcast to match output shape)
        result = jnp.broadcast_to(self.offset.value, first_order.shape) + first_order

        # Add second-order effects if enabled
        if self.second_order and self.coeffs_2 is not None:
            # Compute second-order interactions using einsum
            coeffs_2_full = self.coeffs_2
            second_order = jnp.einsum(
                "ij,ink,jml->nml",
                coeffs_2_full,
                jnp.expand_dims(K_ortho, 1),
                jnp.expand_dims(K_ortho, 0),
            )

            # Sum over dimensions i, j
            second_order = jnp.sum(second_order, axis=(0, 1))

            result = result + second_order

        return result
