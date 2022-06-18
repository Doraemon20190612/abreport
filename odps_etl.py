from odps import ODPS
from odps import options


def odps_sql(sql):
    """

    :param sql:
    :return: pd.DataFrame
    """

    options.sql.settings = {
        'odps.sql.submit.mode': 'script',
        'odps.sql.hive.compatible': 'true',
        'odps.sql.type.system.odps2': 'true',
        'odps.sql.python.version': 'cp37'
    }
    options.connect_timeout = 60
    options.read_timeout = 3600

    o = ODPS(
        'account',
        'password',
        'yw_search_dev',
        end_point='http://service.cn-shanghai.maxcompute.aliyun.com/api'
    )
    data = o.execute_sql(sql).open_reader(tunnel=True).to_pandas()
    return data
