import hashlib
import pandas as pd


def md5_transform(data: pd.DataFrame):
    """

    :type data: pd.DataFrame
    :param data: 输入字段为user_id,search_id,date,click_num
    :return: AA随机分组后的DataFrame,输出字段为user_id,search_id,date,click_num,group
    """
    assert isinstance(data, pd.DataFrame)

    def md5(user_id):
        md5id = hashlib.md5(user_id.encode(encoding='UTF-8')).hexdigest()
        if md5id[-1] in [str(i) for i in range(8)]:
            group_id = 'control1'
        else:
            group_id = 'control2'
        return group_id

    data['group'] = data['user_id'].apply(md5)

    return data
