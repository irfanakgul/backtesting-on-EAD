import numpy as np
import pandas as pd
import py
import pyodbc
from rsmelib.load.data import Data
from rsmelib.load.data import read_sql_file
from rsmelib.configobj_plus import ConfigObjPlus


def sql_query_rev():

    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mon.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_rev = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded data > rev')
    return df_rev

def sql_query_awl():

    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mon_awl.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_awl = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded data > awl')
    return df_awl


def sql_query_loan():

    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mon_loan.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_loan = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded data > loan')
    return df_loan

def sql_query_rop():

    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mon_rop.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_rop= Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded data > rop')
    return df_rop

def sql_query_bgl():

    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mon_bgl.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_bgl = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded data > bglc')
    return df_bgl

def fn_table():

    df_rev = sql_query_rev()
    df_awl =sql_query_awl()
    df_loan =sql_query_loan()
    df_rop= sql_query_rop()
    df_bgl=sql_query_bgl()

    return df_rev,df_awl,df_loan,df_rop,df_bgl

def fn_table_mkt_awl():
    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mkt_awl.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_awl = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded mkt data > awl')
    return df_awl

def fn_table_mkt_loan():
    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mkt_loan.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_loan = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded mkt data > loan')
    return df_loan

def fn_table_mkt_rev_nzo():
    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mkt_rev_NZO.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_rev_nzo = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded mkt data > RevolvingCreditNZO')
    return df_rev_nzo

def fn_table_mkt_rev():
    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mkt_rev.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_rev = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded mkt data > RevolvingCredit')
    return df_rev

def fn_table_mkt_rop():
    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mkt_rop.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_rop = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded mkt data > ROP')
    return df_rop

def fn_table_mkt_bglc():
    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_mkt_bglc.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_bglc = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded mkt data > BGLC')
    return df_bglc


#### loading data for stability tests by products
def fn_table_stb_rop():
    print('$$$ ROP data is loading $$$$')
    query = read_sql_file(r'C:\Users\AkgulI\PycharmProjects\monitoring/query_stb_rop.sql')
    config = ConfigObjPlus(r'C:\Users\AkgulI\PycharmProjects\monitoring/config_sql.ini', unrepr=True)
    conn_dict = config['SQL']['bubble']
    df_rop = Data.from_sql(query_or_table=query, conn_dict=conn_dict).df
    print('loeaded Stability test data >>>> ROP')
    return df_rop