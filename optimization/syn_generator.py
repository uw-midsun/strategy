import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
num_samples = 100000
pitch_values = np.random.uniform(low=0, high=10, size=num_samples)
noise = np.random.normal(loc=0, scale=1, size=num_samples)
velocity_values = 2 * pitch_values + 1 + noise

# Create a DataFrame
data = pd.DataFrame({'pitch': pitch_values, 'velocity': velocity_values})

# Save the synthetic dataset to a CSV file
data.to_csv('synthetic_training.csv', index=False)