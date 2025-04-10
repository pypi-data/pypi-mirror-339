# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: docs
#     language: python
#     name: python3
# ---

# %% [markdown]
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

# %%
"""Example of using the OrthogonalAdditiveKernel."""

# %%
import jax
from jax import config

config.update("jax_enable_x64", True)  # Enable Float64 precision

import jax.numpy as jnp
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import optax

import gpjax as gpx
from gpjax.dataset import Dataset
from gpjax.kernels import OrthogonalAdditiveKernel, RBF
from gpjax.typing import KeyArray


# %%
def f(x: jnp.ndarray) -> jnp.ndarray:
    """Additive function with mixed dependencies:
    f(x) = sin(π*x₁) + 2*cos(2π*x₂) + 0.5*sin(3π*x₁*x₂)

    Args:
        x: Input points array with shape (..., 2)

    Returns:
        Function values at the input points
    """
    return (
        jnp.sin(jnp.pi * x[..., 0])
        + 2.0 * jnp.cos(2.0 * jnp.pi * x[..., 1])
        + 0.5 * jnp.sin(3.0 * jnp.pi * x[..., 0] * x[..., 1])
    )


# %%
def generate_data(
    key: KeyArray, n_train: int = 100, noise_std: float = 0.1
) -> tuple[Dataset, jnp.ndarray, jnp.ndarray]:
    """Generate synthetic training data.

    Args:
        key: JAX PRNG key for random number generation
        n_train: Number of training points to generate
        noise_std: Standard deviation of Gaussian observation noise

    Returns:
        Tuple of (training_data, X_test, meshgrid_for_plotting)
    """
    key1, key2, key3 = jax.random.split(key, 3)

    # Generate training data
    X_train = jax.random.uniform(key1, (n_train, 2))
    y_train = f(X_train) + noise_std * jax.random.normal(key2, (n_train,))

    training_data = Dataset(X=X_train, y=y_train[:, None])

    # Generate test points for prediction
    n_test = 20
    x_range = jnp.linspace(0.0, 1.0, n_test)
    X1, X2 = jnp.meshgrid(x_range, x_range)
    X_test = jnp.vstack([X1.flatten(), X2.flatten()]).T

    return training_data, X_test, (X1, X2)


# %%
def main():
    # Set random seed for reproducibility
    key = jax.random.PRNGKey(42)

    # Generate synthetic training data
    training_data, X_test, (X1, X2) = generate_data(key, n_train=100, noise_std=0.1)

    # Create base kernel (RBF)
    base_kernel = RBF(lengthscale=0.2)

    # Create OAK kernel with second-order interactions
    oak_kernel = OrthogonalAdditiveKernel(
        base_kernel=base_kernel,
        dim=2,
        quad_deg=20,
        second_order=True,
    )

    # Create a GP prior model
    prior = gpx.gps.Prior(
        mean_function=gpx.mean_functions.Zero(),
        kernel=oak_kernel,
    )

    # Create a likelihood
    likelihood = gpx.likelihoods.Gaussian(num_datapoints=training_data.n)

    # Create the posterior
    posterior = prior * likelihood

    # Create parameter optimizer
    optimizer = optax.adam(learning_rate=0.01)

    # Define objective function for training
    def objective(model, data):
        return -model.mll(model.params, data)

    # Optimize hyperparameters
    opt_posterior, history = gpx.fit(
        model=posterior,
        objective=objective,
        train_data=training_data,
        optim=optimizer,
        num_iters=300,
        key=key,
        verbose=True,
    )

    # Plot training curve
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history)
    plt.title("Negative Log Marginal Likelihood")
    plt.xlabel("Iteration")
    plt.ylabel("NLML")

    # Get posterior predictions
    latent_dist = opt_posterior.predict(params=opt_posterior.params, x=X_test)
    predictive_dist = opt_posterior.likelihood.condition(
        latent_dist, opt_posterior.params
    )
    mu = predictive_dist.mean().reshape(X1.shape)
    std = predictive_dist.stddev().reshape(X1.shape)

    # Plot predictions
    plt.subplot(1, 2, 2)
    plt.contourf(X1, X2, mu, 50, cmap="viridis")
    plt.colorbar(label="Predicted Mean")
    plt.scatter(
        training_data.X[:, 0],
        training_data.X[:, 1],
        c=training_data.y,
        cmap=ListedColormap(["red", "blue"]),
        alpha=0.6,
        s=20,
        edgecolors="k",
    )
    plt.title("OAK GP Predictions")
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")

    plt.tight_layout()
    plt.savefig("oak_example.png", dpi=300)
    plt.show()

    # Print learned kernel parameters
    print("\nLearned Parameters:")
    print(f"Offset coefficient: {opt_posterior.params.kernel.offset.value}")
    print(f"First-order coefficients: {opt_posterior.params.kernel.coeffs_1.value}")

    # Analyze the importance of each dimension
    importance_1st_order = opt_posterior.params.kernel.coeffs_1.value
    total_importance = jnp.sum(importance_1st_order)
    relative_importance = importance_1st_order / total_importance

    print("\nRelative Importance of Input Dimensions:")
    for i, imp in enumerate(relative_importance):
        print(f"Dimension {i+1}: {imp:.4f}")

    if opt_posterior.params.kernel.coeffs_2 is not None:
        # Analyze second-order interactions
        coeffs_2 = opt_posterior.params.kernel.coeffs_2
        print("\nSecond-order Interaction Coefficient:")
        print(f"{coeffs_2[0, 1]:.4f}")


# %%
if __name__ == "__main__":
    main()

# %%
