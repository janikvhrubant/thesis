import matplotlib.pyplot as plt
from scipy.stats import qmc

# Generate 2D Sobol and Halton samples
n_samples = 1024
sobol = qmc.Sobol(d=2, scramble=False)
halton = qmc.Halton(d=2, scramble=False)
sobol_samples = sobol.random(n=n_samples)
halton_samples = halton.random(n=n_samples)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].scatter(sobol_samples[:, 0], sobol_samples[:, 1], color='lime', s=10)
axes[0].set_title('Sobol Sequence', fontsize=16)
axes[0].set_xlim(0, 1)
axes[0].set_ylim(0, 1)
axes[0].set_aspect('equal')

axes[1].scatter(halton_samples[:, 0], halton_samples[:, 1], color='blue', s=10)
axes[1].set_title('Halton Sequence', fontsize=16)
axes[1].set_xlim(0, 1)
axes[1].set_ylim(0, 1)
axes[1].set_aspect('equal')

plt.tight_layout()
plt.savefig("./Figures/sobol-vs-halton.png", dpi=600)
plt.close()
