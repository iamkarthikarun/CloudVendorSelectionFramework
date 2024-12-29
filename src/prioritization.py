import numpy as np
import matplotlib.pyplot as plt
import random
from visualization import plot_sensitivity_analysis, plot_prioritization_results
from config import Config

config = Config()
def rotate(arr, steps=1):
    """
    Rotates a list or NumPy array by the specified number of steps.

    Args:
        arr (list or np.ndarray): The list or array to rotate.
        steps (int): Number of steps to rotate. Positive for right rotation, negative for left.

    Returns:
        list or np.ndarray: Rotated list or array.
    """
    if arr is None or arr.size == 0:
        return arr
    steps = -steps % len(arr)
    return np.concatenate((arr[steps:], arr[:steps])) if isinstance(arr, np.ndarray) else arr[steps:] + arr[:steps]


def scheme_a(norm_significance, experts, num_alternatives, num_experts, filex):
    """
    Implements Scheme A: Agent-Based Prioritization.

    Args:
        norm_significance (np.ndarray): Normalized significance weights.
        experts (np.ndarray): Expert decision matrices.
        num_alternatives (int): Number of alternatives.
        num_experts (int): Number of experts.
        filex (file object): File object for logging results.

    Returns:
        None
    """

    print("\n Scheme A: ", file=filex)
    rotated_weights = norm_significance
    for iteration in range(len(norm_significance)):
        rotated_weights = rotate(rotated_weights)

        print(f"Weight Vector {iteration + 1}: {list(np.around(rotated_weights, 4))}", file=filex)
        print(f"Weight Vector {iteration + 1}: {list(np.around(rotated_weights, 4))}")

        weighted_gofi = np.array([
            np.multiply(expert_matrix, rotated_weights) for expert_matrix, rotated_weights in zip(experts, [rotated_weights] * len(experts))
        ])

        net_experts_gofi = np.array([
            np.hstack([
                weighted_matrix,
                1 - np.sum(weighted_matrix, axis=1, keepdims=True)
            ])
            for weighted_matrix in weighted_gofi
        ])

        bay_approx = np.array([
            net_matrix[:, :-1] / (net_matrix[:, -1][:, None] * num_alternatives)
            for net_matrix in net_experts_gofi
        ])

        norm_bay_approx = np.array([
            bay_matrix / bay_matrix.sum(axis=1, keepdims=True)
            for bay_matrix in bay_approx
        ])

        agg_bay = [
            [np.prod(norm_bay_approx[expert_idx][alt_idx]) for alt_idx in range(num_alternatives)]
            for expert_idx in range(num_experts)
        ]
        
        agg_bay_normalized = [
            [value / sum(expert_values) for value in expert_values]
            for expert_values in agg_bay
        ]

        if iteration == len(norm_significance) - 1:
            for expert_values in agg_bay_normalized:
                print("Aggr. Bayesian: ", list(np.around(expert_values, 4)), file=filex)
                print("Rank: ", np.argsort(-np.array(expert_values), kind='stable'), file=filex)

        plot_sensitivity_analysis(
            agg_bay_normalized,
            num_alternatives,
            iteration,
            config.image_dir+f"Set_{iteration + 1}_SchemeA.png"
        )
        

def scheme_b(GR_agg, qrofn, weights_sig, attitude_values, num_attributes,
             num_alternatives, filex):
    """
    Implements Scheme B: Query-Based Prioritization.

    Args:
        GR_agg (np.ndarray): Aggregated GR2 weights across experts.
        qrofn (list): Predefined GOFI values.
        weights_sig (np.ndarray): Significance weights.
        attitude_values (np.ndarray): Attitude values of experts.
        num_attributes (int): Number of attributes.
        num_alternatives (int): Number of alternatives.
        filex (file object): File object for logging results.

    Returns:
        None
    """
    print("\n Scheme B:", file=filex)

    query_vector = [random.choice(qrofn) for _ in range(num_attributes)]
    print(f"Single Query: {query_vector}", file=filex)

    prioritization_order = np.array([
        np.sqrt(np.sum([
            (GR_agg[alt_idx][attr_idx][0] - query_vector[attr_idx][0])**2 +
            (GR_agg[alt_idx][attr_idx][1] - query_vector[attr_idx][1])**2
            for attr_idx in range(num_attributes)
        ]))
        for alt_idx in range(num_alternatives)
    ])

    print(f"Prioritization Values: {np.around(prioritization_order, 4).tolist()}", file=filex)
    print(f"Rank: {np.argsort(prioritization_order).tolist()}", file=filex)

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.plot(range(1, num_alternatives + 1), prioritization_order,
            marker='o', label='Single Query', linewidth=4.0, markersize=10)
    ax.set_xlabel('Cloud Vendors', fontsize=20, weight='bold')
    ax.set_ylabel('Rank Values', fontsize=20, weight='bold')
    ax.set_title('Query-1', fontsize=20, weight='bold')
    ax.legend(loc='upper left', ncol=8, bbox_to_anchor=(0.0, 1.0))
    fig.savefig(config.image_dir+"SchemeB_Single_Query.png")

    print("MultiQuery: 3, 5, 30, 50", file=filex)

    for iter_count in [3, 5, 30, 50]:

        multi_query = np.array([[random.choice(qrofn) for _ in range(num_attributes)] for _ in range(iter_count)])
        
        aggregated_query = [
            (
                np.prod([multi_query[qry_idx][attr_idx][0] ** (1 / iter_count) for qry_idx in range(iter_count)]),
                np.prod([multi_query[qry_idx][attr_idx][1] ** (1 / iter_count) for qry_idx in range(iter_count)])
            )
            for attr_idx in range(num_attributes)
        ]

        print(f"Aggregated Query ({iter_count} Queries): {aggregated_query}", file=filex)
        print(f"Aggregated Query ({iter_count} Queries): {aggregated_query}")

        prioritization_order_multi = np.array([
            np.sqrt(np.sum([
                (GR_agg[alt_idx][attr_idx][0] - aggregated_query[attr_idx][0])**2 +
                (GR_agg[alt_idx][attr_idx][1] - aggregated_query[attr_idx][1])**2
                for attr_idx in range(num_attributes)
            ]))
            for alt_idx in range(num_alternatives)
        ])

        print(f"Prioritization Values ({iter_count} Queries): {np.around(prioritization_order_multi, 4).tolist()}", file=filex)
        print(f"Prioritization Values ({iter_count} Queries): {np.around(prioritization_order_multi, 4).tolist()}")
        print(f"Rank ({iter_count} Queries): {np.argsort(prioritization_order_multi).tolist()}\n", file=filex)
        print(f"Rank ({iter_count} Queries): {np.argsort(prioritization_order_multi).tolist()}\n")

        plot_prioritization_results(
            prioritization_order_multi,
            num_alternatives,
            f"Query-{iter_count}",
            config.image_dir+f"SchemeB_Query_{iter_count}.png"
        )
