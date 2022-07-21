import numpy as np
import pandas as pd
from scipy import stats
import scipy.stats as st

# def fn_bootstrap_year(df,product, dep1, dep2):
#
#     # calc per year
#     df['year'] = df.loc[:, 'measurementPeriodId'].apply(lambda x: str(x)[:-4])
#     df_years = {}
#
#     # separete the data by year
#     for x in df['year'].unique():
#         df_years[f"{x}"] = df[df['year'] == x]
#
#     # perform bootstrap by year
#     for year in np.sort(df.year.unique()):
#         int_year = int(year)
#         if int_year >= 2017:
#             ttest = stats.ttest_rel(df_years[year].loc[:, dep1], df_years[year].loc[:, dep2])
#             tvalue = float("{:.2f}".format(ttest.statistic))
#             low_CI_param, hight_CI_param = st.t.interval(alpha=0.975, df=len(df_years[year].loc[:, dep1]) - 1, loc=df_years[year].loc[:, dep1])
#             low_CI_ead, hight_CI_ead = st.t.interval(alpha=0.975, df=len(df_years[year].loc[:, dep2]) - 1,
#                                                          loc=df_years[year].loc[:, dep2])
#             dic = {'product': product, 'year': int(year), 'low_CI_param': low_CI_param,
#                    'hight_CI_param': hight_CI_param, 'low_CI_ead': low_CI_ead, 'low_CI_ead': low_CI_ead}
#
#             years = pd.DataFrame(dic, index=[0])
#
#
#     return years


def fn_bootstrap(df_rev,df_awl,df_loan,df_rop,df_bgl):

    ### low : % 2.5, hight : % 97.5

    lst_segment = ['rev', 'awl', 'loan', 'rop']
    ead_pred = 'Ead_Product'
    ead_real = 'Realized_EAD'

    df_conf_interval = pd.DataFrame(columns=['product', 't_value_param','low_CI_param', 'hight_CI_param',
                                           "t_value_ead", 'low_CI_EAD', 'hight_CI_EAD'])

    for seg in lst_segment:
        print(f' ******  progress for {seg} ***** ')
        if seg == 'rev':
            data = df_rev
            product = 'Rev.Credit_NZO'
            pred_param = 'Alpha'
            real_param = 'Alpha_Realized_Treated'
        elif seg == 'awl':
            product = 'AccountWithoutLimit'
            data = df_awl
            pred_param = 'Delta_Outstanding'
            real_param = 'DeltaOutstanding_Realized_Treated'
        elif seg == 'loan':
            product = 'Loan'
            data = df_loan
            pred_param = 'alphaLoan_Factor'
            real_param = 'AlphaLoanfactor_Realized'
        elif seg == 'rop':
            product = 'ROP_Flex_Credit'
            data = df_rop
            pred_param = 'Beta'
            real_param = 'Beta_Realized_Treated'
        else:
            product = 'Guarantees/Credit letters'
            data = df_bgl
            pred_param = 'Q'
            real_param = 'Q_Realized'

        t_value_param,p = stats.ttest_rel(data[pred_param], data[real_param])
        t_value_ead, p =  stats.ttest_rel(data[ead_pred], data[ead_real])

        low_CI_param, hight_CI_param = st.t.interval(alpha=0.975, df=len(data[pred_param])-1, loc=t_value_param)
        low_CI_ead, hight_CI_ead = st.t.interval(alpha=0.975, df=len(data[ead_pred])-1, loc=t_value_ead)

        dict = {'product': product,
                't_value_param':t_value_param,
                'low_CI_param': low_CI_param,
                'hight_CI_param': hight_CI_param,
                't_value_ead': t_value_ead,
                'low_CI_EAD': low_CI_ead,
                'hight_CI_EAD': hight_CI_ead}

        df_res = pd.DataFrame(dict, index=[0])
        df_conf_interval = df_conf_interval.append(df_res)

        # resultYear = fn_bootstrap_year(data, product, pred_param, real_param)
    return df_conf_interval