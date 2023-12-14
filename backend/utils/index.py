# -*- coding: utf-8 -*-
# author: timor

from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from hashlib import sha1
from lxml import etree
import time
import requests
import hashlib


def gen_time_pid(prefix):
    pid = '{}_{}'.format(prefix, datetime.now().strftime('%Y%m%d%H%M%S') + str(time.time()).replace('.', '')[-3:])
    return pid


def diff_times_in_seconds(t1, t2):
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60 * h1)
    t2_secs = s2 + 60 * (m2 + 60 * h2)
    tc = str(timedelta(seconds=(t2_secs - t1_secs)))
    return tc


def get_hash(str, salt=None):  # salt 盐
    # 提高字符串的复杂度
    str = '!@#$%' + str + '&^**('
    if salt:
        str = str + salt
    # 取str　hash值
    sh = sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()


def get_cover(w=600, h=800):
    url = f'https://source.unsplash.com/random/{w}x{h}'
    session = requests.Session()
    r = session.get(url)
    return r.url


def gen_md5(str):
    md5 = hashlib.md5()
    # 实例化md5加密方法
    md5.update(str.encode())
    # 进行加密，python2可以给字符串加密，python3只能给字节加密
    result = md5.hexdigest()
    return result


def gen_markdown_table(header, header_code, data):
    n = len(header)
    lines = []
    # 表头部分
    lines += ["{}".format(' | '.join(header))]

    # 分割线
    line = ''
    for i in range(n):
        line += "{}".format(' -- |')
    lines += [line.rstrip(' | ')]

    # 数据部分
    for d in data:
        line = []
        for i in header_code:
            line += [str(d[i])]
        lines += [' | '.join(line)]
    table = '\n'.join(lines)
    return table


def get_stock_info(code):
    headers = {
        'Referer': 'http://www.yjcf360.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    url = f'http://www.yjcf360.com/gegu/{code}/'
    r = requests.get(url, headers=headers).text
    etree_html = etree.HTML(r)
    b = etree_html.xpath('//div[@class="bankuai_list"]/p/span/text()')
    if len(b) > 0:
        b_text = '、'.join(b)
    else:
        b_text = '无'
    c = etree_html.xpath('//div[@class="qu_list"]/p/span/a/text()')
    if len(c) > 0:
        c_text = c[0]
    else:
        c_text = '无'
    g = etree_html.xpath('//div[@class="gainian_list"]/p/span/a/text()')
    g_text = '、'.join(g)
    p = etree_html.xpath('//div[@class="jingying_table"]/div[3]/p/text()')
    if len(p) > 0:
        p_text = p[0].strip()
    else:
        p_text = '无'
    stock_info = {
        'code': code,
        'industry': b_text,
        'address': c_text,
        'product': p_text,
        'concept': g_text,
    }
    return stock_info


def get_163music():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://music.163.com/#/outchain/2/446154202/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    data = {
        'params': 'hosDrAZSw47I9858M/h35luAclU14r5iwahDT7z2vxKqGBKxY0K8bQxSuG/esyBhHPn3r4J3hkbplhNlIc9Q7g5DWrJfIlQ7uy2g4xXihcpR1Z/pJIE/3KksXhZ5l1vfEaEBTv6GFHCTIDk28CWApzUb3g5zcFsUC04HpaR66wsRkCq+gee0dzZvS0rgslGv',
        'encSecKey': 'a4ce0ea8bc28b68f3c50ce14c94f805c02e800a593d42f2acf24c1f01bb5a77c6231d5b45435e045f9d5658d939b2cb6619e530380856bef00cc7267d046b1d8c8b84aae94be3a3b4d45c0ac0731c0d36e50d2b6c6332fa51b9df4afed268e0794ada230296837cc36ad97a1d069410b103ee5b63b3a428c78558efd9c9870bb'
    }
    url = 'https://music.163.com/weapi/v6/playlist/detail'
    r = requests.post(url, data=data, headers=headers).json()
    return r['playlist']['tracks']


def gen_img(prefix, lst, height=1500):
    wight = 100
    font = ImageFont.truetype('SFNS.ttf', 26)
    # 图片颜色
    img_color = "#ffffff"
    font_color = "#000000"
    # 生成背景图片
    image = Image.new('RGB', (wight, height), img_color)
    draw = ImageDraw.Draw(image)
    text_x = 3
    n = 30
    for k, v in enumerate(lst):
        text_y = height - n * k
        draw.text((text_x, height - text_y), v, font_color, font)
    # 保存原始版本
    # img_name = f'{date}_{prefix}.png'
    img_name = f'{prefix}.png'
    image.save(img_name, 'png')


if __name__ == '__main__':
    # header = ["名称", "性别", "电话"]
    # header_code = ["name", "sex", "tel"]
    # data = [
    #     {'name': 'aa', 'sex': 1, 'tel': 11},
    #     {'name': 'bb', 'sex': 2, 'tel': 22},
    #     {'name': 'cc', 'sex': 3, 'tel': 33},
    # ]
    # p = gen_markdown_table(header, header_code, data)
    p = get_163music()
    print(p)
