import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

#theta
def theta(x, A, B, C, D):
    return A*np.sin(B*x+C)+D

#reading data
f = open("data/coord.txt", "r")
data = f.read()
data = data.split(" ")

y = data[:-1]
y = np.array([float(num) for num in y])
x = np.linspace(0.0, 15.55, len(y))

#fitting
param, param_cov = curve_fit(theta, x, y, p0 = [35.0, 3.7699, 0.0, 85.0])
print("Sine function coefficients:")
print(param)
print("Covariance of coefficients:")
print(param_cov)
print(np.sqrt(np.diag(param_cov)))

#plotting
plt.plot(x, y, color="red", label="data")
fit = theta(x, param[0], param[1], param[2], param[3])
plt.plot(x, fit, color="blue", label="fit")
plt.legend()
plt.show()
