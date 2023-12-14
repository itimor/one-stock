# -*- coding: utf-8 -*-
# author: itimor
# 追加当日实时行情，10:10执行

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import tushare as ts

# 设置最大列数，避免只显示部分列
pd.set_option('display.max_columns', 1000)
# 设置最大行数，避免只显示部分行数据
pd.set_option('display.max_rows', 1000)
# 设置显示宽度
pd.set_option('display.width', 1000)
# 设置每列最大宽度，避免属性值或列名显示不全
pd.set_option('display.max_colwidth', 1000)


def get_all_stock():
    df = ts_data.stock_basic(exchange='', list_status='L', fields='symbol,name,area,industry,market')
    df.rename(columns={'symbol': 'code'}, inplace=True)
    df = df[~ df['name'].str.contains('[ST|SS|*S|退]')]
    df = df[~ df['market'].str.contains('[C|创|北]')]
    df['id'] = range(len(df))
    last_df = df.reset_index(drop=True)
    last_df.to_sql('stocks_stock', con=engine, index=False, if_exists='replace')


# 获取实时行情-tushare接口
def get_stocks_tushare():
    df = ts.get_today_all()
    print()
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
    return df


def main():
    df = get_stocks_tushare()
    print(df)
    sql = f"select * from {s_table} where date = '{cur_date}'"
    s_df = pd.read_sql_query(sql, con=engine)
    if len(s_df) > 0:
        conn.execute(f"delete from {s_table} where date = '{cur_date}'")
        trans.commit()
    columns = ['code', 'pct_chg', 'open', 'high', 'low', 'close', 'volume', 'amount', 'turn']
    df.rename(columns={'trade': 'close', 'changepercent': 'pct_chg', 'turnoverratio': 'turn'}, inplace=True)
    df = df[columns]
    sql = f"select code,name,industry from stocks_stock"
    df_name = pd.read_sql_query(sql, con=engine)
    df = pd.merge(df, df_name, how='inner', left_on=['code'], right_on=['code'])
    df['date'] = cur_date

    df['pre_close'] = 0.0
    df.drop(index=df.open[df.open == 0.0].index, inplace=True)
    df['return_0'] = (df['close'] / (df['open']) - 1) * 100
    df['market'] = df['volume'] / df['turn'] * df['close'] / 1000 / 1000  # 亿为单位
    round_dict = {'return_0': 2, 'market': 2}
    for column in columns[1:]:
        round_dict[column] = 2
    df = df.drop_duplicates(subset=['date', 'code'], keep='first')
    sql = f"select id  from {s_table} order by id desc limit 1;"
    df_id = pd.read_sql_query(sql, con=engine)
    sid = df_id['id'].to_list()[0] + 1
    df['id'] = list(range(sid, sid + len(df)))
    # df['id'] = range(1, len(df)+1)
    last_df = df.reset_index(drop=True).round(round_dict)
    print(last_df)
    last_df.to_sql(s_table, engine, if_exists='append', index=False)


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
    m = 0
    start_date = dd - timedelta(days=10 + m)
    end_date = dd - timedelta(days=m)
    cur_date = end_date.strftime(date_format)
    cur_d = dd.strftime(d_format)
    cur_t = dd.strftime(t_format)
    # ts初始化
    ts.set_token('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
    ts_data = ts.pro_api()
    # 创建连接引擎
    engine = create_engine(db, echo=False)
    conn = engine.connect()
    trans = conn.begin()
    s_table = 'stocks_stockdaily'
    get_all_stock()
    main()
