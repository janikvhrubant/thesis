from spekpy import Spek
import matplotlib.pyplot as plt

# Create the spectrum with 80 kVp and 0.4 mm Sn filter
spek = Spek(kvp=100, targ="W")
spek = spek.filter("Sn", 0.4)

# Get energies separately
energies, intensities = spek.get_spectrum()
print(energies)
print(intensities)

# Plot
plt.plot(energies, intensities)
plt.xlabel("Energy (keV)")
plt.ylabel("Fluence")
# plt.grid(True)
plt.savefig("Figures/spectrum_with_filter.png", dpi=300, bbox_inches='tight')
# plt.show()
