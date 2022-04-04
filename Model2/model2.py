import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings('ignore')

plt.style.use("seaborn")
plt.rc('font', family='SimHei', size=13)  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 先读取数据
China_data = pd.read_csv(r"/Users/a1/Desktop/数据挖掘CS173/cs173_Project/DataCrawl/RawData/china_daily.csv", encoding='gbk')


def logistic_increase_func(t, a, b, K):
    exp_value = np.exp(-a * (t - b))
    return K / (1 + exp_value)


def exponential(t, a, b, c):
    return a * np.exp(b * t) + c


def fit(x, y):
    recentdbltime = float('NaN')
    logisticworked = False
    exponentialworked = False
    fig, axes = plt.subplots(1, 2)

    logistic_increase = logistic_increase_func
    lpopt, lpcov = curve_fit(logistic_increase, x, y, maxfev=10000)
    # the error of fit

    error = np.sqrt(np.diag(lpcov))

    # for logistic curve at half maximum, slope = growth rate/2. so doubling time = ln(2) / (growth rate/2)

    doubletime_l = np.log(2) / (lpopt[1] / 2)
    # standard error
    ldoubletimeerror = 1.96 * doubletime_l * np.abs(error[1] / lpopt[1])
    # calculate R^2
    residuals_1 = y - logistic_increase(x, *lpopt)

    ss_res = np.sum(residuals_1 ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    logisticr2 = 1 - (ss_res / ss_tot)

    future_t = np.array([i + 1 for i in range(0, 3000)])
    axes[0].scatter(t, China_y, label="实际确诊患者数量")
    axes[0].plot(future_t, logistic_increase(future_t, *lpopt), 'b--', label='预测患者数量曲线')
    plt.xlabel('time')
    plt.ylabel('患者数量')
    print('\n** Based on Logistic Fit**\n')
    print('\tR^2:', logisticr2)
    print('\tDoubling Time (during middle of growth): ', round(doubletime_l, 2), '(±',
          round(ldoubletimeerror, 2), ') days')
    logisticworked = True

    epopt, epcov = curve_fit(exponential, x, y, maxfev=10000)
    eerror = np.sqrt(np.diag(epcov))

    # for exponential curve, slope = growth rate. so doubling time = ln(2) / growth rate
    edoubletime = np.log(2) / epopt[1]
    # standard error
    edoubletimeerror = 1.96 * edoubletime * np.abs(eerror[1] / epopt[1])

    # calculate R^2
    residuals_2 = y - exponential(x, *epopt)
    ss_res = np.sum(residuals_2 ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    expr2 = 1 - (ss_res / ss_tot)

    axes[1].scatter(t, China_y, label="实际确诊患者数量")
    axes[1].plot(future_t, exponential(future_t, *epopt), 'r--', label='预测患者数量曲线')
    plt.xlabel('time')
    plt.ylabel('患者数量')
    print('\n** Based on Exponential Fit **\n')
    print('\tR^2:', expr2)
    print('\tDoubling Time (represents overall growth): ', round(edoubletime, 2), '(±',
          round(edoubletimeerror, 2), ') days')
    exponentialworked = True

    plt.show()

    return [residuals_1, residuals_2]


if __name__ == '__main__':

    date = China_data['dateId'].values
    x_length = len(China_data['dateId'].values)
    t = np.array([i + 1 for i in range(x_length)])
    China_y = China_data['confirmedCount'].values

    if China_y[-1] > China_y[-8]:
        print('\n** Based on Most Recent Week of Data **\n')
        print('\tConfirmed cases on', date[t[-1] - 1], '\t', China_y[-1])
        print('\tConfirmed cases on', date[t[-8] - 1], '\t', China_y[-8])
        ratio = China_y[-1] / China_y[-8]
        print('\tRatio:', round(ratio, 2))
        print('\tWeekly increase:', round(100 * (ratio - 1), 1), '%')
        dailypercentchange = round(100 * (pow(ratio, 1 / 7) - 1), 1)
        print('\tDaily increase:', dailypercentchange, '% per day')
        recentdbltime = round(7 * np.log(2) / np.log(ratio), 1)
        print('\tDoubling Time (represents recent growth):', recentdbltime, 'days')

    resid = fit(t, China_y)
    # 在最近的地方可以突然误差率大，无法应付突发情况
    # todo: delete the outliers?

    fig, axes = plt.subplots(1, 2)
    axes[0].scatter(China_y, resid[0])
    axes[1].scatter(China_y,resid[1])
    plt.show()
