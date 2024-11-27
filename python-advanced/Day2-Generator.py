from torch.utils.hipify.hipify_python import value

temp_str = "YouAreNumerousStars"
my_iter = iter(temp_str)  # 转换为迭代器


# for i in my_iter: #输出字符
# print(i)

def fibo(n):
    a = b = 1
    for i in range(n):
        yield a  # 将a的值返回给调用者fibo，然后暂停观察是否还需要进行下一次迭代
        # 如果需要下一次迭代，就继续运行a, b = b, a + b
        a, b = b, a + b  # a=b,b=a+b


# for i in fibo(5):  # 调用斐波那契数列需要使用迭代才能调用
# print(i)

class cal_area(object):
    pi = 3.142

    def __init__(self, r):
        self.r = r

    def area(self):
        return self.pi * self.r * self.r  # 需要给变量前面加上self


# a = cal_area(5)
# print(a.area())

class test_info(object):
    def __init__(self, **kwargs):
        self.info = {**kwargs}

    def __getitem__(self, item):
        return self.info[item]

myinfo = {"name": "Arden", "position": 'student'}
a = test_info(**myinfo)
# print(a.__getitem__("name"))

"""
元类是创建类的类。比如元类为Mymeta，其中的x为新建的类。
"""
class Mymeta(type):  # type是内建的元类，用于创建类对象
    def __new__(cls, name, bases, dct):  # 允许我们自定义类的创建过程
        """
        注：以下内容为局部变量，非属性
        cls：指的是当前正在创建的类（即MyMeta自身）。
        name：是类的名称。
        bases：是类的基类元组（由于在Python 3中，所有类默认继承自object，所以这里可能不显式包含object）。
        dct：是一个字典，包含了类定义中所有的属性和方法。
        """
        x = super().__new__(cls, name, bases, dct)
        # 新建类x，super()返回了母函数(Mymeta的上一级type)
        x.attrs = 100 #给x类添加属性attrs，赋值100
        return x
class MyClass(metaclass=Mymeta): #
    pass  # 占位符语句
#print(MyClass.name) 局部变量无法运行
#print(MyClass.__name__) #__name__是Python自动为每个类设置的，用于存储类的名称

#描述符只要定义了__set__，被称为数据描述符；没有定义__set__为实例描述符
#数据优先级>实例优先级
class Descriptor: #定义描述符
    def __set_name__(self, owner, name):#描述符被分配给了哪个类（owner）以及它在该类中的名称（name）
        self.name = f"__{name}__"  #加下划线是为了符合描述符在类中被赋予的名称
    def __get__(self, instance, owner):#获取描述符的值。instance 是尝试访问描述符的实例（如果有的话）。
        return getattr(instance, self.name) #从实例的 __dict__ 中获取以 self.name的值，并返回它
    def __set__(self, instance, value):#设置描述符的值
        setattr(instance, self.name, value)
        #在实例的 __dict__ 中设置以 self.name命名的属性的值为 value
    def __delete__(self, instance):
        delattr(instance, self.name)#从实例的 __dict__ 中删除以self.name命名的属性。

class X:
    """
    data的类属性是 Descriptor 类的一个实例。
    它会自动为 X的实例提供 __get__, __set__, 和 __delete__ 方法所定义的行为。
    """
    data=Descriptor()
    name=Descriptor()
x=X()
x.data=100
x.name="Arden"
#print(x.data, x.name)
#print(x.__dict__)

"""
使用上下文管理器的好处带来了更好的异常处理、更简洁的代码和更高的可维护性。
"""
class File(): #可以省略括号中的object，因为在Python3中是默认的
    def __init__(self, file_name):#初始化File，每次使用都会实现以下代码
        self.file_name = file_name
        self.file_obj = open(self.file_name, "w") #按file_name以写入模式打开文件
    def __enter__(self):
        return self.file_obj
        #在 with 语句中，这个返回的对象会被赋值给 as 关键字后面的变量
    def __exit__(self, exc_type, exc_val, exc_tb):#当 with 语句块执行完毕或发生异常时，会自动调用这个方法
        #异常类型 exc_type，异常值 exc_val，和异常跟踪信息 exc_tb
        print(exc_type, exc_val, exc_tb)
        self.file_obj.close()
#with File("test.txt") as opened_file:#File中的self.file_obj返回给opened_file
    #opened_file.write("Hiiii")
    #opened_file.read() #只写文件，读会报错

#with open("test2.txt", "w") as write_file: #直接实现对文件的修改
    #write_file.write("hello world")

from contextlib import contextmanager
@contextmanager
def open_file(name):
    f = open(name, "w")
    try:
        yield f #这行代码是 contextmanager 装饰器使用的关键。
        # 它暂停了生成器的执行，并将 f 返回给上下文管理器的调用者。
        # 调用者可以使用这个文件对象进行读写操作。
        # 当调用者完成操作并退出 with 语句块时，生成器的执行将继续进行。
    finally:
        f.close()
"""
change_file打开了test3文件，文件对象返回给变量f
然后执行try命令，遇见yield f，暂停并返回给with语句调用者。
执行with语句中的操作，执行完毕后，生成器将继续执行。
"""
#with open_file("test3.txt") as f:
    #f.write("Context\n")

#实现一个简单的性能监控装饰器
import functools
import time
import tracemalloc

def performance(func):
    @functools.wraps(func)
    def wrapper_time_memory(*args, **kwargs):
        start_time = time.time()

        tracemalloc.start()

        value = func(*args,**kwargs)

        snapshot = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        # 分别获取当前内存和峰值内存
        current_memory = snapshot[0]
        peak_memory = snapshot[1]

        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time: {time_taken:.4f} seconds") #格式化输出时间
        print(f"Memory taken: {current_memory/1024:.2f} KB")
        print(f"Peak Memory taken: {peak_memory/1024:.2f} KB")
        return value
    return wrapper_time_memory

@performance
def fibon(n):
    a=b=1
    for i in range(n):
        yield a
        a,b = b,a+b

fibon(100) #运行时打印时间和内存占用情况
for i in fibon(100): #生成器会再次运行，再打印一次
    print(i)


