# -*- coding: utf-8 -*-
# author: itimor
# baostock获取股票行情

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import tushare as ts
import baostock as bs


def main():
    stock_rs = bs.query_all_stock(ee_date)
    stock_df = stock_rs.get_data()
    df = pd.DataFrame()
    columns = ['date', 'code', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'turn', 'pctChg']
    x = 0
    for code in stock_df["code"]:
        x += 1
        print(x)
        if code[:5] in ['sz.30', 'sz.39', 'sh.00', 'sh.68', 'bj.83', 'bj.87', 'bj.43']:
            print(f"跳过 {code}")
            continue
        print(code)
        k_rs = bs.query_history_k_data_plus(code, ','.join(columns), ss_date, ee_date, frequency="d", adjustflag="3")
        df_code = k_rs.get_data()
        df = pd.concat([df, df_code], ignore_index=True)
    df[columns[2:]] = df[columns[2:]].apply(pd.to_numeric, errors='coerce').fillna(0.0)
    df['date'] = pd.to_datetime(df["date"]).dt.date
    df['pre_code'] = df['code']
    df['code'] = df['code'].str.replace('sz.', '')
    df['code'] = df['code'].str.replace('sh.', '')
    df['return_0'] = (df['close'] / (df['open']) - 1) * 100
    # df['market'] = df['volume'] / df['turn'] * df['close'] * 100  # 原始数值
    df['market'] = df['volume'] / df['turn'] * df['close'] / 1000 / 1000  # 亿为单位
    sql = f"select code,name,industry from stocks_stock"
    df_name = pd.read_sql_query(sql, con=engine)
    df = pd.merge(df, df_name, how='inner', left_on=['code'], right_on=['code'])
    df['id'] = list(range(1, 1 + len(df)))
    round_dict = {'market': 2}
    for column in columns[2:]:
        round_dict[column] = 2
    df.rename(columns={'preclose': 'pre_close', 'pctChg': 'pct_chg'}, inplace=True)
    last_df = df.reset_index(drop=True).round(round_dict)
    last_df.to_sql(s_table, engine, if_exists='replace', index=False)


if __name__ == '__main__':
    import sys
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(BASE_DIR, 'core.db')
    if sys.platform == 'win32':
        db = f'sqlite:///{p}'
        engine = create_engine(db, echo=False)
    else:
        db = f'sqlite:////data/projects/one-stock/backend/core.db'
        engine = create_engine(db, echo=False)
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    m = 80
    n = 0
    start_date = dd - timedelta(days=m + n)
    end_date = dd - timedelta(days=n)
    cur_date = dd.strftime(date_format)
    cur_d = dd.strftime(d_format)
    cur_t = dd.strftime(t_format)
    ss_date = start_date.strftime(date_format)
    ee_date = end_date.strftime(date_format)
    print(ss_date)
    print(ee_date)
    # 创建连接引擎
    conn = engine.connect()
    trans = conn.begin()
    s_table = 'stocks_stockdaily'
    # 登陆系统
    bs.login()
    main()
    # 登出系统
    bs.logout()
