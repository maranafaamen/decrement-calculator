import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os


# Импорт данных с осциллографа

filename = '3.csv'
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', filename)
data = pd.read_csv(filepath, usecols=['y'], names=['_', 'y'])

# "Обрезка" лишних данных

data = data.iloc[550:3300] 

# Сглаживание кривой методом lowess (local weighted smoothing)

smoothed_data = pd.DataFrame(
    sm.nonparametric.lowess(data.y, data.index, frac=0.035),
    columns=('x', 'y')
)

# Поиск экстремумов

maximums = smoothed_data.iloc[argrelextrema(smoothed_data.y.values, np.greater_equal)]
minimums = smoothed_data.iloc[argrelextrema(smoothed_data.y.values, np.less_equal)]

# Расчет логарифмического декремента

delta_array = [np.log((maximums.y.iloc[0] - minimums.y.iloc[0]) / 
                     (maximums.y.iloc[n] - minimums.y.iloc[n])) / n for n in range(1, 4)]
log_dec = np.mean(delta_array)

# Визуализация

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(data.index, data.y, label='Raw signal', color='cyan', zorder=1)
ax.plot(smoothed_data.x, smoothed_data.y, label='Smoothed curve')
ax.scatter(maximums.x, maximums.y, color='red', label='Maximums')
ax.scatter(minimums.x, minimums.y, color='green', label='Minimums')
ax.text(0.6, 0.1, f'Logarithmic decrement = {log_dec:.2f}', 
        transform=ax.transAxes, fontsize=12,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
ax.legend()
ax.set_title('Signal analysis')
ax.set_xlabel('Time, ms')
ax.set_ylabel('Amplitude, V')
plt.tight_layout()
plt.show()

print(f'Result: {log_dec:.2f}')