import numpy as np
import pyodbc
import pandas as pd

from cmlib.model_monitoring_metrics import JensenShannonDivergence as js
from cmlib.model_monitoring_metrics import Threshold

# General table set up
Product_table = '[RA_ABB_Custom].[dbo].[RSME_FinalModelPrediction_Monitoring2021_200912_202106_Product_RemediatedModel_202111]'
Facility_table = '[RA_ABB_Custom].[dbo].[RSME_FinalModelPrediction_Monitoring2021_200912_202106_Facility_RemediatedModel_202111]'

conn = pyodbc.connect('''DRIVER={SQL Server};Server=lbbbubble.eu.rabonet.com\ABB_PRD_01;
                          Database=RA_ABB_CUSTOM;Trusted_connection=yes;''')

# Select time periods
stmt = f""" select A.measurementperiodID as yearmonth
                     , floor(A.measurementperiodID/100) as year
                     , A.measurementperiodID - floor(A.measurementperiodID/100)*100 as month
                     , case when B.FacilityOutstanding < 30.96 then 'B01'
                         when B.FacilityOutstanding < 46341.4791 then 'B02'
                         when B.FacilityOutstanding < 92651.9982 then 'B03'
                         when B.FacilityOutstanding < 138962.5173 then 'B04'
                         when B.FacilityOutstanding < 185273.0364 then 'B05'
                         when B.FacilityOutstanding < 231583.5556 then 'B06'
                         when B.FacilityOutstanding < 277894.0747 then 'B07'
                         when B.FacilityOutstanding < 324204.5938 then 'B08'
                         when B.FacilityOutstanding < 370515.1129 then 'B09'
                         when B.FacilityOutstanding < 416825.632 then 'B10'
                         else 'B11' end as FacilityOutstanding_Bucket
                     , case when A.outstandingAmount < 13.12 then 'B01'
                         when A.outstandingAmount < 433.6037 then 'B02'
                         when A.outstandingAmount < 854.0873 then 'B03'
                         when A.outstandingAmount < 1274.571 then 'B04'
                         when A.outstandingAmount < 1695.0547 then 'B05'
                         when A.outstandingAmount < 2115.5383 then 'B06'
                         when A.outstandingAmount < 2536.022 then 'B07'
                         when A.outstandingAmount < 2956.5057 then 'B08'
                         when A.outstandingAmount < 3376.9893 then 'B09'
                         when A.outstandingAmount < 3797.473 then 'B10'
                         else 'B11' end as outstandingAmount_Bucket
                     , A.eadSegment_ as eadSegment
                     , case when A.eadProduct is null then 'B01'
                         when A.eadProduct < 2000 then 'B02'
                         when A.eadProduct < 2500 then 'B03'
                         when A.eadProduct < 3000 then 'B04'
                         when A.eadProduct < 3500 then 'B05'
                         when A.eadProduct < 4000 then 'B06'
                         when A.eadProduct < 5000 then 'B07'
                         when A.eadProduct < 6000 then 'B08'
                         when A.eadProduct < 7000 then 'B09'
                         when A.eadProduct < 8000 then 'B10'
                         when A.eadProduct < 9000 then 'B11'
                         else 'B12' end as eadProduct_
                    from (select *
                            , case when eadSegment = 'Revolving credit' then
                                case when outstandingAmount = 0 then 'Revolving credit zero outstanding' else 'Revolving credit nonzero outstanding' end
                                else eadSegment end as eadSegment_
                         from {Product_table} 
                         ) A
                    left join {Facility_table} B
                    on A.FacilityId=B.FacilityId and A.measurementperiodID=B.measurementperiodID
                    where A.defaultFlag = 0
                        and A.Isactive = 1
                        and A.CapitalBearing = 1
                        and B.Indicator_In_Scope = 1
                        and A.eadSegment_ = 'Account without Limit'
                        and (A.measurementperiodID <= 201612 or A.measurementperiodID >= 201901)
                    order by A.measurementperiodID
                    """
data = pd.read_sql_query(stmt, conn)

data_dev = data[(data['yearmonth'] <= 201612) & (data['yearmonth'] >= 201001)]
data_prev = data[(data['yearmonth'] <= 201912) & (data['yearmonth'] >= 201901)]
data_curr = data[(data['yearmonth'] <= 202012) & (data['yearmonth'] >= 202001)]

data_dev_FO = pd.crosstab(data_dev['FacilityOutstanding_Bucket'].fillna('missing'), data_dev['month'].fillna('missing'),
                          margins=False, dropna=False, normalize='columns')
data_prev_FO = pd.crosstab(data_prev['FacilityOutstanding_Bucket'].fillna('missing'),
                           data_prev['month'].fillna('missing'), margins=False, dropna=False, normalize='columns')
data_curr_FO = pd.crosstab(data_curr['FacilityOutstanding_Bucket'].fillna('missing'),
                           data_curr['month'].fillna('missing'), margins=False, dropna=False, normalize='columns')

for i in range(1, 13):
    globals()['outcome_' + str(i)] = js(
        actual_model=np.array(data_curr_FO.iloc[:, i - 1].to_numpy()),
        reference_model=np.array(data_dev_FO.iloc[:, i - 1].to_numpy()),
        bucket_names=["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B10", "B11"],
        thresholds={Threshold.GREEN: 0.001, Threshold.RED: 0.025},
    ).compare()

    globals()['outcome_teststat_' + str(i)] = globals()['outcome_' + str(i)].overall_divergence

Overallresults_FO_LT = (
outcome_teststat_1, outcome_teststat_2, outcome_teststat_3, outcome_teststat_4, outcome_teststat_5, outcome_teststat_6,
outcome_teststat_7, outcome_teststat_8, outcome_teststat_9, outcome_teststat_10, outcome_teststat_11,
outcome_teststat_12)

for i in range(1, 13):
    globals()['outcome_' + str(i)] = js(
        actual_model=np.array(data_curr_FO.iloc[:, i - 1].to_numpy()),
        reference_model=np.array(data_prev_FO.iloc[:, i - 1].to_numpy()),
        bucket_names=["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B10", "B11"],
        thresholds={Threshold.GREEN: 0.001, Threshold.RED: 0.025},
    ).compare()

    globals()['outcome_teststat_' + str(i)] = globals()['outcome_' + str(i)].overall_divergence

Overallresults_FO_ST = (
outcome_teststat_1, outcome_teststat_2, outcome_teststat_3, outcome_teststat_4, outcome_teststat_5, outcome_teststat_6,
outcome_teststat_7, outcome_teststat_8, outcome_teststat_9, outcome_teststat_10, outcome_teststat_11,
outcome_teststat_12)