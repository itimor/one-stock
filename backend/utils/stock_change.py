# -*- coding: utf-8 -*-
# author: itimor
# 东方财富-行情中心-盘口异动

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import requests


class StockChange(object):
    symbol_map = {'8201': '火箭发射',
                  '8202': '快速反弹',
                  '8193': '大笔买入',
                  '4': '封涨停板',
                  '32': '打开跌停板',
                  '64': '有大买盘',
                  '8207': '竞价上涨',
                  '8209': '高开5日线',
                  '8211': '向上缺口',
                  '8213': '60日新高',
                  '8215': '60日大幅上涨',
                  '8204': '加速下跌',
                  '8203': '高台跳水',
                  '8194': '大笔卖出',
                  '8': '封跌停板',
                  '16': '打开涨停板',
                  '128': '有大卖盘',
                  '8208': '竞价下跌',
                  '8210': '低开5日线',
                  '8212': '向下缺口',
                  '8214': '60日新低',
                  '8216': '60日大幅下跌'
                  }

    def __init__(self, engine, cur_date):
        self.engine = engine
        self.cur_date = cur_date

    def stock_changes(self, symbol: str) -> pd.DataFrame:
        """
        东方财富-行情中心-盘口异动
        http://quote.eastmoney.com/changes/
        :param symbol: str
        :return: 盘口异动
        :rtype: pandas.DataFrame
        """
        url = "http://push2ex.eastmoney.com/getAllStockChanges"
        params = {
            "type": symbol,
            "pageindex": "0",
            "pagesize": "5000",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "dpt": "wzchanges",
            "_": "1624005264245",
        }
        r = requests.get(url, params=params)
        print(r.url)
        data_json = r.json()
        df = pd.DataFrame(data_json["data"]["allstock"])
        df.columns = [
            "tm",
            "code",
            "_",
            "name",
            "type",
            "i",
        ]
        info = df["i"].str.split(',', expand=True)
        df["info"] = info[0].astype(float)
        df = df[
            [
                "tm",
                "code",
                "name",
                "type",
                "info",
            ]
        ]
        df["time"] = pd.to_datetime(df["tm"], format="%H%M%S").dt.time
        df["type"] = df["type"].astype(str)

        # 设置日期
        df['date'] = self.cur_date
        df['pct_chg'] = 0
        df['hand'] = 0
        return df

    def merge_market(self, df_b: pd.DataFrame) -> pd.DataFrame:
        sql_d = f"select * from stocks_stockdaily order by date desc limit 1;"
        df_d = pd.read_sql_query(sql_d, con=self.engine)
        d = df_d['date'].to_list()[0]
        sql_a = f"select code,close,market,industry from stocks_stockdaily where date='{d}'"
        df_a = pd.read_sql_query(sql_a, con=self.engine)
        df = pd.merge(df_b, df_a, how='inner', left_on=['code'], right_on=['code'])
        df = df[df['market'] < 250]
        df = df[df['market'] > 5]
        df = df[df['close'] > 4]
        return df

    def merge_industry(self, df_b: pd.DataFrame) -> pd.DataFrame:
        sql_a = f"select code,industry from stocks_stock"
        df_a = pd.read_sql_query(sql_a, con=self.engine)
        df = pd.merge(df_b, df_a, how='inner', left_on=['code'], right_on=['code'])
        return df

    def save_df_pct_chg(self, df: pd.DataFrame, n: float = 2.0, mx: float = 7.0) -> pd.DataFrame:
        # 排除股票
        df = df[~ df['name'].str.contains('[ST|SS|*S|退]')]
        df = df[~ df['code'].str.contains('^[3489]')]
        df['pct_chg'] = df['info'] * 100
        df = df[df['pct_chg'] > n]
        df = df[df['pct_chg'] < mx]
        round_dict = {'pct_chg': 2}
        df = df.round(round_dict).sort_values(['pct_chg'], ascending=False)
        df = self.merge_market(df)
        return df

    def save_df_hand(self, df: pd.DataFrame, n: int = 200) -> pd.DataFrame:
        # 排除股票
        df = df[~ df['name'].str.contains('[ST|SS|*S|退]')]
        df = df[~ df['code'].str.contains('^[3489]')]
        df['hand'] = df['info'] / 100
        df = df[df['hand'] > n]
        round_dict = {'hand': 2}
        df = df.round(round_dict).sort_values(['hand'], ascending=False)
        df = self.merge_market(df)
        return df


def main():
    t = int(cur_t)
    print(t)

    cs = StockChange(engine, cur_date)

    # # 60日大幅上涨
    # df = cs.stock_changes(symbol="8215")
    # df = cs.save_df_pct_chg(df, 3.5)
    # last_df = df[df['tm'] < 93000]
    # last_df.to_sql(s_table, con=engine, index=False, if_exists='append')
    #
    # # 竞价上涨
    # df = cs.stock_changes(symbol="8207")
    # df = cs.save_df_pct_chg(df, 3.5)
    # last_df = df[df['tm'] > 92400]
    # last_df.to_sql(s_table, con=engine, index=False, if_exists='append')
    #
    # # 高开5日线
    # df = cs.stock_changes(symbol="8209")
    # df = cs.save_df_pct_chg(df, 4.5)
    # last_df = df
    # last_df.to_sql(s_table, con=engine, index=False, if_exists='append')

    # # 火箭发射
    # df = cs.stock_changes(symbol="8201")
    # df = cs.save_df_pct_chg(df, 2)
    # df.to_sql(s_table, con=engine, index=False, if_exists='append')
    #
    # # 大笔买入
    # df = cs.stock_changes(symbol="8193")
    # df = cs.save_df_hand(df, 200)
    # df.to_sql(s_table, con=engine, index=False, if_exists='append')


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
    s_table = 'stocks_stockchange_xxx'
    print(f'今天日期 {cur_date}')
    main()
