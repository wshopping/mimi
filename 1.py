# a = range(12)
# k = 5
# num = 0
# x = len(a)//k
# y = len(a)%k
# # for i in range(x):
# for i in range(k):
#     if i<x:
#         list = []
#         for j in range(3):
#             list.append(num)
#             num+=1
#         print(list)
# # for d in range(3):
#     else:
#         list2 = []
#         for c in range(y):
#             list2.append(num)
#             num += 1
#         print(list2)






# def func(a:list,b:list):
#     # temp_dict = defaultdict(set)
#     temp_dict = {}
#     temp_list = a + b
#     res = []
#     for string in temp_list:
#         handler(string,temp_dict)
#     for k,v in temp_dict.items():
#         res.append(f'{k},' + ','.join(v))
#     return res
#
# def handler(string:str,d:dict):
#     temp_list = string.split(',')
#     letter = temp_list[0]
#     numbers = temp_list[1:]
#     number_set = d.get(letter,set())
#     for number in numbers:
#         number_set.add(number)
#     d[letter] = number_set
#
# if __name__ == '__main__':
#     a = ['a,1','bb,3,22','c,3,4','b,5',]
#     b = ['a,2', 'bb,1','d,2','a,3', ]
#     c = func(a,b)
#     print(c)



# def is_even(k):
#     flag = 0
#     for i in range(k+1):
#         if i == flag:
#             flag+=2
#             if i == len(range(k)):
#                 print(k,"是偶数")
#         else:
#             if i == len(range(k)):
#                 print(k,"是技术")
# is_even(8)



# def minmax(data):
#     if data == []:
#         return (None)
#     else:
#         Max = data[0]
#         Min = data[0]
#         for i in  data:
#             if i>Max:
#                 Max=i
#             if i<Min:
#                 Min=i
#         return (Max,Min)
#
# data = [1,4,3,6,2,9,8,0]
# print(minmax(data))


# def s(n):
#     return [i*i for i in range(n)]
# print(s(5))
# list = []
# for i in range(8,-10,-2):
#     list.append(i)
# print(list)



# print([2**i for i in range(9)])

# a= [1,2,3,4]
# print(len(a))
# class A(object):
#     def __init__(self):
#         pass


# def pre(data):
#     n = len(data)
#     a = [0]*n
#     for j in range(n):
#         total = 0
#         for i in range(j+1):
#             total += data[i]
#         a[j] = total/(j+1)
#     return a
# data = [1,2,3,4]
# print(pre(data))




# def fibo(n):
#     if n==1  or  n==2:
#         return 1
#     else:
#         if n>2:
#             return fibo(n-1)+fibo(n-2)
# res = fibo(5)
# print(res)




# lis = []
# for i in range(1,20):
#     if i ==1 or i ==2:
#         lis.append(1)
#     else:
#         lis.append(lis[i-3]+lis[i-2])
# print(lis)


# a = ["name","li",'age','18']
# b = dict(zip(a[0::2],a[1::2]))
# print(b)
a = ["name","li",'age','18']
# info = {}
# for i in range(0,len(a),2):
#     info[a[i]]=a[i+1]
# print(info)
# info = {}
# for i in  range(0,len(a),2):
#     info[a[i]]=a[i+1]
# print(info)
# b = dict(zip(a[0::2],a[1::2]))
# print(type(b))
# b = zip(a[0::2],a[1::2])
# print(b)
# info = {}
# for index,value in enumerate(a):
#     if index%2==0:
#         info[a[index]] = a[index+1]
# print(info)



a = [1,1,2,3,3,4,5,5]
# result = list(set(a))
# print(result)
# result.sort(key=a.index)
# print(result)
# result = []
# [result.append(i) for  i in a if i not in result]
# print(result)


# import random
# def choice():
#     a = random.randint(1,100)
#     if a>10:
#         return a
#     else:
#         return choice()
# i = choice()
# print(i)


# a = {'a':24,'b':56,'c':23,'d':12,'e':34}
# result = sorted(a.items(),key=lambda x:x[1])
# print(result)




# a= int(input(""))
# list = []
# for i in range(2,a):
#     while True:
#         if a%i==0:
#             a = a/i
#             list.append(i)
#         else:
#             break
# b = []
# for name in list:
#     b.append(str(name))
# print('*'.join(b))


# a = int(input())
# list = []
# for i in range(2,a):
#     while True:
#         if a%i==0:
#             a = a/i
#             list.append(i)
#         else:
#             break
# b = []
# for name in list:
#     b.append(str(name))
# print("*".join(b))

# a = 1
# for i in range(5):
#     if i == 2:
#         break
#         a += 1
#     else:
#         a += 1
# print (a)

# from  collections import Counter
# import random
# list1 = [random.randint(0,100) for i in range(1000)]
# print(Counter(list1))
# print(dict([1, 2]))


# a = {"a":1,"b":2,"c":3,"d":4}
# key = input("请输入键：")
# print(a.get(key,"不存在"))

# def bar(n):
#   m = n
#   while True:
#     m += 1
#     yield m
# b = bar(3)
# print(b.next())
#













