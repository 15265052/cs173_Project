import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date
from matplotlib import dates as mdates
from matplotlib import ticker
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from scipy import stats as sps
from scipy.interpolate import interp1d
from IPython.display import clear_output
import warnings

warnings.filterwarnings('ignore')

plt.style.use("seaborn")
plt.rc('font', family='SimHei', size=13)  # 显示中文
plt.rcParams['axes.unicode_minus'] = False

def prepare_cases(cases,cutoff=5):
    # for continuous
    smoothed = cases.rolling(7,
                             win_type='gaussian',
                             min_periods=1,
                             center=True).mean(std=2).round()

    smoothed=np.array(smoothed)
    new_smoothed=[]
    for i in smoothed:
        new_smoothed.append(i[0])
    smoothed=new_smoothed
    # for smooth
    idx_start = np.searchsorted(smoothed, cutoff)

    smoothed = smoothed[idx_start:]
    smoothed=pd.DataFrame(smoothed)
    original = cases.loc[smoothed.index]

    return original, smoothed


# k = np.arange(0, 70)[:, None]
# # Different values of Lambda
# lambdas = [10, 20, 30, 40]
# # Evaluated the Probability Mass Function (remember: poisson is discrete)
# y = sps.poisson.pmf(k, lambdas)
#
# R_T_MAX = 12
# r_t_range = np.linspace(0, R_T_MAX, R_T_MAX * 100 + 1)
# GAMMA = 1 / 7
# lam = k[:-1] * np.exp(GAMMA * (r_t_range[:, None] - 1))
# likelihood_r_t = sps.poisson.pmf(k[1:], lam)
# likelihood_r_t /= np.sum(likelihood_r_t, axis=0)
#
# posteriors = likelihood_r_t.cumprod(axis=1)
# posteriors = posteriors / np.sum(posteriors, axis=0)
#
# columns = pd.Index(range(1, posteriors.shape[1] + 1), name='Day')
# posteriors = pd.DataFrame(
#     data=posteriors,
#     index=r_t_range,
#     columns=columns)
#
# most_likely_values = posteriors.idxmax(axis=0)

if __name__ == '__main__':
    China_data = pd.read_csv(r"/Users/a1/Desktop/数据挖掘CS173/cs173_Project/DataCrawl/RawData/china_daily.csv",
                             encoding='gbk')
    date = China_data['dateId'].values
    x_length = len(China_data['dateId'].values)
    t = np.array([i + 1 for i in range(x_length)])
    China_y =pd.DataFrame(China_data['confirmedIncr'].values)
    print(China_y)
    original, smoothed = prepare_cases(China_y)

    original.plot(title=f" New Cases per Day",
                  c='k',
                  linestyle=':',
                  alpha=.5,
                  label='Actual',
                  legend=True,
                  figsize=(500 / 72, 300 / 72))

    ax = smoothed.plot(label='Smoothed',
                       legend=True)

    ax.get_figure().set_facecolor('w')
    plt.show()