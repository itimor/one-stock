# -*- coding: utf-8 -*-
# author: itimor


import random

hua = ['黑桃', '红桃', '梅花', '方块']

base_puke = [3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
puke = [3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]


def conversion(xlist):
    '''
    将花牌和大小王转换成数字10
    '''
    l = []
    for i in xlist:
        if i in ["J", "Q", "K", "小王", "大王"]:
            l.append(10)
        elif i == "A":
            l.append(1)
        else:
            l.append(i)
    return l


def niuniu():
    x = []
    first = random.choice(puke)
    x.append(first)
    puke.pop(puke.index(first))
    second = random.choice(puke)
    x.append(second)
    puke.pop(puke.index(second))
    thrid = random.choice(puke)
    x.append(thrid)
    puke.pop(puke.index(thrid))
    fourth = random.choice(puke)
    x.append(fourth)
    puke.pop(puke.index(fourth))
    fifth = random.choice(puke)
    x.append(fifth)
    puke.pop(puke.index(fifth))
    return x


def compute(xlist):
    if (xlist[0] + xlist[1] + xlist[2]) % 10 == 0 or (xlist[0] + xlist[1] + xlist[3]) % 10 == 0 or (
            xlist[0] + xlist[1] + xlist[4]) % 10 == 0 or (xlist[0] + xlist[2] + xlist[3]) % 10 == 0 or (
            xlist[0] + xlist[2] + xlist[4]) % 10 == 0 or (xlist[0] + xlist[3] + xlist[4]) % 10 == 0 or (
            xlist[1] + xlist[2] + xlist[3]) % 10 == 0 or (xlist[1] + xlist[2] + xlist[4]) % 10 == 0 or (
            xlist[1] + xlist[3] + xlist[4]) % 10 == 0 or (xlist[2] + xlist[3] + xlist[4]) % 10 == 0:
        total = xlist[0] + xlist[1] + xlist[2] + xlist[3] + xlist[4]
        result = int(str(total)[-1])
        if result == 0:
            return 0  # 牛牛
        else:
            return result
    return -1  # 无牛


def format_print(x):
    if len(str(x)) > 1:
        return str(x)
    return " " + str(x)


def players(x):
    di = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七"}
    for i in range(x):
        player_puke = niuniu()
        player = conversion(player_puke)
        player_puke = f"{format_print(player_puke[0])}  {format_print(player_puke[1])}  {format_print(player_puke[2])}  {format_print(player_puke[3])}  {format_print(player_puke[4])}"
        if compute(player) != -1:
            if compute(player) != 0:
                print(f"玩家{di[i + 1]}: {player_puke}  --  牛{compute(player)}")
            else:
                print(f"玩家{di[i + 1]}: {player_puke}  --  『牛牛』")
        else:
            print(f"玩家{di[i + 1]}: {player_puke}  --  无牛")


def zhuang():
    zhuang_puke = niuniu()
    player = conversion(zhuang_puke)
    zhuang_puke = f"{format_print(zhuang_puke[0])}  {format_print(zhuang_puke[1])}  {format_print(zhuang_puke[2])}  {format_print(zhuang_puke[3])}  {format_print(zhuang_puke[4])}"
    if compute(player) != -1:
        if compute(player) != 0:
            print(f"庄 家: {zhuang_puke}  --  牛{compute(player)}")
        else:
            print(f"庄 家: {zhuang_puke}  --  『牛牛』")
    else:
        print(f"庄 家: {zhuang_puke}  --  无牛")


if __name__ == '__main__':
    # players(3)
    # input("按下回车键开庄...")
    # zhuang()
    a = conversion(base_puke)
    print(a)
