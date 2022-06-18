# 容许区间计算
import numpy as np
import pandas as pd
from scipy import stats
from . indicator_define import ctr_summary


def normal_range(data, sample_prop=0.5, sample_freq=100, critical_value=0.95, method='norm'):
    """

    :type data: pd.DataFrame
    :param data: 输入字段为user_id,search_id,date,click_num的DataFrame
    :param sample_prop: bootstrap抽样比例
    :param sample_freq: bootstrap抽样次数
    :param critical_value: 容许区间界值,一般取95%
    :param method: {'norm','percentile'}
        default: 'norm'

        - `norm` : 正态分布法
        - `percentile` : 百分位数法

    :return: 容许区间
    """
    assert isinstance(data, pd.DataFrame)
    # 随机抽样后计算的指标列表
    bootstrap_lst = []
    for random_number in list(np.random.permutation(1000000))[:sample_freq]:
        data_sample = data.sample(frac=sample_prop, random_state=random_number)
        indicator = ctr_summary(data_sample)
        bootstrap_lst.append(indicator)
    # 计算容许区间
    if method == 'norm':
        ti = [np.mean(bootstrap_lst) - stats.norm(0, 1).ppf(1 - (1 - critical_value) / 2) * np.std(bootstrap_lst),
              np.mean(bootstrap_lst) + stats.norm(0, 1).ppf(1 - (1 - critical_value) / 2) * np.std(bootstrap_lst)]
    elif method == 'percentile':
        percentile_range = [
            i for i in bootstrap_lst if np.percentile(bootstrap_lst, ((1 - critical_value) * 100) / 2) <= i <= np.percentile(bootstrap_lst, 100 - (((1 - critical_value) * 100) / 2))
        ]
        ti = [min(percentile_range), max(percentile_range)]
    else:
        raise ValueError('model error')
    return ti


