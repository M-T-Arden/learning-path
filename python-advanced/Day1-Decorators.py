# *args and **kwargs 传递不定数量的值，如没有规定数量的字符串等
# 当使用 * 解包时，如果传入的是一个字符串，它会将字符串解包为字符序列。
# 当使用 ** 解包时，如果传入的是一个字典，它会将字典解包为关键字参数。

def test_args(value, *args):
    print("first:", value)
    for arg in args:
        print("next:", arg)


# test_args('hello','world','three','four')

def test_kwargs(**kwargs):
    for key, value in kwargs.items():
        print("{} = {}".format(key, value))


# test_kwargs(name='GPT',age='0.5 year',sex='none')

def test_args_and_kwargs(name, age, sex):
    print("name:", name)
    print("age:", age)
    print("sex:", sex)


args = ("GPT", "0.5 year", 'none')
# test_args_and_kwargs(*args)
kwargs = {"name": 'GPT', "sex": 'none', "age": '0.5 year'}


# test_args_and_kwargs(**kwargs) #使用**输出时需要注意列表里的key要与函数里的key对应

def decorator(func):
    def wrapper():  # 包装内容
        print("before the function")
        func()
        print("after the function")

    return wrapper


def say_hello():
    print("hello!")


# say_hello() #装饰前
say_hello = decorator(say_hello)  # 装饰后的


# say_hello()

@decorator  # 文法糖的装饰功能与say_hello = decorator(say_hello)功能一致
def say_hi():
    print("hi")


# say_hi()

import functools

def do_twice(func):
    @functools.wraps(func)  # 使用 @ functools.wraps裝飾器，它將保留有關原始函數的資訊
    def wrapper(*args, **kwargs):  # 接受任意數量的參數並將它們傳遞給它修飾的函數
        func(*args, **kwargs)
        func(*args, **kwargs)
        return func(*args, **kwargs)  # 保证如果与需求，可以回传函数值

    return wrapper


@do_twice
def say_hello(name):
    print("hello!", name)


# say_hello('Arden')
info = "Arden"
# say_hello(*info) #无法实现，*会将“Arden”解包为字符序列，因此有五个参数，与函数不符。
# say_hello(info)
info_me = {"name": "Arden"}
# say_hello(**info_me)

import functools  # 装饰器模板
import time

def timer(func):
    # 用来统计函数运行时间
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        start_time = time.time()  # 统计开始时时间
        value = func(*args, **kwargs)
        end_time = time.time()  # 记结束时间
        time_taken = end_time - start_time #时间差值
        print("It takes", time_taken, "seconds")
        return value
    return wrapper_decorator

@timer
def waste(num):
    for i in range(num):
        sum([i**2 for i in range(10000)]) #计算(1+...+2i)的和(i<=10000)

#waste(1)
#waste(999)