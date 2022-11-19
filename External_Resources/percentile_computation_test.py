import numpy as np

a = np.array([0,1,2,3,4,5,6,7,1097, 1100, 2000])
perc = np.percentile(a, 99.95, interpolation="linear")
print(perc)