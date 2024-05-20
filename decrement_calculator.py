import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os

data = pd.read_csv(
    os.path.join(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'data'),
        '3.csv'),
    names=('_', 'y'),
    usecols=['y'])

data['x'] = np.linspace(0, len(data), len(data), dtype=int)
data = data[550:3300]

smoothed_data = pd.DataFrame(
    sm.nonparametric.lowess(data.y, data.x, frac=0.035), columns=('x', 'y'))

maximums = (smoothed_data.iloc[argrelextrema(
    smoothed_data.y.values,
    np.greater_equal)]
    .reset_index(drop=True))

minimums = (smoothed_data.iloc[argrelextrema(
    smoothed_data.y.values,
    np.less_equal)]
    .reset_index(drop=True))

delta_array = np.array(
    [np.log(
        (maximums.y[0] - minimums.y[0]) / (maximums.y[n] - minimums.y[n])) / n
        for n in range(1, 4)])

log_dec = delta_array.mean()

plt.figure(figsize=(8, 6))
plt.plot(data.x, data.y, label='Raw signal', color='cyan', zorder=1)
plt.plot(smoothed_data.x, smoothed_data.y, label='Smoothed curve')
plt.scatter(minimums.x, minimums.y, color='red', label='Minimums')
plt.scatter(maximums.x, maximums.y, color='green', label='Maximums')
plt.legend()
plt.show()
