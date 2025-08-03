import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import qmc
import os

# Approximate star discrepancy using a grid-based upper bound (not exact)
def approximate_star_discrepancy(points, resolution=100):
    s = points.shape[1]
    grid = np.linspace(0, 1, resolution)
    max_diff = 0
    for x in grid:
        for y in grid:
            box = np.array([x, y])
            volume = np.prod(box)
            count = np.sum(np.all(points <= box, axis=1))
            empirical = count / len(points)
            max_diff = max(max_diff, abs(empirical - volume))
    return max_diff

# Sample sizes
Ns = np.logspace(2, 3.5, 10, dtype=int)
disc_mc, disc_halton, disc_sobol = [], [], []

# Discrepancy computation
for N in Ns:
    # MC
    points_mc = np.random.rand(N, 2)
    disc_mc.append(approximate_star_discrepancy(points_mc))

    # Halton
    sampler_halton = qmc.Halton(d=2, scramble=False)
    points_halton = sampler_halton.random(n=N)
    disc_halton.append(approximate_star_discrepancy(points_halton))

    # Sobol
    sampler_sobol = qmc.Sobol(d=2, scramble=False)
    points_sobol = sampler_sobol.random(n=N)
    disc_sobol.append(approximate_star_discrepancy(points_sobol))

# Plotting
plt.figure(figsize=(10, 6))
plt.loglog(Ns, disc_mc, label='Monte Carlo', color='red', marker='s', markersize=6)      # square
plt.loglog(Ns, disc_halton, label='Halton', color='blue', marker='^', markersize=6)      # triangle
plt.loglog(Ns, disc_sobol, label='Sobol', color='gold', marker='o', markersize=6)        # circle

plt.xlabel('Number of Points (N)')
plt.ylabel('Approximate Star Discrepancy $D_N^*$')
plt.legend()
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.tight_layout()
os.makedirs("./Figures", exist_ok=True)
plt.savefig("./Figures/qmc_discrepancy_comparison.pdf")
plt.close()