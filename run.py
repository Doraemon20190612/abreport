from odps_etl import odps_sql
from indicator_define import ctr_summary
from indicator_volatility import normal_range
from aa_test import diff_proptest as diff_proptest_aa
from aa_test import diff_ci as diff_ci_aa
from sample_estimate import sample_size
from sample_estimate import testtime_estimate
from report_pdf import pretest_pdf
from ab_test import diff_info as diff_info_ab
from ab_test import diff_proptest as diff_proptest_ab
from ab_test import diff_ci as diff_ci_ab
from report_pdf import posttest_pdf


aa_start_date = '2021-09-08'
aa_end_date = '2021-09-14'
ab_start_date = '2021-10-04'
ab_end_date = '2021-10-10'


sql_aa = '''
select 
    u_login_id as user_id,
    q_search_id as search_id,
    t_date as date,
    sum(is_search_result_click)+sum(is_search_result_click_searchid)+sum(is_search_result_addcart_searchid) as click_num 
from yw_search.odl_yc_spider
where 
    ds between '%s' and '%s'
    and u_login_id is not null 
    and u_login_id not in ('',' ')
group by u_login_id,q_search_id,t_date
'''%(aa_start_date,aa_end_date)
sql_ab = '''
select 
    u_login_id as user_id,
    u_exp_layer3_name_app as group,
    q_search_id as search_id,
    t_date as date,
    sum(is_search_result_click)+sum(is_search_result_click_searchid)+sum(is_search_result_addcart_searchid) as click_num
from yw_search.odl_yc_spider
where 
    ds between '%s' and '%s'
    and u_login_id is not null 
    and u_login_id not in ('',' ')
group by u_login_id,u_exp_layer3_name_app,q_search_id,t_date
'''%(ab_start_date,ab_end_date)

data_aa = odps_sql(sql_aa)
data_ab = odps_sql(sql_ab)

aa_ctr = ctr_summary(data_aa)

indicator_vol1_s2 = normal_range(data_aa,sample_prop=0.2,sample_freq=100,method='norm')
indicator_vol2_s2 = normal_range(data_aa,sample_prop=0.2,sample_freq=100,method='percentile')

aa_diff_stat,aa_diff_p = diff_proptest_aa(data_aa)
aa_diff_ci95 = diff_ci_aa(data_aa)

min_n_base = sample_size(data_aa,aa_diff_ci95,diff_range=None)
min_n_1 = sample_size(data_aa,aa_diff_ci95,diff_range=0.01)
min_n_2 = sample_size(data_aa,aa_diff_ci95,diff_range=0.02)
min_n_3 = sample_size(data_aa,aa_diff_ci95,diff_range=0.03)

test_days_base = testtime_estimate(data_aa,min_n_base,prop=0.1)
test_days_1 = testtime_estimate(data_aa,min_n_1,prop=0.1)
test_days_2 = testtime_estimate(data_aa,min_n_2,prop=0.1)
test_days_3 = testtime_estimate(data_aa,min_n_3,prop=0.1)

pretest_pdf(aa_start_date, aa_end_date, aa_ctr, indicator_vol1_s2, indicator_vol2_s2,
        aa_diff_stat, aa_diff_p, aa_diff_ci95,
        min_n_base, min_n_1, min_n_2, min_n_3, test_days_base, test_days_1, test_days_2, test_days_3)

data_bb = data_ab[data_ab['group'].isin(['rerank1','baseline_strategy'])]

ab_groupname1 = diff_info_ab(data_bb)['group_name'][0]
ab_groupname2 = diff_info_ab(data_bb)['group_name'][1]
ab_diff = diff_info_ab(data_bb)['diff'][1]
ab_diff_stat,ab_diff_p = diff_proptest_ab(data_bb)
ab_diff_ci = diff_ci_ab(data_bb)

posttest_pdf(ab_start_date, ab_end_date, ab_groupname1, ab_groupname2,
        ab_diff, ab_diff_stat, ab_diff_p, ab_diff_ci)

