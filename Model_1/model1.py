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

R_T_MAX = 12
r_t_range = np.linspace(0, R_T_MAX, R_T_MAX * 100 + 1)
GAMMA = 1 / 7

def prepare_cases(cases, cutoff=5):
    new_cases = cases.diff()

    smoothed = new_cases.rolling(7,
                                 win_type='gaussian',
                                 min_periods=1,
                                 center=True).mean(std=2).round()

    idx_start = np.searchsorted(smoothed, cutoff)

    smoothed = smoothed.iloc[idx_start:]
    original = new_cases.loc[smoothed.index]

    return original, smoothed


def get_posteriors(sr, sigma=0.15):
    # (1) Calculate Lambda

    lam = sr[:-1].values * np.exp(GAMMA * (r_t_range[:, None] - 1))

    # (2) Calculate each day's likelihood
    likelihoods = pd.DataFrame(
        data=sps.poisson.pmf(sr[1:].values, lam),
        index=r_t_range,
        columns=sr.index[1:])

    # (3) Create the Gaussian Matrix
    process_matrix = sps.norm(loc=r_t_range,
                              scale=sigma
                              ).pdf(r_t_range[:, None])

    # (3a) Normalize all rows to sum to 1
    process_matrix /= process_matrix.sum(axis=0)

    # (4) Calculate the initial prior
    # prior0 = sps.gamma(a=4).pdf(r_t_range)
    prior0 = np.ones_like(r_t_range) / len(r_t_range)
    prior0 /= prior0.sum()

    # Create a DataFrame that will hold our posteriors for each day
    # Insert our prior as the first posterior.
    posteriors = pd.DataFrame(
        index=r_t_range,
        columns=sr.index,
        data={sr.index[0]: prior0}
    )

    # We said we'd keep track of the sum of the log of the probability
    # of the data for maximum likelihood calculation.
    log_likelihood = 0.0

    # (5) Iteratively apply Bayes' rule
    for previous_day, current_day in zip(sr.index[:-1], sr.index[1:]):
        # (5a) Calculate the new prior
        current_prior = process_matrix @ posteriors[previous_day]

        # (5b) Calculate the numerator of Bayes' Rule: P(k|R_t)P(R_t)
        numerator = likelihoods[current_day] * current_prior

        # (5c) Calcluate the denominator of Bayes' Rule P(k)
        denominator = np.sum(numerator)

        # Execute full Bayes' Rule
        posteriors[current_day] = numerator / denominator

        # Add to the running sum of log likelihoods
        log_likelihood += np.log(denominator)

    return posteriors, log_likelihood


def plot_rt(result, ax):
    ax.set_title(f"123")

    # Colors
    ABOVE = [1, 0, 0]
    MIDDLE = [1, 1, 1]
    BELOW = [0, 0, 0]
    cmap = ListedColormap(np.r_[
                              np.linspace(BELOW, MIDDLE, 25),
                              np.linspace(MIDDLE, ABOVE, 25)
                          ])
    color_mapped = lambda y: np.clip(y, .5, 1.5) - .5

    index = result.index.get_level_values('dateId')
    values = result.values

    # Plot dots and line
    ax.plot(index, values, c='k', zorder=1, alpha=.25)
    ax.scatter(index,
               values,
               s=40,
               lw=.5,
               c=cmap(color_mapped(values)),
               edgecolors='k', zorder=2)

    ax.axhline(1.0, c='k', lw=1, label='$R_t=1.0$', alpha=.25)

    # Formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}"))
    ax.yaxis.tick_right()
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.margins(0)


if __name__ == '__main__':

    sigmas = np.linspace(1 / 20, 1, 20)
    China_data = pd.read_csv(r"/Users/a1/Desktop/数据挖掘CS173/cs173_Project/DataCrawl/RawData/china_daily.csv",
                             encoding='gbk', usecols=['dateId', 'confirmedCount'], parse_dates=['dateId'],
                             index_col=['dateId'], squeeze=True).sort_index()

    original, smoothed = prepare_cases(China_data)

    result = {'posteriors': [], 'log_likelihoods': []}

    # Holds all posteriors with every given value of sigma

    # Holds the log likelihood across all k for each value of sigma

    for sigma in sigmas:
        posteriors, log_likelihood = get_posteriors(smoothed, sigma=sigma)
        result['posteriors'].append(posteriors)
        result['log_likelihoods'].append(log_likelihood)
    total_log_likelihoods = np.zeros_like(sigmas)

    # Loop through each state's results and add the log likelihoods to the running total.

    total_log_likelihoods += result['log_likelihoods']

    # Select the index with the largest log likelihood total
    max_likelihood_index = total_log_likelihoods.argmax()

    # Select the value that has the highest log likelihood
    sigma = sigmas[max_likelihood_index]

    # Plot it
    fig, ax = plt.subplots()
    ax.set_title(f"Maximum Likelihood value for $\sigma$ = {sigma:.2f}");
    ax.plot(sigmas, total_log_likelihoods)
    ax.axvline(sigma, color='k', linestyle=":")
    plt.show()

    ax = smoothed.plot(label='Smoothed',
                       legend=True)

    ax.get_figure().set_facecolor('w')

    posteriors, log_likelihood = get_posteriors(smoothed, sigma=sigma)

    # hdis = highest_density_interval(posteriors, p=.9)

    result = posteriors.idxmax().rename('ML')

    fig, ax = plt.subplots(figsize=(600 / 72, 400 / 72))
    plot_rt(result, ax)
    ax.set_title(f'Real-time $R_t$')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

    plt.show()
