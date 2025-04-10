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

from typing import (
    Callable,
    Tuple,
    List,
    Dict,
    Any,
    Optional,
    TypeVar,
    Union,
    cast,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture

import jax
import jax.numpy as jnp
import pytest
from jaxtyping import Float, Array

from gpjax.kernels import RBF, OrthogonalAdditiveKernel, AbstractKernel
from gpjax.kernels.nonstationary.oak import gauss_legendre_quadrature


@pytest.mark.parametrize("deg", [1, 2, 3, 4, 8, 16])
def test_gauss_legendre_quadrature(deg: int) -> None:
    """Test that the Gauss-Legendre quadrature implementation correctly
    integrates simple polynomials.

    Args:
        deg: Number of quadrature points
    """

    # For a polynomial of degree 2*deg-1 or less, the quadrature should be exact
    def f(x: Float[Array, " N"]) -> Float[Array, " N"]:
        """Simple polynomial function: f(x) = x^2"""
        return x**2

    # Compute integral with quadrature
    x, w = gauss_legendre_quadrature(deg, a=0.0, b=1.0)
    quad_result = jnp.sum(w * f(x))

    # Compare with analytical result (∫₀¹ x² dx = 1/3)
    expected = 1.0 / 3.0
    assert jnp.isclose(quad_result, expected, rtol=1e-5)


def test_oak_init() -> None:
    """Test initialization of OrthogonalAdditiveKernel"""
    # Basic initialization
    base_kernel = RBF(lengthscale=0.5)
    oak = OrthogonalAdditiveKernel(base_kernel=base_kernel, dim=2, quad_deg=8)

    # Check attributes
    assert oak.dim == 2
    assert oak.quad_deg == 8
    assert isinstance(oak.base_kernel, RBF)
    assert oak.z.shape == (8, 2)
    assert oak.w.shape == (8, 1)

    # Check default parameters
    assert oak.offset.value > 0.0
    assert oak.coeffs_1.value.shape == (2,)
    assert oak.coeffs_2 is None


def test_oak_second_order() -> None:
    """Test initialization of OrthogonalAdditiveKernel with second-order interactions"""
    # Initialize with second-order interactions
    base_kernel = RBF(lengthscale=0.5)
    oak = OrthogonalAdditiveKernel(
        base_kernel=base_kernel, dim=3, quad_deg=8, second_order=True
    )

    # Check second-order coefficients
    assert oak.second_order is True
    assert oak.coeffs_2 is not None
    assert oak.coeffs_2.shape == (3, 3)

    # Check coefficients symmetry
    assert jnp.isclose(oak.coeffs_2[0, 1], oak.coeffs_2[1, 0])
    assert jnp.isclose(oak.coeffs_2[0, 2], oak.coeffs_2[2, 0])
    assert jnp.isclose(oak.coeffs_2[1, 2], oak.coeffs_2[2, 1])


def test_orthogonal_base_kernels() -> None:
    """Test the orthogonalization of base kernels"""
    # Create test points
    x1 = jnp.array([[0.3, 0.7]])
    x2 = jnp.array([[0.4, 0.6]])

    # Create kernel
    base_kernel = RBF(lengthscale=0.5)
    oak = OrthogonalAdditiveKernel(base_kernel=base_kernel, dim=2, quad_deg=8)

    # Compute orthogonalized kernels
    K_ortho = oak._orthogonal_base_kernels(x1, x2)

    # Verify shape
    assert K_ortho.shape == (2, 1, 1)

    # Verify orthogonality criterion
    # For a single input, the orthogonal kernels should have near-zero means
    z, w = gauss_legendre_quadrature(32, a=0.0, b=1.0)
    z_test = jnp.vstack(
        [z, jnp.ones_like(z) * 0.5]
    )  # Add a second dimension with constant values

    K_test = oak._orthogonal_base_kernels(jnp.expand_dims(z_test.T, 1), x2)

    # Compute mean along first dimension, which should be close to zero
    mean_K = jnp.sum(w.reshape(-1, 1, 1) * K_test[0], axis=0)
    assert jnp.all(jnp.abs(mean_K) < 1e-5)


def test_oak_call() -> None:
    """Test that the kernel's call method works correctly"""
    # Create test points
    x1 = jnp.array([0.3, 0.7])
    x2 = jnp.array([0.4, 0.6])

    # Create kernel
    base_kernel = RBF(lengthscale=0.5)
    oak = OrthogonalAdditiveKernel(base_kernel=base_kernel, dim=2, quad_deg=8)

    # Set coefficients for predictable results
    oak.offset = jnp.array(1.0)
    oak.coeffs_1 = jnp.array([0.5, 0.5])

    # Call kernel
    k_val = oak(x1, x2)

    # Ensure result is a scalar and not NaN
    assert k_val.ndim == 0
    assert not jnp.isnan(k_val)
    assert jnp.isfinite(k_val)


def test_oak_cross_covariance() -> None:
    """Test the cross_covariance method"""
    # Create test points
    x1 = jnp.array([[0.3, 0.7], [0.1, 0.9]])
    x2 = jnp.array([[0.4, 0.6], [0.2, 0.8], [0.5, 0.5]])

    # Create kernel
    base_kernel = RBF(lengthscale=0.5)
    oak = OrthogonalAdditiveKernel(
        base_kernel=base_kernel, dim=2, quad_deg=8, second_order=True
    )

    # Compute cross-covariance
    K = oak.cross_covariance(x1, x2)

    # Verify shape
    assert K.shape == (2, 3)

    # Verify values are finite
    assert jnp.all(jnp.isfinite(K))


def test_oak_gram() -> None:
    """Test the gram matrix computation"""
    # Create test points
    x = jnp.array([[0.3, 0.7], [0.1, 0.9], [0.5, 0.5]])

    # Create kernel
    base_kernel = RBF(lengthscale=0.5)
    oak = OrthogonalAdditiveKernel(
        base_kernel=base_kernel, dim=2, quad_deg=8, second_order=True
    )

    # Compute gram matrix
    gram = oak.gram(x)

    # Convert to dense for testing
    gram_dense = gram.to_dense()

    # Verify shape
    assert gram_dense.shape == (3, 3)

    # Verify values are finite
    assert jnp.all(jnp.isfinite(gram_dense))

    # Verify the matrix is symmetric
    assert jnp.allclose(gram_dense, gram_dense.T, rtol=1e-5)

    # Verify the diagonal is positive
    assert jnp.all(jnp.diag(gram_dense) > 0)
