import random

count = int(input("你要随机多少个数呢？"))

list = []

for num in range(count):
    list.append(random.randrange(-10000,10000))

print("排序前:"+str(list))
list.sort()
print("排序后："+str(list))