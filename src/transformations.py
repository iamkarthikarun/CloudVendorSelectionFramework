import numpy as np

def transform_expert_matrices(experts):
    """
    Transforms expert matrices using the formula μ^3 + ν^3.

    Args:
        experts (np.ndarray): A 4D array of shape (num_experts, num_alternatives, num_attributes, 2),
                              where the last dimension contains (μ, ν).

    Returns:
        np.ndarray: A 3D array of transformed matrices with scalar values.
    """
    try:
        # Extract μ and ν from the last dimension
        mu = experts[..., 0]  # First column (μ)
        nu = experts[..., 1]  # Second column (ν)

        # Apply the transformation μ^3 + ν^3
        transformed = mu**3 + nu**3

        return transformed
    except Exception as e:
        raise ValueError(f"Error transforming expert matrices: {e}")



def calculate_column_averages(transformed_experts):
    """
    Calculates column-wise averages for each expert's transformed matrix.

    Args:
        transformed_experts (np.ndarray): A 3D array of transformed matrices.

    Returns:
        np.ndarray: A 2D array of column averages for each expert.
    """
    return np.mean(transformed_experts, axis=1)



def calculate_variances(transformed_experts, column_averages):
    """
    Calculates variance factor-wise for each expert's transformed matrix.

    Args:
        transformed_experts (np.ndarray): A 3D array of transformed matrices.
        column_averages (np.ndarray): A 2D array of column averages for each expert.

    Returns:
        np.ndarray: A 2D array of variances for each expert.
    """
    deviations = transformed_experts - column_averages[:, None, :]
    return np.var(deviations, axis=1, ddof=1)



def transform_factor_weights_gr2(factor_weights, attitude_values):
    """
    Transforms factor weights using the GR2 formula:
    GR2 = [(1 - (1 - μ^3)^att)^1/3, v^att]

    Args:
        factor_weights (np.ndarray): A 2D array of shape (num_experts, num_attributes) containing tuples (μ, v).
        attitude_values (np.ndarray): A 1D array of normalized attitude values for each expert.

    Returns:
        np.ndarray: A 2D array of GR2-transformed weights.
    """
    num_experts, num_attributes = factor_weights.shape[0], factor_weights.shape[1]

    return np.array([
        [
            (
                (1 - ((1 - factor_weights[k, m][0]**3)**attitude_values[k]))**(1/3),
                factor_weights[k, m][1]**attitude_values[k]
            )
            for m in range(num_attributes)
        ]
        for k in range(num_experts)
    ], dtype=object)

def transform_gr2_to_scalar(gr2_weights):
    """
    Transforms GR2 weights into single scalar values using μ^3 + v^3.

    Args:
        gr2_weights (np.ndarray): A 2D array of GR2-transformed weights.

    Returns:
        np.ndarray: A 2D array of scalar-transformed GR2 weights.
    """
    mu = gr2_weights[:, :, 0]
    nu = gr2_weights[:, :, 1]
    return mu**3 + nu**3
