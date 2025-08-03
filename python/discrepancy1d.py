import numpy as np
import matplotlib.pyplot as plt
import os

# Example 1D point set
points = np.array([0.1, 0.2, 0.35, 0.5, 0.8])
N = len(points)
points_sorted = np.sort(points)

# Empirical CDF values
empirical_cdf = np.arange(1, N + 1) / N
uniform_cdf = points_sorted

# Compute star discrepancy: max(|F_N(x) - x|, |x - F_N(x−)|)
discrepancies = np.maximum(np.abs(empirical_cdf - uniform_cdf),
                           np.abs(np.roll(empirical_cdf, 1, axis=0) - uniform_cdf))
discrepancies[0] = np.abs(0 - uniform_cdf[0])  # handle left-limit at 0
star_discrepancy = np.max(discrepancies)
max_index = np.argmax(discrepancies)

# Plotting
plt.figure(figsize=(8, 4))
plt.step(points_sorted, empirical_cdf, where='post', label='Empirical CDF $F_N(x)$')
plt.plot([0, 1], [0, 1], 'k--', label='Ideal CDF $F(x) = x$')

# Highlight max discrepancy
plt.vlines(points_sorted[max_index], uniform_cdf[max_index], empirical_cdf[max_index],
           color='red', linestyle='-', linewidth=3, label='Max Discrepancy')
plt.scatter(points_sorted, empirical_cdf, color='blue', zorder=5)

# Annotations and styling
plt.xlabel('$x$')
plt.ylabel('Cumulative Distribution')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Ensure the Figures directory exists
os.makedirs('./Figures', exist_ok=True)
plt.savefig('./Figures/discrepancy1d.png')
plt.close()
