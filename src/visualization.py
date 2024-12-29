import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmap(correlation_matrix, output_path):
    """
    Plots a heatmap of the correlation matrix.

    Args:
        correlation_matrix (pd.DataFrame): The correlation matrix to visualize.
        output_path (str): Path to save the heatmap image.

    Returns:
        None
    """
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 8))
    
    heatmap = sns.heatmap(correlation_matrix, annot=True, cmap="YlGnBu", annot_kws={"size": 10})
    plt.title("Correlation Heatmap", fontsize=16, weight='bold')
    
    heatmap.figure.savefig(output_path)
    plt.close()


def plot_sensitivity_analysis(agg_bay_normalized, num_alternatives, iteration, output_path):
    """
    Plots sensitivity analysis results for Scheme A.

    Args:
        agg_bay_normalized (list): Aggregated Bayesian values normalized for each expert.
        num_alternatives (int): Number of alternatives.
        iteration (int): Current iteration index.
        output_path (str): Path to save the sensitivity analysis plot.

    Returns:
        None
    """
    markers = ['o', 'v', '^', 's', 'P', '*', 'X', 'D', '+']
    
    fig, ax = plt.subplots(figsize=(15, 15))
    for idx, expert_values in enumerate(agg_bay_normalized):
        ax.plot(
            range(1, num_alternatives + 1),
            expert_values,
            marker=markers[idx % len(markers)],
            label=f'Expert {idx + 1}',
            linewidth=4.0,
            markersize=12.5
        )

    ax.set_xlabel('Cloud Vendors', fontsize=20, weight='bold')
    ax.set_ylabel('Rank Values', fontsize=20, weight='bold')
    ax.set_title(f'Set-{iteration + 1}', fontsize=20, weight='bold')
    
    _ , labels = ax.get_legend_handles_labels()
    plt.legend(labels, loc='upper left', ncol=8, bbox_to_anchor=(0.0, 1.0))
    
    fig.savefig(output_path)
    plt.close()


def plot_prioritization_results(prioritization_order, num_alternatives, query_type, output_path):
    """
    Plots prioritization results for Scheme B.

    Args:
        prioritization_order (np.ndarray): Prioritization order values for alternatives.
        num_alternatives (int): Number of alternatives.
        query_type (str): Query type ('Single Query' or 'Multi Query').
        output_path (str): Path to save the prioritization plot.

    Returns:
        None
    """
    fig, ax = plt.subplots(figsize=(15, 15))
    
    ax.plot(
        range(1, num_alternatives + 1),
        prioritization_order,
        marker='o',
        label=query_type,
        linewidth=4.0,
        markersize=10
    )
    
    ax.set_xlabel('Cloud Vendors', fontsize=20, weight='bold')
    ax.set_ylabel('Rank Values', fontsize=20, weight='bold')
    ax.set_title(query_type, fontsize=20, weight='bold')
    
    plt.legend(loc='upper left', ncol=8, bbox_to_anchor=(0.0, 1.0))
    
    fig.savefig(output_path)
    plt.close()
