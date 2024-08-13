# 5_2장_되새김_문제.py
from audioop import reverse

# Q1
korean = 80
english = 75
math = 55
print((korean + english + math) / 3)    # 70.0

# Q2
a = 13
if a % 2 == 1:
    print("홀수")
else :
    print("짝수")

# Q3
pin = "881120-1068234"
print(pin.split('-'))
yyyymmdd = "19" + pin.split('-')[0]
num = pin.split('-')[1]
print(yyyymmdd)
print(num)

# Q4
t1 = tuple(pin)
print(t1)
print(t1[7])

# Q5
a1 = "a:b:c:d"
print(a1.replace(":","#"))

# Q6
a2 = [1,2,3,4,5]
a2.reverse()
print(a2)

# Q7
a3 = ['Life', 'is', 'too', 'short']
result = ' '.join(a3)
print(result)

# Q8
a4 = (1, 2, 3)
a5 = (4, )
a4 = a4 + a5
print(a4)

# Q9
a6 = dict()
a6[('a',)] = 'python'
print(a6)
a6['name'] = 'python'
print(a6)
# a6[[1]] = 'python' # 오류 발생
# print(a6)
# a[250] = 'python' # 대입 자체가 안된다.
# print(a6)

# Q10
a7 = {'A' : 90, 'B' : 80, 'C' : 70}
result1 = a7.pop('B')
print(a7)
print(result1)

# Q11
a8 = [1,1,1,2,2,2,3,3,3,4,4,5]
aSet = set(a8)
b = list(aSet)
print(b)

# Q12
a9 = b9 = [1,2,3]
a9[1] = 4
print(b9)   # a9 와 b9 에 같은 값을 대입했기 때문에 a9[1] = 4를 대입해도 b9[1] = 4가 같이 대입된다.


