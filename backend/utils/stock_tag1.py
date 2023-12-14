# -*- coding: utf-8 -*-
# author: itimor
# 给股票打标签

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import sys

from timelib import spent_time

# 设置最大列数，避免只显示部分列
pd.set_option('display.max_columns', 1000)
# 设置最大行数，避免只显示部分行数据
pd.set_option('display.max_rows', 1000)
# 设置显示宽度
pd.set_option('display.width', 1000)
# 设置每列最大宽度，避免属性值或列名显示不全
pd.set_option('display.max_colwidth', 1000)


def get_tag(df):
    df['max_volume'] = df['volume'].rolling(17).max()
    df['is_max_volume'] = df['volume'] == df['max_volume']
    df['max_price'] = df['high'].rolling(17).max()
    df['is_max_price'] = df['high'] == df['max_price']
    df['l_amount_n'] = df['amount'].rolling(5).min()
    df['h_amount_n'] = df['amount'].rolling(7).max()
    df['is_bei'] = (df['amount'] / df['l_amount_n'] > 2) & (df['turn'] > 1)
    df['is_suo'] = (df['h_amount_n'] / df['amount'] > 2) & (df['turn'] > 0)
    df['is_fang'] = (df['amount'] / df['amount'].shift(1) > 1) & (df['turn'] > 0)
    df['mid'] = (df['close'] + df['open']) / 2
    df['return_0'] = (df['close'] / df['open'] - 1) * 100 + 0.0000001
    df['return_kai'] = (df['open'] / df['close'].shift(1) - 1) * 100 + 0.0000001
    df['is_zt'] = (df['high'] == df['close']) & (df['pct_chg'] > 9)
    df['is_first_zt'] = (df['is_zt'] == 1) & (df['pct_chg'].shift(1) < 9)

    # ma
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(8).mean()
    df['ma20'] = df['close'].rolling(18).mean()
    df['ma30'] = df['close'].rolling(28).mean()
    df['is_ma5_ma10_x'] = (df['ma5'] >= df['ma10']) & (df['ma5'].shift(1) <= df['ma10'].shift(1))
    df['is_ma10_ma20_x'] = (df['ma10'] >= df['ma20']) & (df['ma10'].shift(1) <= df['ma20'].shift(1))
    df['is_ma10_ma30_x'] = (df['ma10'] >= df['ma30']) & (df['ma10'].shift(1) <= df['ma30'].shift(1))
    df['is_ma5_x'] = (df['high'] >= df['ma5']) & (df['low'] <= df['ma5'])
    df['is_ma10_x'] = (df['high'] >= df['ma10']) & (df['low'] <= df['ma10'])
    df['is_ma20_x'] = (df['high'] >= df['ma20']) & (df['low'] <= df['ma20'])
    df['is_ma30_x'] = (df['high'] >= df['ma30']) & (df['low'] <= df['ma30'])
    df.drop(['max_volume', 'l_amount_n', 'h_amount_n'], axis=1, inplace=True)
    round_dict = {'ma5': 2, 'ma10': 2, 'ma20': 2, 'ma30': 2, 'return': 2, 'return_kai': 2}
    df = df.round(round_dict)
    return df


@spent_time
def main():
    sql = f"select * from stocks_stock"
    df = pd.read_sql_query(sql, con=engine)
    if len(df) < 1:
        sys.exit()
    data_df = pd.DataFrame()
    m = 0
    print(f'给股票打标签')
    for code in df['code']:
        m += 1
        print(m)
        sql = f"select * from '{s_table}' where code='{code}' order by date asc"
        df = pd.read_sql_query(sql, con=engine)
        df = get_tag(df)
        data_df = pd.concat([data_df, df], ignore_index=True)
    last_df = data_df.reset_index(drop=True)
    last_df['date'] = pd.to_datetime(last_df["date"]).dt.date
    last_df['id'] = list(range(1, 1 + len(last_df)))
    print(last_df)
    if len(last_df) > 0:
        last_df.to_sql(s_table, engine, if_exists='replace', index=False)


if __name__ == '__main__':
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(BASE_DIR, 'core.db')
    db = f'sqlite:///{p}'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    n = 0
    start_date = dd - timedelta(days=60 + n)
    end_date = dd - timedelta(days=n)
    cur_date = dd.strftime(date_format)
    cur_d = dd.strftime(d_format)
    cur_t = int(dd.strftime(t_format))
    # 创建连接引擎
    engine = create_engine(db, echo=False)
    conn = engine.connect()
    trans = conn.begin()
    s_table = 'stocks_stockdaily'
    main()
