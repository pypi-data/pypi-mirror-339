"""
A comprehensive example that shows the whole workflow of
1) Loading data
2) Defining the model structure for a joint distribution
3) Estimating the parameter values of the model ("Fitting")
4) Computing a 3D environmental contour

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from virocon import (
    GlobalHierarchicalModel,
    LogNormalDistribution,
    ExponentiatedWeibullDistribution,
    DependenceFunction,
    WidthOfIntervalSlicer,
    HighestDensityContour,
    plot_marginal_quantiles,
    plot_dependence_functions,
)


# Load sea state measurements.
data = pd.read_csv("datasets/coastDat2_oneyear.csv", sep=";", skipinitialspace=True)
data.index = pd.to_datetime(data.pop(data.columns[0]), format="%Y-%m-%d-%H")


# Define the structure of the joint model that we will use to describe
# the the environmental data. To define a joint model, we define the
# univariate parametric distributions and the dependence structure.
# The dependence structure is defined using parametric functions.


# A 3-parameter power function, which will be used as a dependence function.
def _power3(x, a, b, c):
    return a + b * x**c


# A 3-parameter exponential function, which will be used as a dependence function.
def _exp3(x, a, b, c):
    return a + b * np.exp(c * x)


# A 3- parameter alpha function, which will be used as a dependence function.
def _alpha3(x, a, b, c, d_of_x):
    return (a + b * x**c) / 2.0445 ** (1 / d_of_x(x))


# A 4- parameter logistic function, which will be used as a dependence function.
def _logistics4(x, a=1, b=1, c=-1, d=1):
    return a + b / (1 + np.exp(c * (x - d)))


# Lower and upper interval boundaries for the three parameter values.
bounds = [(0, None), (0, None), (None, None)]
logistics_bounds = [(0, None), (0, None), (None, 0), (0, None)]

power3 = DependenceFunction(_power3, bounds, latex="$a + b * x^c$")
exp3 = DependenceFunction(_exp3, bounds, latex="$a + b * \exp(c * x)$")
logistics4 = DependenceFunction(
    _logistics4,
    logistics_bounds,
    weights=lambda x, y: y,
    latex="$a + b / (1 + \exp[c * (x -d)])$",
)
alpha3 = DependenceFunction(
    _alpha3,
    bounds,
    d_of_x=logistics4,
    weights=lambda x, y: y,
    latex="$(a + b * x^c) / 2.0445^{1 / F()}$",
)

# Define the structure of the joint distribution.

# Wind speed.
dist_description_0 = {
    "distribution": ExponentiatedWeibullDistribution(),
    "intervals": WidthOfIntervalSlicer(2, min_n_points=50),
}
# Wave height.
dist_description_1 = {
    "distribution": ExponentiatedWeibullDistribution(f_delta=5),
    "intervals": WidthOfIntervalSlicer(0.5),
    "conditional_on": 0,
    "parameters": {
        "alpha": alpha3,
        "beta": logistics4,
    },
}
# Zero-up-crossing period.
dist_description_2 = {
    "distribution": LogNormalDistribution(),
    "conditional_on": 1,
    "parameters": {"mu": power3, "sigma": exp3},
}


model = GlobalHierarchicalModel(
    [dist_description_0, dist_description_1, dist_description_2]
)

# Define a dictionary that describes the model.
semantics = {
    "names": ["Wind speed", "Significant wave height", "Zero-up-crossing period"],
    "symbols": ["V", "H_s", "T_z"],
    "units": ["m/s", "m", "s"],
}

# Fit the model to the data (estimate the model's parameter values).
model.fit(data)

# Print the estimated parameter values.
print(model)

# Create plots to inspect the model's goodness-of-fit.
fig1, axs = plt.subplots(1, 3, figsize=[20, 7], dpi=300)
plot_marginal_quantiles(model, data, semantics, axes=axs)
fig2, axs = plt.subplots(1, 4, figsize=[20, 7], dpi=300)
plot_dependence_functions(model, semantics, axes=axs)

# Calculate 3D Contour.
state_duration = 1  # hours
return_period = 20  # years
alpha = state_duration / (return_period * 365.25 * 24)
HDC = HighestDensityContour(model, alpha, limits=[(0, 50), (0, 25), (0, 25)])

# randomly select only 5% of the contour's points to increase performance
rng = np.random.default_rng(42)
n_contour_points = len(HDC.coordinates)
random_points = rng.choice(
    n_contour_points, int(0.05 * n_contour_points), replace=False
)

Xs = HDC.coordinates[random_points, 0]
Ys = HDC.coordinates[random_points, 1]
Zs = HDC.coordinates[random_points, 2]

fig = plt.figure(dpi=300, figsize=[15, 7])
ax = fig.add_subplot(111, projection="3d")
ax.scatter(Xs, Ys, Zs, c="#004488")
ax.set_xlabel("Wind speed (m/s)")
ax.set_ylabel("Significant wave height (m)")
ax.set_zlabel("Zero-up-crossing period (s)")
