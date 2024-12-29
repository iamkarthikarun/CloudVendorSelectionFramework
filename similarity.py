import numpy as np
import pandas as pd

def compute_similarity_matrix(variances):
    """
    Constructs a similarity matrix between experts based on variance vectors.

    Args:
        variances (list): A list of variance vectors for each expert.

    Returns:
        np.ndarray: A 2D similarity matrix of shape (num_experts, num_experts).
    """
    num_experts = len(variances)
    similarity_matrix = np.zeros((num_experts, num_experts))

    for s in range(num_experts):
        for t in range(num_experts):
            if s != t:

                distance = np.sqrt(np.sum((np.array(variances[s]) - np.array(variances[t]))**2))
                similarity_matrix[s, t] = 1 - distance  
            else:
                similarity_matrix[s, t] = 1.0 

    return similarity_matrix



def calculate_attitude_values(similarity_matrix):
    """
    Calculates attitude values for each expert based on the similarity matrix.

    Args:
        similarity_matrix (np.ndarray): A 2D similarity matrix of shape (num_experts, num_experts).

    Returns:
        np.ndarray: A 1D array of normalized attitude values for each expert.
    """
    num_experts = similarity_matrix.shape[0]
    
    mask = ~np.eye(num_experts, dtype=bool)
    attitude_values = np.sum(similarity_matrix * mask, axis=1) / (num_experts - 1)
    
    attitude_values /= np.sum(attitude_values)
    
    return attitude_values



def log_similarity_and_attitudes(similarity_matrix, attitude_values, filex):
    """
    Logs the similarity matrix and attitude values to a file.

    Args:
        similarity_matrix (np.ndarray): The computed similarity matrix.
        attitude_values (np.ndarray): The computed attitude values.
        filex (file object): The file object to write logs to.
    """
    similarity_df = pd.DataFrame(similarity_matrix)
    
    print("Similarity Matrix:\n", similarity_df, file=filex)
    print("Similarity Matrix:\n", similarity_df)

    print(f"Attitude Values: {np.around(attitude_values, 4)}", file=filex)
    print(f"Attitude Values: {np.around(attitude_values, 4)}")
