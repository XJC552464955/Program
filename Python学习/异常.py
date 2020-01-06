# try:
#     num = int(input("请输入一个数字"))
#     result = 10/num
# except ZeroDivisionError:
#     print("不能是0")
# except ValueError:
#     print("类型错误")
# except Exception:
#     print("11")

def A():
    password = input("输入密码:")

    if len(password) < 8:
        return password

    print("抛出异常")
    ex = Exception("密码长度不够")
    raise ex

try:
    print(A())
except Exception as e:
    print(e)