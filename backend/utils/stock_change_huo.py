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


def count_stock(typ, t1, t2, min, max):
    time = f"time>='{t1}' and time <'{t2}'"
    info = f"pct_chg>2 and pct_chg <9.43"
    sql = f"select name,code,close,market,date,time,count(*) as c,industry from {s_table} where type='{typ}' and date='{cur_date}' and {time} and {info} group by code having c>{min} and c<{max} order by c desc"
    df = pd.read_sql_query(sql, con=engine)
    new_df = df['code']
    if len(df) > 0:
        print(f'############## 时间：「{t1} - {t2}」，请于观察3分钟再操作股票 ##############')
        df['tm'] = t1
        df['type'] = typ
        print(df)
        df.to_sql(d_table, con=engine, index=False, if_exists='append')
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


def main():
    t = int(cur_t)
    print(t)
    typ = '8201'
    if 93000 < t <= 194500:
        # print("清理 s_table 数据")
        # sql = f"select * from {s_table} where date='{cur_date}' and time>'09:30:00' and type='{typ}'"
        # df = pd.read_sql_query(sql, con=engine)
        # if len(df) > 0:
        #     conn.execute(f"delete from {s_table} where date='{cur_date}' and time>'09:30:00' and type='{typ}'")
        # trans.commit()

        print("搜集数据")
        df = cs.stock_changes(symbol=typ)
        df = cs.save_df_pct_chg(df, 2)
        df.to_sql(s_table, con=engine, index=False, if_exists='append')

    min = 1
    max = 15
    ts = 30
    tn = 30
    step = 4
    n = int((tn - ts) / step)
    print("统计数据")
    for i in range(n + 1):
        t1 = '09:%s:00' % (ts + i * step)
        t2 = f'09:%s:00' % (ts + i * step + step)
        count_stock(typ, t1, t2, min, max)


if __name__ == '__main__':
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(BASE_DIR, 'core.db')
    db = f'sqlite:///{p}'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M%S'
    time_format = '%H:%M:%S'
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
    s_table = 'stocks_stockchange'
    d_table = 'stocks_stockhuo'
    pre_d_table = 'huo'
    print(f'今天日期 {cur_date}')
    cs = StockChange(engine, cur_date)
    # cur_date = '2022-07-04'
    main()
