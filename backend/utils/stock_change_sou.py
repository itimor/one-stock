# -*- coding: utf-8 -*-
# author: itimor
# 东方财富-行情中心-盘口异动

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
from stock_change import StockChange
import sys


# 设置最大列数，避免只显示部分列
pd.set_option('display.max_columns', 1000)
# 设置最大行数，避免只显示部分行数据
pd.set_option('display.max_rows', 1000)
# 设置显示宽度
pd.set_option('display.width', 1000)
# 设置每列最大宽度，避免属性值或列名显示不全
pd.set_option('display.max_colwidth', 1000)


def main():
    t = int(cur_t)
    print(t)
    if 91500 < t <= 193000:
        print("搜集数据")
        # 60日大幅上涨
        df = cs.stock_changes(symbol="8215")
        df = cs.save_df_pct_chg(df, 4, 7)
        last_df = df[df['tm'] < 93000]
        last_df.to_sql(s_table, con=engine, index=False, if_exists='append')
        print(last_df)

        # 高开5日线
        df = cs.stock_changes(symbol="8209")
        df = cs.save_df_pct_chg(df, 3, 7)
        last_df = df
        last_df.to_sql(s_table, con=engine, index=False, if_exists='append')
        print(last_df)

    sql = f"select * from {s_table} where date='{cur_date}' and tm<93100"
    df = pd.read_sql_query(sql, con=engine)
    new_df = df['code']
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
    t_format = '%H%M%S'
    # 获得当天
    dd = datetime.now()
    m = 0
    start_date = dd - timedelta(days=10 + m)
    end_date = dd - timedelta(days=m)
    cur_date = end_date.strftime(date_format)
    cur_d = dd.strftime(d_format)
    cur_t = dd.strftime(t_format)
    # 创建连接引擎
    engine = create_engine(db, echo=False)
    conn = engine.connect()
    trans = conn.begin()
    s_table = 'stocks_stocksou'
    pre_d_table = 'sou'
    print(f'今天日期 {cur_date}')
    cs = StockChange(engine, cur_date)
    # cur_date = '2022-06-27'
    main()
