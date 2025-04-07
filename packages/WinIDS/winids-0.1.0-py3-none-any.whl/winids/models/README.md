# WinIDS Model Files

This directory contains the machine learning model files used by the WinIDS system.

## Required Files

The following files are required for the WinIDS system to function correctly:

1. `best_fast_model.h5` - TensorFlow model file for network traffic classification
2. `normalization_params.json` - JSON file containing normalization parameters for features

## Reinforcement Learning Models

When using the reinforcement learning capabilities of WinIDS, additional model files are created:

1. `dqn_model.h5` - Deep Q-Network model for the reinforcement learning agent
2. `adaptive_state.json` - Saved state of the adaptive IDS, including threshold values and metrics

These files are automatically saved to the directory specified by the `rl_model_dir` parameter (default: `./rl_models`).

## Model Training

The models are trained on network traffic data with the following attack categories:
- Normal traffic
- DOS (Denial of Service)
- Probe (Network scanning and probing)
- R2L (Remote to Local attacks)
- U2R (User to Root attacks)

## Getting Started

If you're using the package for the first time, download the pretrained models from:
https://github.com/yourusername/winids-models

Or train your own models using your own network traffic data with the provided training scripts.

## Custom Model Creation

To create your own models, collect network traffic data and use the following scripts:
- `winids/scripts/train_model.py`
- `winids/scripts/normalize_features.py`

## Model Structure

The default model is a multi-layer neural network with the following architecture:
- Input layer: Feature vector size
- Hidden layers: Multiple dense layers with dropout
- Output layer: 5 nodes (normal, dos, probe, r2l, u2r)

## RL Agent Structure

The reinforcement learning agent uses a Deep Q-Network with the following architecture:
- Input layer: State size (features representing system status)
- Hidden layers: Dense layers with dropout for regularization
- Output layer: Action size (different threshold adjustment values)

The agent learns through interaction with the environment, receiving rewards for correctly identifying attacks while minimizing false positives.

## Feature Normalization

Feature normalization is critical for model performance. The normalization parameters
are stored in the `normalization_params.json` file with the following structure:

```json
{
  "mean": [feature1_mean, feature2_mean, ...],
  "std": [feature1_std, feature2_std, ...]
}
``` 