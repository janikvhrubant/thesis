import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "axes.labelsize": 11,
    "font.size": 11,
    "legend.fontsize": 10,
})

x = np.linspace(-6, 6, 500)
tanh = np.tanh(x)
sigmoid = 1 / (1 + np.exp(-x))

fig, ax = plt.subplots(figsize=(6.5, 2.8))

ax.plot(x, tanh, label=r'Tanh: $\tanh(x)$')
ax.plot(x, sigmoid, label=r'Sigmoid: $\sigma(x) = \frac{1}{1 + e^{-x}}$', color='orange')

ax.set_title("Activation Functions")
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.set_ylim([-2, 2])
ax.set_xlim([-6, 6])
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$\sigma(x)$')
ax.legend()

plt.tight_layout()
plt.savefig("Figures/activations_functions.png", dpi=600)
plt.close()
