# -*- coding: utf-8 -*-
# author: itimor
# 东方财富龙虎榜

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import tushare as ts
import re
import requests

# 设置最大列数，避免只显示部分列
pd.set_option('display.max_columns', 1000)
# 设置最大行数，避免只显示部分行数据
pd.set_option('display.max_rows', 1000)
# 设置显示宽度
pd.set_option('display.width', 1000)
# 设置每列最大宽度，避免属性值或列名显示不全
pd.set_option('display.max_colwidth', 1000)

columns = ['code', 'name', 'jd', 'close', 'pct_chg', 'turn', 'net_buy', 'buy', 'sell', 'memo']


def merge_industry(df_b: pd.DataFrame) -> pd.DataFrame:
    sql_a = f"select code,industry from stocks_stock"
    df_a = pd.read_sql_query(sql_a, con=engine)
    df = pd.merge(df_b, df_a, how='inner', left_on=['code'], right_on=['code'])
    print(df)
    return df


def merge_market(df_b: pd.DataFrame) -> pd.DataFrame:
    sql_d = f"select * from stocks_stockdaily order by date desc limit 1;"
    df_d = pd.read_sql_query(sql_d, con=engine)
    d = df_d['date'].to_list()[0]
    sql_a = f"select code,market from stocks_stockdaily where date='{d}'"
    df_a = pd.read_sql_query(sql_a, con=engine)
    df = pd.merge(df_b, df_a, how='inner', left_on=['code'], right_on=['code'])
    df = df[df['market'] < 200]
    df = df[df['market'] > 5]
    df = merge_industry(df)
    return df


def main():
    for date in trade_days:
        s_date = datetime.strptime(date, d_format)
        ss_date = s_date.strftime(date_format)
        print(ss_date)
        url = f'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,startDate={ss_date},endDate={ss_date},gpfw=0,js=var%20data_tab_1.html?rt=26442172'
        r = requests.get(url).text
        X = re.split(',"url"', r)[0]
        X = re.split('"data":', X)[1]
        df = pd.read_json(X, orient='records')
        df = df[
            ['SCode', 'SName', 'JD', 'ClosePrice', 'Chgradio', 'Dchratio', 'JmMoney', 'Bmoney', 'Smoney', 'Ctypedes']]
        df.columns = columns
        s_codes = []
        for i in df['code']:
            if len(str(i)) < 6:
                s = '0' * (6 - len(str(i))) + str(i)
            else:
                s = str(i)
            if len(s_codes) == 0:
                s_codes = [s]
            else:
                s_codes.append(s)
        df['code'] = s_codes
        df['date'] = ss_date
        df = df[~ df['name'].str.contains('[ST|SS|*S|退]')]
        df = df[~ df['name'].str.contains('[银行|证券]')]
        df = df[~ df['code'].str.contains('^[3489]')]
        df['success'] = df['jd'].str.extract('，成功率(?P<success>.+)%', expand=True)
        df['jd'] = df['jd'].str.extract('(?P<jd>.+)，成功率', expand=True)
        df['success'] = df['success'].astype('float')
        # merge cg lhb
        # cg_sql = f"select date,code,master,chg from {d_table}"
        # df_cg = pd.read_sql_query(cg_sql, con=engine)
        # if len(df_cg):
        #     df = pd.merge(df, df_cg, how='inner', left_on=['date', 'code'], right_on=['date', 'code'])
        # df.fillna(0.0)
        df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
        df = merge_market(df)
        try:
            sql = f"select id  from {s_table} order by id desc limit 1;"
            df_id = pd.read_sql_query(sql, con=engine)
            sid = df_id['id'].to_list()[0] + 1
        except:
            sid = 1
        df['id'] = list(range(sid, sid + len(df)))
        round_dict = {}
        for i in columns[3:]:
            round_dict[i] = 2
        # 去重
        df.drop_duplicates(subset=['code', 'date'], keep='first', inplace=True)
        last_df = df.reset_index(drop=True).round(round_dict)
        last_df.to_sql(s_table, con=engine, index=False, if_exists='append')


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
    s_table = 'stocks_stockeastlhb'
    d_table = 'stocks_stocklhb'
    main()
