from scipy.stats import qmc

# build a 2d sobol sequence and print the first 3 points
sampler = qmc.Sobol(d=2, scramble=False)
points = sampler.random(n=3)
print(points)