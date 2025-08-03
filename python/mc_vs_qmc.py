import numpy as np
from scipy.stats.qmc import Sobol

import matplotlib.pyplot as plt
import os

# Number of points
n_points = 300

# Generate 2D Monte Carlo (MC) sequence
mc_points = np.random.rand(n_points, 2)

# Generate 2D Quasi-Monte Carlo (QMC) Sobol sequence
sobol_engine = Sobol(d=2, scramble=False)
qmc_points = sobol_engine.random(n_points)

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# MC plot
axs[0].scatter(mc_points[:, 0], mc_points[:, 1], color='blue', s=10)
# axs[0].set_title('2D Monte Carlo')
axs[0].set_xlim(0, 1)
axs[0].set_ylim(0, 1)
axs[0].set_aspect('equal')

# QMC Sobol plot
axs[1].scatter(qmc_points[:, 0], qmc_points[:, 1], color='red', s=10)
# axs[1].set_title('2D QMC Sobol')
axs[1].set_xlim(0, 1)
axs[1].set_ylim(0, 1)
axs[1].set_aspect('equal')

plt.tight_layout()

# Ensure the directory exists
output_dir = os.path.join(os.path.dirname(__file__), '../Figures')
os.makedirs(output_dir, exist_ok=True)

# Save the figure
plt.savefig(os.path.join(output_dir, 'mc_vs_qmc.png'))

plt.close()