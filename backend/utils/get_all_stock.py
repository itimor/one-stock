# -*- coding: utf-8 -*-
# author: itimor
# 成交量持续倍增
# 代表 中国国贸 拉芳家化 2021-04-30

from sqlalchemy import create_engine
import pandas as pd
import tushare as ts
import time

# 设置最大列数，避免只显示部分列
pd.set_option('display.max_columns', 1000)
# 设置最大行数，避免只显示部分行数据
pd.set_option('display.max_rows', 1000)
# 设置显示宽度
pd.set_option('display.width', 1000)
# 设置每列最大宽度，避免属性值或列名显示不全
pd.set_option('display.max_colwidth', 1000)

headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def main():
    df = ts_data.stock_basic(exchange='', list_status='L', fields='symbol,name,area,industry,market')
    df.rename(columns={'symbol': 'code'}, inplace=True)
    df = df[~ df['name'].str.contains('[ST|SS|*S|退]')]
    df = df[~ df['market'].str.contains('[C|创|北]')]
    df['id'] = range(len(df))
    last_df = df.reset_index(drop=True)
    last_df.to_sql(s_table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(BASE_DIR, 'core.db')
    db = f'sqlite:///{p}'
    # ts初始化
    ts.set_token('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
    ts_data = ts.pro_api()
    # 创建连接引擎
    engine = create_engine(db, echo=False)
    conn = engine.connect()
    trans = conn.begin()
    s_table = 'stocks_stock'
    main()
