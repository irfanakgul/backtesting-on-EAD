import numpy as np
import pandas as pd
from sql_query import fn_table, fn_table_mkt_awl,fn_table_mkt_loan,\
    fn_table_mkt_rop,fn_table_mkt_bglc, fn_table_mkt_rev, fn_table_mkt_rev_nzo, \
    fn_table_stb_rop



from ttest import t_test
from disc_power_test import gini_calc, fn_disc_power
from bootstrap import fn_bootstrap
from mann_kendal_test import fn_mann_kendal
from stability_test import fn_stability_test

################################### configration of backtesting ############################################

#
sql_part_ttest = False
sql_part_mkt = False
sql_part_stb =True

ttest_bool = False
bootstrap_bool = False
disc_bool = False
mkt_bool = False
stb_bool = True


############################### SQL - data loading ##################################################
##### sql queries for ttest and disc.power #####
if sql_part_ttest==True:
    df_rev,df_awl,df_loan,df_rop,df_bgl = fn_table()

##### sql queries for mann-kendall test #####
if sql_part_mkt ==True:
    df_awl_mkt = fn_table_mkt_awl()
    df_loan_mkt = fn_table_mkt_loan()
    df_rev_mkt = fn_table_mkt_rev()
    df_rev_nzo_mkt = fn_table_mkt_rev_nzo()
    df_rop_mkt = fn_table_mkt_rop()
    df_bglc_mkt = fn_table_mkt_bglc()

##### sql queries for Stability tests -JSD -PSI  #####
if sql_part_stb == True:
    df_rop_stb = fn_table_stb_rop()


######################################   Tests Performing   ################################################
#### implement T-TEST ######
if ttest_bool == True:
    print("*** Calculated t-test for all segments at PRODUCT LEVEL on EAD MODEL")

    rev_param = t_test(df_rev,'revCredit_NZO','Alpha','Alpha_Realized_Treated')
    rev_ead = t_test(df_rev,'revCredit_NZO','Ead_Product','Realized_EAD')

    awl_param = t_test(df_awl,'AccountWithoutLimit','Delta_Outstanding','DeltaOutstanding_Realized_Treated')
    awl_ead = t_test(df_awl,'AccountWithoutLimit','Ead_Product','Realized_EAD')

    loan_param = t_test(df_loan,'Loan','alphaLoan_Factor','AlphaLoanfactor_Realized')
    loan_ead = t_test(df_loan,'Loan','Ead_Product','Realized_EAD')

    rop_param = t_test(df_rop,'ROP','Beta','Beta_Realized_Treated')
    rop_ead = t_test(df_rop,'ROP','Ead_Product','Realized_EAD')

    bgl_param = t_test(df_bgl,'BGL','Q','Q_Realized')
    bgl_ead = t_test(df_bgl,'BGL','Ead_Product','Realized_EAD')

# # implement des. Power test (loss capture ratio and spearman rank correlation)
if disc_bool==True:
    df_disc_power_results = fn_disc_power(df_rev,df_awl,df_loan,df_rop,df_bgl)

    print("*** Calculated LossCaptureRatio for all segments at PRODUCT LEVEL on EAD MODEL")

# implement bootstrapped t-test > low: 0.025, hight: 0.975
if bootstrap_bool == True:
    output_bootstrap = fn_bootstrap(df_rev,df_awl,df_loan,df_rop,df_bgl)

# implement Mann-Kendall test for each product
if mkt_bool == True:
    awl_FO = fn_mann_kendal(df_awl_mkt,'Facility_Outstanding',12)
    awl_OA = fn_mann_kendal(df_awl_mkt, 'Outstanding_Amount', 12)
    loan_EXP = fn_mann_kendal(df_loan_mkt, 'Exposure', 12)
    rop_LA = fn_mann_kendal(df_rop_mkt, 'Limit_Amount', 12)
    bglc_LA = fn_mann_kendal(df_bglc_mkt, 'Limit_Amount', 12)
    rev_nzo_OA = fn_mann_kendal(df_rev_nzo_mkt, 'Outstanding_Amount', 12)
    rev_nzo_UTI = fn_mann_kendal(df_rev_nzo_mkt, 'Utilisation_Uncapped', 12)
    rev_LA = fn_mann_kendal(df_rev_mkt, 'Limit_Amount', 12)

    df_all_product = pd.concat([awl_FO, awl_OA,loan_EXP,rop_LA,bglc_LA,rev_nzo_OA,rev_nzo_UTI,rev_LA])


# implement Stability tests for each product - JSD and PSI
if stb_bool == True:
    rop_LA_stb = fn_stability_test(df_rop_stb, 'Limit_Amount')




exit()