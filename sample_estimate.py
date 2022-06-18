import numpy as np
import pandas as pd
from scipy import stats
from .indicator_define import ctr_summary


def sample_size(data: pd.DataFrame, diff_ci, diff_range=None, alpha=0.05, power=0.8):
    """

    :param data: AA实验数据(历史数据)
    :type data: pd.DataFrame
    :param diff_ci: AA实验差值的置信区间
    :param diff_range:指标预期提升差值
    :param alpha: 检验水准
    :param power: 检验功效
    :return: 最小样本量
    """
    assert isinstance(data, pd.DataFrame)

    if diff_range is None:
        diff = max([abs(i) for i in diff_ci])
    else:
        diff = diff_range

    p_control = ctr_summary(data)
    p_test = p_control + diff
    var_pooled = p_test * (1 - p_test) + p_control * (1 - p_control)
    z_alpha = stats.norm(0, 1).ppf(1 - alpha / 2)
    z_power = stats.norm(0, 1).ppf(power)
    n = np.square(z_alpha+z_power) / (np.square(diff) / var_pooled)
    return n


def testtime_estimate(data: pd.DataFrame, min_n, prop=0.1):
    """

    :param data: AA实验数据(历史数据)
    :type data: pd.DataFrame
    :param min_n: 最小样本量
    :param prop: 实验组流量比例
    :return: 预估最小实验天数
    """
    data_result = data.groupby('date').agg({'user_id': lambda x:len(x.dropna().unique())})
    days = min_n / (data_result['user_id'].mean() * prop)
    return days
