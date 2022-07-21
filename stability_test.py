def fn_stability_test(df, str_var):
    df_current = df[(df['measurementPeriodId'] >= 202001) and (df['measurementPeriodId'] <= 202001) ]

    min, max = min(df_current['measurementPeriodId'].min())


    pass
