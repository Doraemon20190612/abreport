import numpy as np
import pandas as pd
from scipy import stats
from .aa_bucket import md5_transform
from .indicator_define import ctr_by_group
from .indicator_define import ctr_summary


def diff_info(data: pd.DataFrame, sample_prop=1.0, random_seed=1):
    """

    :param data:
    :type data: pd.DataFrame
    :param sample_prop:
    :param random_seed:
    :return:
    """
    assert isinstance(data, pd.DataFrame)

    data_sample = data.sample(frac=sample_prop, random_state=random_seed)
    data_transform = md5_transform(data_sample)
    data_result = ctr_by_group(data_transform)

    p1 = float(data_result.iloc[0])
    group1 = data_result.index[0]
    p2 = float(data_result.iloc[1])
    group2 = data_result.index[1]
    diff = p1-p2
    data_info = pd.DataFrame({
        'group_name': [group1, group2],
        'indicator': [p1, p2],
        'diff': ['-', diff]
    })
    return data_info


def diff_ci(data: pd.DataFrame, sample_prop=1.0, critical_value=0.95, random_seed=1):
    """

    计算AA实验差值的置信区间
    :param data:输入字段为user_id,search_id,date,click_num,group的DataFrame
    :type data: pd.DataFrame
    :param sample_prop:抽样比例
    :param critical_value:置信区间界值,默认95%
    :param random_seed:随机数种子
    :return:置信区间
    """
    assert isinstance(data, pd.DataFrame)

    data_sample = data.sample(frac=sample_prop, random_state=random_seed)
    data_transform = md5_transform(data_sample)
    data_result = ctr_by_group(data_transform)

    p1 = float(data_result.iloc[0])
    n1 = len(data_transform[data_transform['group'] == data_result.index[0]])
    sp1 = (p1 * (1 - p1)) / n1
    p2 = float(data_result.iloc[1])
    n2 = len(data_transform[data_transform['group'] == data_result.index[1]])
    sp2 = (p2 * (1 - p2)) / n2
    diff = p1 - p2
    sp = np.sqrt(sp1 + sp2)
    ci = [diff - stats.norm(0, 1).ppf(1 - (1 - critical_value) / 2) * sp,
          diff + stats.norm(0, 1).ppf(1 - (1 - critical_value) / 2) * sp]
    return ci


def diff_proptest(data: pd.DataFrame, sample_prop=1.0, random_seed=1):
    """

    :param data:
    :type data: pd.DataFrame
    :param sample_prop:
    :param random_seed:
    :return:统计量u和P值p
    """
    assert isinstance(data, pd.DataFrame)

    data_sample = data.sample(frac=sample_prop, random_state=random_seed)
    data_transform = md5_transform(data_sample)
    data_result = ctr_by_group(data_transform)

    p1 = float(data_result.iloc[0])
    n1 = len(data_transform[data_transform['group'] == data_result.index[0]])
    p2 = float(data_result.iloc[1])
    n2 = len(data_transform[data_transform['group'] == data_result.index[1]])
    diff = p1 - p2
    pc = ctr_summary(data_sample)
    sp = np.sqrt(pc * (1 - pc) * (1 / n1 + 1 / n2))
    u = abs(diff) / sp
    p = (1 - stats.norm(0, 1).cdf(u)) * 2
    return u, p



