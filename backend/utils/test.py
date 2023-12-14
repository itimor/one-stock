# -*- coding: utf-8 -*-
# author: itimor
# 同花顺概念资金流向前 50

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from requests.exceptions import RequestException
import pandas as pd
import tushare as ts
from lxml import etree
import requests


# 获取网页详情页
def get_page_detail(url):
    """ 提取网页详情页
    :param url: url
    :return: response.text
    """

    cookie = "A3yVJlFlMg6EEAbCrtW2RqA0SxErdSJdoh002Fb9jF5KaBJPfoXwL_IpBSCl"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'http://q.10jqka.com.cn/thshy/detail',
        'Cookie': 'v={}'.format(cookie)
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('请求页面成功')
            return response.text
        return None
    except RequestException:
        print('请求页面失败', url)
        return None


def extract_theme_page(text):
    """ 提取概念页面内容
    :param text: response.text
    :return df_list: list
    """

    selector = etree.HTML(text)
    elements = selector.xpath('//table[@class="m-table J-ajax-table"]/tbody/tr')
    df_list = []
    for element in elements:
        df_dict = dict()
        df_dict['name'] = element.xpath('.//td[2]/a/text()')[0]  # 概念名称
        df_dict['pct_chg'] = float(element.xpath('.//td[4]/text()')[0].rstrip('%'))  # 涨跌幅
        df_dict['amount_in'] = float(element.xpath('.//td[5]/text()')[0])  # 流入资金
        df_dict['amount_out'] = float(element.xpath('.//td[6]/text()')[0])  # 流出资金
        df_dict['real_in'] = float(element.xpath('.//td[7]/text()')[0])  # 净额
        df_dict['leader'] = element.xpath('.//td[9]/a/text()')[0]  # 领涨股
        df_dict['leader_pct_chg'] = float(element.xpath('.//td[10]/text()')[0].rstrip('%'))  # 涨跌幅
        print(df_dict)
        df_list.append(df_dict)
    return df_list


def main():
    # 获取概念资金流
    page_url = ('http://data.10jqka.com.cn/funds/gnzjl/')
    text = get_page_detail(page_url)
    df_list = extract_theme_page(text)
    df = pd.DataFrame(df_list)
    df['date'] = ss_date
    last_df = df.sort_values(['pct_chg'], ascending=False)
    print(last_df.head())
    last_df.to_sql(s_table, engine, if_exists='append', index=False)


if __name__ == '__main__':
    db = f'sqlite:////data/projects/one-stock/backend/core.db'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    m = 2
    n = 0
    start_date = dd - timedelta(days=n + m)
    end_date = dd - timedelta(days=m)
    cur_date = dd.strftime(date_format)
    cur_d = dd.strftime(d_format)
    cur_t = dd.strftime(t_format)
    # 创建连接引擎
    engine = create_engine(db, echo=False)
    conn = engine.connect()
    trans = conn.begin()
    s_table = 'stocks_stockgn'
    ss_date = start_date.strftime(date_format)
    print(f'今天日期 {ss_date}')
    main()
