# fn_lossCapture

import numpy as np
import pandas as pd


def gini_calc(df, predictor, target):

    """
    :param predictor: Predictor variable (a vector)
    :param target: Target variable (Loss Given Loss,
            Loss Given Default, realized EAD, ...) (a vector)
    :GOAL: This function calculates loss capture ratio
    :return:Loss capture ratio (1 is perferct, 0 - is no predictive power
    """

    predictor = df[predictor]
    target = df[target]

    my_data = pd.DataFrame()

    my_data["Target"] = target
    my_data["Predictor"] = predictor

    # Removing missing data
    my_data.dropna(inplace=True)
    my_data.reset_index(drop=True, inplace=True)

    # Sorting and calculating cummulative number of observations
    grouped = my_data.groupby("Predictor", as_index=False).mean()
    cnt = my_data.groupby("Predictor", as_index=True).size()
    cnt = cnt.reset_index(level=0)
    cnt.rename({0:'size'},axis=1, inplace=True)

    avg_target = cnt.merge(grouped, on='Predictor')
    avg_target["numel_Target"] = cnt["size"]
    avg_target.rename(columns={"size": "GroupCount", "Target": "mean_Target"}, inplace=True)

    my_data_predict = my_data.merge(avg_target, how='outer')
    my_data_predict.sort_values(by=['Predictor'], inplace=True)
    my_data_predict.drop(['GroupCount', 'numel_Target', 'Target'], axis=1, inplace=True)
    my_data_predict.reset_index(drop=True, inplace=True)
    my_data_predict.rename({'mean_Target': 'Target'}, inplace=True, axis=1)

    my_data_ideal = my_data.sort_values(by=['Target'], ascending=False).reset_index(drop=True)

    cum_count = [i / len(my_data.Target) for i in range(1, len(my_data.Target) + 1)]

    my_data_ideal["CumCount"] = pd.Series(cum_count)

    # for MyDataPredict
    my_data_predict.sort_values(by="Predictor", ascending=False, inplace=True, ignore_index=True)

    cum_count = [i / len(my_data.Predictor) for i in range(1, len(my_data.Predictor) + 1)]

    cum_count = pd.Series(cum_count, name="CumCount")

    my_data_predict["CumCount"] = cum_count

    my_data_ideal['CumSumTarget'] = np.cumsum(my_data_ideal.Target).apply(lambda x: x / np.sum(my_data_ideal.Target))
    my_data_predict["CumSumTarget"] = np.cumsum(my_data_predict.Target).apply(lambda x: x / np.sum(my_data_predict.Target))

    for i in np.arange(len(my_data.Target)):
        if i == 0:

            numenator = 0.5 * my_data_predict.CumSumTarget[i] * my_data_predict.CumCount[i]
            denom = 0.5 * my_data_ideal.CumSumTarget[i] * my_data_ideal.CumCount[i]

        else:
            numenator = numenator + 0.5 * (my_data_predict.CumSumTarget[i] + my_data_predict.CumSumTarget[i - 1]) * (
                        my_data_predict.CumCount[i] - my_data_predict.CumCount[i - 1])
            denom = denom + 0.5 * (my_data_ideal.CumSumTarget[i] + my_data_ideal.CumSumTarget[i - 1]) * (
                        my_data_ideal.CumCount[i] - my_data_ideal.CumCount[i - 1])

    num_gini_score = (numenator - 0.5) / (denom - 0.5)
    num_gini_score = float("{:.2f}".format(num_gini_score))
    # print(f'gini score = {num_gini_score}')
    return num_gini_score

def spearman_calc(df, predictor, target):
    predictor = df[predictor]
    target = df[target]

    spearman_value = predictor.corr(target,  method='spearman')
    return spearman_value



def fn_disc_power(df_rev,df_awl,df_loan,df_rop,df_bgl):
    lst_segment = ['rev','awl','loan','rop','bgl']
    ead_pred = 'Ead_Product'
    ead_real = 'Realized_EAD'

    df_gini_scores = pd.DataFrame(columns=['product', 'param_lcr','param_spearman', 'ead_lcr', 'ead_spearman'])

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

        dict = {'product':product,
                'param_lcr':gini_calc(data, pred_param,real_param),
                'param_spearman':spearman_calc(data,pred_param,real_param),
                'ead_lcr':gini_calc(data, ead_pred,ead_real),
                'ead_spearman':spearman_calc(data,ead_pred,ead_real)}

        df_res = pd.DataFrame(dict, index=[0])
        df_gini_scores = df_gini_scores.append(df_res)

    return df_gini_scores