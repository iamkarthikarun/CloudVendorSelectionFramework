from config import Config
import pandas as pd
from data_generator import DataGenerator
from transformations import (
    transform_expert_matrices,
    calculate_column_averages,
    calculate_variances,
    transform_factor_weights_gr2,
    transform_gr2_to_scalar,
)
from similarity import compute_similarity_matrix, calculate_attitude_values
from prioritization import scheme_a, scheme_b
from visualization import plot_heatmap
from printer import log_to_file, initialize_output_file
import numpy as np

config = Config()
filex = initialize_output_file(config.output_file)

def pretty_print(no_iters,print_obj):
    for iteratorp in range(0, no_iters):
        pd.options.display.width=None
        print("\n")
        print("\n", file=filex)
        pd.set_option('display.max_columns', None)
        df = pd.DataFrame(list(map(np.ravel, print_obj[iteratorp])))
        df.style.set_properties(**{'text-align': 'center'})
        print(df)
        print(df, file=filex)

generator = DataGenerator(config.num_experts, config.num_alternatives, config.num_attributes)
experts = generator.generate_expert_matrices()

print("Experts Shape:", experts.shape)
print("Experts Contents:", experts)

factor_weights = generator.generate_factor_weights()
print("Factor Weights", factor_weights.shape)

log_to_file("Main Experts:\n", filex)
pretty_print(config.num_experts, experts)

experts_transformed = transform_expert_matrices(experts)
pretty_print(config.num_experts, experts_transformed)

column_averages = calculate_column_averages(experts_transformed)
variances = calculate_variances(experts_transformed, column_averages)

similarity_matrix = compute_similarity_matrix(variances)
attitude_values = calculate_attitude_values(similarity_matrix)

print(pd.DataFrame(similarity_matrix))
print(pd.DataFrame(similarity_matrix), file=filex)

log_to_file(f"Attitude Values: {attitude_values}", filex)

print("Factor Weights Shape: ",factor_weights.shape)
print("Attitude Values Shape: ", attitude_values.shape)

factor_weight_gr2 = transform_factor_weights_gr2(factor_weights, attitude_values)
factor_weight_gr2_scalar = transform_gr2_to_scalar(factor_weight_gr2)

correlation_matrix = pd.DataFrame(factor_weight_gr2_scalar).corr(method="pearson")
plot_heatmap(correlation_matrix, f"{config.image_dir}/heatmap.png")

factor_weight_gr2_df = pd.DataFrame(factor_weight_gr2_scalar).astype('float')
deviation = factor_weight_gr2_df.std().to_numpy()
sum_rows_corr = correlation_matrix.sum(axis=1).to_numpy()
significance_values = np.abs(deviation * sum_rows_corr)

print(f"Significance Values: {significance_values}")

norm_significance = significance_values / np.sum(significance_values)
weights_sig = norm_significance.copy()

print(f"Normalized Significance Values: {norm_significance}")
print(f"Weight Vector 1x{config.num_attributes}: ", list(np.around(norm_significance, 4)))
print(f"Weight Vector 1x{config.num_attributes}: ", list(np.around(norm_significance, 4)), file=filex)

scheme_a(norm_significance, experts_transformed, config.num_alternatives, config.num_experts, filex)

GR_agg = np.empty((config.num_alternatives, config.num_attributes), dtype=object)

for alt_idx in range(config.num_alternatives):
    for attr_idx in range(config.num_attributes):
        temp_u = np.prod([
            experts[exp_idx][alt_idx][attr_idx][0] ** attitude_values[exp_idx]
            for exp_idx in range(config.num_experts)
        ])
        temp_v = np.prod([
            experts[exp_idx][alt_idx][attr_idx][1] ** attitude_values[exp_idx]
            for exp_idx in range(config.num_experts)
        ])
        GR_agg[alt_idx, attr_idx] = [temp_u, temp_v]

GR_agg_transformed = np.array([
    [
        [
            (1 - ((1 - (GR_agg[alt_idx, attr_idx][0] ** 3)) ** weights_sig[attr_idx])) ** (1 / 3),
            GR_agg[alt_idx, attr_idx][1] ** weights_sig[attr_idx]
        ]
        for attr_idx in range(config.num_attributes)
    ]
    for alt_idx in range(config.num_alternatives)
], dtype=object)

scheme_b(
    GR_agg_transformed,
    config.qrofn,
    weights_sig,
    attitude_values,
    config.num_attributes,
    config.num_alternatives,
    filex,
)

filex.close()
