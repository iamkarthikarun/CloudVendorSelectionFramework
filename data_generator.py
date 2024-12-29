import numpy as np
import random
class DataGenerator:
    """
    A class to generate expert decision matrices and factor weights for fuzzy logic-based decision-making.

    Attributes:
        num_experts (int): Number of experts.
        num_alternatives (int): Number of alternatives.
        num_attributes (int): Number of attributes.
        qrofn (list): Predefined list of GOFI values (membership, non-membership grades).
    """

    def __init__(self, num_experts, num_alternatives, num_attributes):
        """
        Initializes the DataGenerator with the given parameters.

        Args:
            num_experts (int): Number of experts.
            num_alternatives (int): Number of alternatives.
            num_attributes (int): Number of attributes.
        """
        self.num_experts = num_experts
        self.num_alternatives = num_alternatives
        self.num_attributes = num_attributes
        self.qrofn = [
            (0.98, 0.01), (0.9, 0.6), (0.8, 0.65), (0.75, 0.6),
            (0.5, 0.5), (0.6, 0.7), (0.7, 0.8), (0.6, 0.9), (0.01, 0.98)
        ]

    def generate_expert_matrices(self):
        """
        Generates random expert decision matrices.

        Returns:
            np.ndarray: A 3D array of shape (num_experts, num_alternatives, num_attributes) containing GOFI values.
        """
        # Randomly select GOFI values for each expert's matrix
        return np.array([
            np.array([
                [random.choice(self.qrofn) for _ in range(self.num_attributes)]
                for _ in range(self.num_alternatives)
            ])
            for _ in range(self.num_experts)
        ], dtype=object)

    def generate_factor_weights(self):
        """
        Generates random factor weights for each expert.

        Returns:
            np.ndarray: A 2D array of shape (num_experts, num_attributes) containing GOFI values as factor weights.
        """
        # Randomly select GOFI values for each expert's factor weights
        return np.array([
            [random.choice(self.qrofn) for _ in range(self.num_attributes)]
            for _ in range(self.num_experts)
        ], dtype=object)

