import numpy as np

from spekpy import Spek # Import the SpekPy library for spectral calculations
import matplotlib.pyplot as plt # Import pyplot for plotting
from numpy import arange # Import stuff from numpy

## Set parameters
# Define arrays with filtration tuples  
filters = [("Sn", 0.4),("Cu", 0.1)]
kvp = 120. # Define the tube potential in kV
target_material = 'W' # Tungsten target
theta = 12.5 # Anode angle in degrees

spectrum = Spek(kvp=120.,th=theta) # Create a spectrum
spectrum.multi_filter(filters) # Apply the filtration to the spectrum

spectrum = spectrum.get_spectrum() # Get the total fluence
energy_keVs = spectrum[0]
fluence = spectrum[1]
probability = fluence / fluence.sum()

u = np.random.rand()  # Sample a random number between 0 and 1
sampled_energy = np.random.choice(energy_keVs, p=probability)  # Sample energy based on probability distribution
print(f"Random number u: {u}, Sampled energy: {sampled_energy} keV")

## Plot the percentage against kV
plt.plot(energy_keVs,fluence) 
plt.xlabel('Tube potential  [kV]')
plt.ylabel('Perecentage of fluence  [%]')
plt.title('Percent of fluence from characteristic emissions')

## Show plots on screen
plt.show()