# -*- coding: utf-8 -*-
# author: timor

from random import shuffle, sample
from datetime import datetime, timedelta
from time import time
from timelib import spent_time
import os


def gen_red(red_box, kill_red, redchoose):
    for i in kill_red:
        if i in red_box:
            red_box.remove(i)
    red_balls = []
    for _ in range(redchoose):
        red_nums = gun(red_box)
        qiu = red_nums.pop()
        red_balls.append(qiu)
    return red_balls


def init_box(kill_red):
    redchoose = 11
    red1 = [i for i in range(1, 12)]
    red2 = [i for i in range(12, 23)]
    red3 = [i for i in range(23, 34)]
    red_1_2 = red1 + red2
    red_1_3 = red1 + red3
    red_2_3 = red2 + red3
    red_balls_1 = gen_red(red_1_2, kill_red, redchoose)
    red_balls_2 = gen_red(red_1_3, kill_red, redchoose)
    red_balls_3 = gen_red(red_2_3, kill_red, redchoose)
    return red_balls_1 + red_balls_2 + red_balls_3


def display(t, balls):
    """
    输出列表中的双色球号码
    """
    if t == 'ssq':
        n = 1
    else:
        n = 2

    a = ''
    for index, ball in enumerate(balls):
        if index == len(balls) - n:
            a += ' |'
        a += ' %02d' % ball
    print(a)
    with open(f, 'a+') as fn:
        fn.write(a + '\n')


def gun(lst):
    a = str(time())
    b = a[::-1]
    c = str(int(float(b)))
    s = 0
    for i in c:
        s += int(i)
    for _ in range(s):
        shuffle(lst)
    return lst


def random_select(info, kill_red, kill_blue):
    """
    随机选择一组号码
    """

    red_nums = init_box(kill_red)
    red_balls = []
    for _ in range(info['redchoose']):
        red_nums = gun(red_nums)
        qiu = red_nums.pop()
        red_balls.append(qiu)
    red_balls.sort()

    blue_nums = list(range(1, info['bluemax']))
    [blue_nums.remove(i) for i in kill_blue]
    blue_balls = []
    for _ in range(info['bluechoose']):
        blue_nums = gun(blue_nums)
        qiu = blue_nums.pop()
        blue_balls.append(qiu)
    blue_balls.sort()
    display(t, red_balls + blue_balls)
    return red_balls + blue_balls


@spent_time
def gen_double(t, m, kill_red, kill_blue):
    lst = []
    if t == 'ssq':
        info = {
            'redmax': 33 + 1,
            'bluemax': 16 + 1,
            'redchoose': 6,
            'bluechoose': 1,
        }
    else:
        info = {
            'redmax': 35 + 1,
            'bluemax': 12 + 1,
            'redchoose': 5,
            'bluechoose': 2,
        }
    for _ in range(m):
        lst.append(random_select(info, kill_red, kill_blue))
    return {'all_ball': lst, 'god_ball': sample(lst, 2)}


if __name__ == '__main__':
    date_format = '%Y-%m-%d'
    dd = datetime.now()
    cur_date = dd.strftime(date_format)
    f = cur_date + '.qiu'
    if os.path.isfile(f):
        os.remove(f)
    t = 'ssq'
    # t = 'dlt'
    # 杀号
    kill_red = [5, 14, 20, 23, 33]
    kill_blue = [4, 11, 12, 13, 14, 16]
    m = 10
    gen_double(t, m, kill_red, kill_blue)
