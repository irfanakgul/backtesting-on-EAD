
import scipy.stats as stats
import pandas as pd
import numpy as np



def t_test(df, product, dep1, dep2):
    # entire of data
    ttest = stats.ttest_rel(df[dep1], df[dep2])
    pvalue = float("{:.2f}".format(ttest.pvalue))

    if pvalue == 0.0:
        statu = 'red-Conservative'
    elif pvalue > 0.0 and ttest.pvalue < 0.05:
        statu = 'yellow-optimistic'
    else:
        statu = 'green - Accurate'

    dic = {'product': product, 'year': 'general', 'obs': len(df.measurementPeriodId), 'pred_AVG': df[dep1].mean(),
           'real_AVG': df[dep2].mean(), 'p_value': pvalue, 'status': statu}
    result_all = pd.DataFrame(dic, index=[0])

    ## show normal dist.
    # import pylab
    # stats.probplot(df[dep1], dist='norm', plot=pylab)
    # pylab.show()

    # calc per year
    df['year'] = df.loc[:, 'measurementPeriodId'].apply(lambda x: str(x)[:-4])
    df_years = {}

    # separete the data by year
    for x in df['year'].unique():
        df_years[f"{x}"] = df[df['year'] == x]

    # perform ttest by year
    for year in np.sort(df.year.unique()):
        int_year = int(year)
        if int_year >= 2017:

            ttest = stats.ttest_rel(df_years[year].loc[:, dep1], df_years[year].loc[:, dep2])
            pvalue = float("{:.2f}".format(ttest.pvalue))
            print('t value p value : ', ttest[:])

            if pvalue == 0.0:
                statu = 'red-Conservative'
            elif pvalue > 0.0 and ttest.pvalue < 0.05:
                statu = 'yellow-optimistic'
            else:
                statu = 'green-Accurate'

            dic = {'product': product, 'year': int(year), 'obs': len(df_years[year].measurementPeriodId),
                   'pred_AVG': df_years[year][dep1].mean(), 'real_AVG': df_years[year][dep2].mean(), 'p_value': pvalue,
                   'status': statu}

            result = pd.DataFrame(dic, index=[0])
            result_all = result_all.append(result)



    return result_all