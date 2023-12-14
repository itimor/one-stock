# -*- coding: utf-8 -*-
# author: itimor
# 上涨前下跌下10日线， 在放量涨上1.5倍以上的量可以放心入
# 20220729 恒久科技 胜利精密 常青股份
# 大盘高开可以闭着眼睛打板， 竞价涨幅排序， 王中王

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import sys

# 设置最大列数，避免只显示部分列
pd.set_option('display.max_columns', 1000)
# 设置最大行数，避免只显示部分行数据
pd.set_option('display.max_rows', 1000)
# 设置显示宽度
pd.set_option('display.width', 1000)
# 设置每列最大宽度，避免属性值或列名显示不全
pd.set_option('display.max_colwidth', 1000)


def handle(df):
    r = [1, 2, 3, 4, 5]
    for i in r:
        df['return_' + str(i)] = df['return_0'].shift(i)
        df['pct_chg_' + str(i)] = df['pct_chg'].shift(i)
        df['volume_' + str(i)] = df['volume'].shift(i)
    return df


def main():
    sql = f"select * from {s_table} order by date asc"
    df = pd.read_sql_query(sql, con=engine)
    managed_df = df.groupby('code').apply(handle).reset_index(drop=True)
    result_buy = managed_df[
        (managed_df['return_0'] > 0) &
        (managed_df['volume'] / managed_df['volume_5'] > 2) &
        (managed_df['volume_1'] / managed_df['volume_5'] > 2) &
        (managed_df['volume_2'] / managed_df['volume_5'] > 2) &
        (managed_df['turn'] > 3) &
        (managed_df['close'] > 3) &
        (managed_df['close'] < 100) &
        (managed_df['market'] > 10) &
        (managed_df['market'] < 600)
        ]
    last_df = result_buy.sort_values(['amount'], ascending=False)
    print(last_df.head())
    last_df.to_sql(d_table, engine, if_exists='replace', index=False)

    new_df = last_df[last_df.date == ee_date]['code']
    if len(df) > 0:
        print("导出当天牛股")
        if not os.path.isdir(pre_d_table):
            os.mkdir(pre_d_table)
        if sys.platform == 'win32':
            fd = f'{pre_d_table}\\{cur_date}.txt'
            with open(fd, 'w') as fn:
                for i in new_df:
                    fn.write(i + '\n')
        else:
            from index import gen_img
            fd = os.path.join(pre_d_table, cur_date)
            gen_img(fd, new_df.to_list(), height=800)


if __name__ == '__main__':
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(BASE_DIR, 'core.db')
    db = f'sqlite:///{p}'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    time_format = '%H:%M:%S'

    # 获得当天
    dd = datetime.now()
    m = 0
    start_date = dd - timedelta(days=30 + m)
    end_date = dd - timedelta(days=m)
    cur_date = end_date.strftime(date_format)
    cur_d = dd.strftime(d_format)
    cur_t = int(dd.strftime(t_format))
    # 创建连接引擎
    engine = create_engine(db, echo=False)
    conn = engine.connect()
    trans = conn.begin()
    ss_date = start_date.strftime(date_format)
    ee_date = end_date.strftime(date_format)
    pre_d_table = os.path.basename(__file__).split('.')[0].split('_')[1]
    s_table = 'stocks_stockdaily'
    d_table = f'stocks_stock{pre_d_table}'
    print(f'今天日期 {cur_date}')
    main()
