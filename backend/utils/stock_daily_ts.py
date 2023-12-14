# -*- coding: utf-8 -*-
# author: itimor
# tushare获取股票行情

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import tushare as ts


def main():
    for date in trade_days:
        conn.execute(f"delete from {s_table} where date = '{cur_date}'")
        trans.commit()
        s_date = datetime.strptime(date, d_format)
        ss_date = s_date.strftime(date_format)
        print(ss_date)
        df = ts_data.daily(trade_date=date)
        df['code'] = df['ts_code'].str.replace('.SZ', '')
        df['code'] = df['code'].str.replace('.SH', '')
        sql = f"select code,name,industry from stocks_stock"
        df_name = pd.read_sql_query(sql, con=engine)
        df = pd.merge(df, df_name, how='inner', left_on=['code'], right_on=['code'])
        df.rename(columns={'vol': 'volume'}, inplace=True)
        df['volume'] = df['volume'] * 100
        df['amount'] = df['amount'] * 1000
        df['date'] = ss_date
        df['return_0'] = (df['close'] / (df['open']) - 1) * 100
        df.drop(['ts_code', 'trade_date', 'change'], axis=1, inplace=True)
        try:
            sql = f"select id  from {s_table} order by id desc limit 1;"
            df_id = pd.read_sql_query(sql, con=engine)
            sid = df_id['id'].to_list()[0] + 1
        except:
            sid = 1
        df['id'] = list(range(sid, sid + len(df)))
        df['turn'] = 0
        df['market'] = 0
        round_dict = {'pct_chg': 2, 'return_0': 2}
        last_df = df.reset_index(drop=True).round(round_dict)
        last_df.to_sql(s_table, engine, if_exists='append', index=False)


if __name__ == '__main__':
    import sys
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(BASE_DIR, 'core.db')
    if sys.platform == 'win32':
        db = f'sqlite:///{p}'
    else:
        db = f'sqlite:////data/projects/one-stock/backend/core.db'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    m = 0
    n = 0
    start_date = dd - timedelta(days=m + n)
    end_date = dd - timedelta(days=n)
    cur_date = dd.strftime(date_format)
    cur_d = dd.strftime(d_format)
    cur_t = dd.strftime(t_format)
    # ts初始化
    ts.set_token('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
    ts_data = ts.pro_api()
    df_ts = ts_data.trade_cal(exchange='', start_date=start_date.strftime(d_format),
                              end_date=end_date.strftime(d_format), is_open='1')
    trade_days = df_ts['cal_date'].to_list()
    # 创建连接引擎
    engine = create_engine(db, echo=False)
    conn = engine.connect()
    trans = conn.begin()
    s_table = 'stocks_stockdaily'
    main()
