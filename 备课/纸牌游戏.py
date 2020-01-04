'''
游戏规则：随机抽取两张纸牌，比较双方点数，大的获胜
'''

import random

types = ["黑桃","红心","梅花","方块"]
nums = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]


keep_going = True

answer = input("输入Enter继续，任意键退出")
keep_going = (answer == "")

while keep_going:
    my_types = random.choice(types)
    my_num = random.choice(nums)

    your_types = random.choice(types)
    your_num = random.choice(nums)

    print("我的牌是：" + my_types + my_num)
    print("电脑的牌是：" + your_types + your_num)

    if nums.index(my_num) < nums.index(your_num):
        print("电脑赢了")
    elif nums.index(my_num) > nums.index(your_num):
        print("我赢了")
    else:
        print("平局")
    answer = input("输入Enter继续，任意键退出")
    keep_going = (answer=="")
    
