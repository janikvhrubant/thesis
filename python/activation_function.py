import numpy as np
import matplotlib.pyplot as plt

# LaTeX-style fonts (optional, für Konsistenz im Thesis-Look)
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "axes.labelsize": 11,
    "font.size": 11,
    "legend.fontsize": 10,
})

# Wertebereich
x = np.linspace(-6, 6, 500)
relu = np.maximum(0, x)
sigmoid = 1 / (1 + np.exp(-x))

# Plot erstellen
fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.8))  # Side-by-side

# ReLU
axs[0].plot(x, relu, label=r'$\mathrm{ReLU}(x)$')
axs[0].set_title("ReLU Activation")
axs[0].axhline(0, color='gray', lw=0.5)
axs[0].axvline(0, color='gray', lw=0.5)
axs[0].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Sigmoid
axs[1].plot(x, sigmoid, label=r'$\sigma(x) = \frac{1}{1 + e^{-x}}$', color='orange')
axs[1].set_title("Sigmoid Activation")
axs[1].axhline(0, color='gray', lw=0.5)
axs[1].axvline(0, color='gray', lw=0.5)
axs[1].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Layout und speichern
axs[0].set_ylim([-0.5, 6])
axs[0].set_xlim([-6, 6])
axs[0].set_xlabel(r'$x$')
axs[0].set_ylabel(r'$ReLu(x)$')

axs[1].set_ylim([-0.5, 6])
axs[1].set_xlim([-6, 6])
axs[1].set_xlabel(r'$x$')
axs[1].set_ylabel(r'$\sigma(x)$')

plt.tight_layout()
plt.savefig("Figures/activations_functions.png", dpi=600)
plt.close()