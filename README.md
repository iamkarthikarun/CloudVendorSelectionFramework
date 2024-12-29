# A Decision-Aiding Framework for Two-Way Selection of Cloud Vendors in Medical Centers

This repository contains the official implementation of the research paper titled **"A Decision Aiding Framework for Two-Way Selection of Cloud Vendors in Medical Centers With Generalized Orthopair Fuzzy Information"**, authored by **R. Krishankumar, Karthik Arun R, Dragan Pamucar, and K. S. Ravichandran**.

## Overview

This repository is a code-share of a research paper I worked on during my undergrad at SASTRA University, Thanjavur, India. It is not an out-of-the-box usage ready repo since that was not the sole intention but to provide substantial mathematical evidence for the theories mentioned in the research paper.

The project introduces a novel decision-aiding framework for the **selection of cloud vendors (CVs)** in healthcare systems using **Generalized Orthopair Fuzzy Information (GOFI)**. The framework addresses critical challenges in cloud vendor selection, including:
- Handling uncertainty and hesitation during preference elicitation.
- Modeling interdependencies between factors.
- Providing personalized rankings based on agent-driven and user-driven preferences.

The framework implements two prioritization schemes:
1. **Scheme A (Agent-Based Prioritization)**: Ranks CVs based on agents' preferences and attitudes.
2. **Scheme B (Query-Based Prioritization)**: Allows users to input queries for personalized CV rankings.

This repository contains the Python code used for the implementation, analysis, sensitivity testing, and visualization of results.

---

## Features

- **Agent Attitude Calculation**: Uses a variance-based similarity approach to compute agents' attitudes.
- **Factor Weight Determination**: Extends the CRITIC method to capture interdependencies among factors while incorporating agent attitudes.
- **Two-Way Prioritization**:
  - **Agent-Driven**: Aggregates agents' preferences using Bayesian approximation.
  - **User-Driven**: Computes rankings based on user-defined query vectors.
- **Robustness Testing**: Includes sensitivity analysis to validate the stability of rankings under varying factor weights and query inputs.
- **Visualization**: Generates heatmaps, sensitivity plots, and ranking visualizations for better interpretability.

---

## Repository Structure

```
├── config.py              # Configuration file for parameters and paths
├── data_generator.py      # Handles generation of expert matrices and factor weights
├── main.py                # Main script implementing both prioritization schemes
├── printer.py             # Utility for formatted printing of matrices
├── prioritization.py      # Implements Scheme A and Scheme B prioritizations
├── similarity.py          # Computes similarity matrix and attitude values
├── transformations.py     # Handles matrix and weight transformations
├── utils.py               # Utility functions (e.g., rotate)
├── visualization.py       # Handles all plotting and graphical outputs
├── results/               # Directory containing output files and visualizations
│   ├── opfile.txt         # Output log file for all results including Attitudinal-CRITIC values, rankings, prioritizations etc.,
│   ├── images/
│   │   ├──heatmap.png                  # Correlation heatmap
│   │   ├──SchemeB_Query_<N>.png        # Prioritization plots for Scheme B for various query values (N denotes query values)
│   │   ├──SchemeB_Single_Query.png     # Prioritization plot for Scheme B for single query value
│   │   ├──Set_<N>_SchemeA.png          # Sensitivity analysis plots for Scheme A (N denotes various iterations)

```

---

### Output Files
The results are saved in the `results/` directory:
- **Heatmaps**: Visualizations of factor interrelationships.
- **Ranking Files**: Text files containing CV rankings for each sensitivity test or query set.
- **Plots**: Sensitivity analysis plots showing ranking stability under varying conditions.

---

## Methodology

### Scheme A: Agent-Based Prioritization
1. Compute weighted GOFI values based on agents' preferences and factor weights.
2. Normalize using Bayesian approximation to determine ranking scores.
3. Aggregate Bayesian values across attributes to produce final rankings.

### Scheme B: Query-Based Prioritization
1. Aggregate expert evaluations into a single matrix using attitude values.
2. Match user queries against aggregated evaluations using a distance norm.
3. Rank CVs based on proximity to user-defined preferences.

---

## Results

### Case Study
The framework was applied to a real-world case study involving cloud vendor selection for a private hospital in Tamil Nadu, India. The results demonstrated:
- Robustness to changes in factor weights or query inputs.
- Flexibility in handling both agent-driven and user-driven prioritization scenarios.

### Sensitivity Analysis
Comprehensive sensitivity tests confirmed that the framework is highly stable under varying conditions, ensuring reliable decision-making.

---

## Citation

If you use this code or find it helpful, please cite our research paper:

```
@article{9502144,
  author={Krishankumar, R. and Arun, Karthik and Pamucar, Dragan and Ravichandran, K. S.},
  journal={IEEE Transactions on Engineering Management}, 
  title={A Decision Aiding Framework for Two-Way Selection of Cloud Vendors in Medical Centers With Generalized Orthopair Fuzzy Information}, 
  year={2023},
  volume={70},
  number={10},
  pages={3653-3664},
  keywords={Uncertainty;Decision making;Approximation algorithms;Quality of service;Power measurement;Optical fibers;Mathematical model;Attitudinal critic;cloud vendors (CVs);generalized orthopair;variance method},
  doi={10.1109/TEM.2021.3097139}}
```

---

## Contact

For any questions or feedback regarding this project:
- Email: karthikarun2000@gmail.com
