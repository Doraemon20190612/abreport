# 指标自定义计算模块
import numpy as np
import pandas as pd


def ctr_by_group(data: pd.DataFrame):
    """

    输入字段为user_id,group,search_id,date,click_num的DataFrame
    输出index为group,value为ctr的DataFrame
    :type data: pd.DataFrame
    """
    assert isinstance(data, pd.DataFrame)

    data['click'] = np.where(data['click_num'] > 0, data['search_id'], 'NA')
    data_result = data.groupby('group').agg({'click': lambda x: len(x.dropna().unique()),
                                             'search_id': lambda x: len(x.dropna().unique())})
    data_result['ctr'] = data_result['click'] / data_result['search_id']
    return data_result[['ctr']]


def ctr_summary(data: pd.DataFrame):
    """

    输入字段为user_id,q_search_id,date,click_num的DataFrame
    输出ctr的float类型
    :type data: pd.DataFrame
    """
    assert isinstance(data, pd.DataFrame)

    data_click = len(data[data['click_num']>0])
    data_total = len(data)

    return data_click/data_total
