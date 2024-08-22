# day07 > 5_내장함수.py

# 파이썬 배포본에 함께 들어있는 함수들 = 라이브러리
# import를 하지 않아도 된다.

# 1. abs(숫자) : 절댓값 함수
print(f"{abs(3)}, {abs(-3)}, {abs(-1.2)}")

# 2. all(리스트 / 튜플 / 딕셔너리 / 집합) : 모두 참이면 True 반환하는 함수
    # 데이터들의 참과 거짓, day02 4_불.py 참조
print(f"{all([1,2,3])}, {all([1,2,3,0])}, {all([])}")

# 3. any(리스트 / 튜플 / 딕셔너리 / 집합) : 하나라도 참이면 True 반환하는 함수
print(f"{any([1,2,3])}, {any([0,1,2,3])}, {any([])}")

# 4. chr(유니코드) : 유니코드 숫자를 문자로 변환하는 함수
print(f"{chr(97)}, {chr(44032)}")   # a, 가

# 5. dic(객체) : 해당 객체가 가지는 변수나 함수를 보여주는 함수
print(f"{dir([])}, {dir({})}")

# 6. divmod() : a를 b로 나눈 몫과 나머지를 튜플로 반환
print(divmod(7,3))  # (2, 1), 몫 : 2, 나머지 : 1

# 7. enumerate(리스트 / 튜플 / 문자열) : 인덱스 값을 포함한 객체 반환
for i, name in enumerate(["body", "foo", "bar"]) :
    print(i, name)

# 8. eval(문자열로 구성된 코드) :
print(eval("1 + 2"))            # 3
print(eval("'hi' + 'a'"))       # hia
print(eval("divmod(4,3)"))      # (1,1)

# 9. filter(메소드, 데이터) : 첫번째 인수로 메소드, 두번째 인수로 그 함수에 들어갈 데이터, 메소드의 결과가 참인 것만 묶어서 반환함
def positive(x) :
    return x > 0
print(list(filter(positive, [1, -3, 2, 0, -5, 6]))) # [1, 2, 6]
# 람다식 함수, 함수명 = lambda 매개변수1, 매개변수2 : 실행문
    # 주로 간단한 함수를 간결하게 사용할 때
add = lambda a, b : a+b     # return 명령어가 없어도 결과값이 자동 리턴
print(add(3,4))       # 7
# filter 와 람다식 활용
print(list(filter(lambda x : x > 0, [1, -3, 2, 0, -5, 6])))  # [1, 2, 6],  js : data.filter(x => x>0)


# 10. map(함수, 데이터) : 함수 내 실행문 결과를 반환하는 함수, list()를 이용해서 리스트로 반환 가능
print(list(map(lambda x : x * 2, [1, -3, 2, 0, -5, 6])))    # [2, -6, 4, 0, -10, 12]

# 11. hex
print(hex(234))
print(hex(3))

# 12. id
a = 3
print(id(3))    # 140733444393464
print(id(a))    # 140733444393464
b = a
print(id(b))    # 140733444393464

print(id(4))    # 140733444393496

# 13. input
a = input()
print(a)
b = input("Enter : ")
print(b)

# 14. int
print(int("3"))     # 3
print(int(3.4))     # 3

# 15. isinstance
class Person :
    pass
a = Person()
print(isinstance(a, Person))    # True
b = 3
print(isinstance(b,Person))     # False

# 16. len
print(len("python"))        # 6
print(len([1,2,3]))         # 3
print((1,'a'))              # 2

# 17. list
print(list("python"))       # ['p', 'y', 't', 'h', 'o', 'n']
print(list((1,2,3)))        # [1, 2, 3]
a = [1,2,3]
b = list(a)
print(b)                    # [1, 2, 3]

# 18. max
print(max([1,2,3]))         # 3
print(max("python"))        # y

# 19. min
print(min([1,2,3]))         # 1
print(min("python"))        # h

# 20. oct
print(oct(34))          # 0o42
print(oct(12345))       # 0o30071

# 21. open
f = open("binary_file", "rb")

# 22. ord
print(ord("a"))         # 97
print(ord("가"))        # 44032

# 23. pow
print(pow(2,4))         # 16
print(pow(3,3))         # 27

# 24. range
print(list(range(5)))           # [0, 1, 2, 3, 4]
print(list(range(5,10)))        # [5, 6, 7, 8, 9]
print(list(range(1,10,2)))      # [1, 3, 5, 7, 9]
print(list(range(0,-10,-1)))    # [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]

# 25. round
print(round(4.6))           # 5
print(round(4.2))           # 4
print(round(5.678, 2))      # 5.68

# 26. sorted
print(sorted([3,1,2]))          # [1, 2, 3]
print(sorted(["a","c","b"]))    # ['a', 'b', 'c']
print(sorted("zero"))           # ['e', 'o', 'r', 'z']
print(sorted((3,2,1)))          # [1, 2, 3]

# 27. str
print(str(3))           # 3
print(str("hi"))        # hi

# 28. sum
print(sum([1,2,3]))     # 6
print(sum([4,5,6]))     # 15

# 29. tuple
print(tuple("abc"))     # ('a', 'b', 'c')
print(tuple([1,2,3]))   # (1, 2, 3)
print(tuple((1,2,3)))   # (1, 2, 3)

# 30. type
print(type("abc"))              # <class 'str'>
print(type([]))                 # <class 'list'>
print(type(open("test","w")))   # <class '_io.TextIOWrapper'>

# 31. zip
print(list(zip([1,2,3], [4,5,6])))              # [(1, 4), (2, 5), (3, 6)]
print(list(zip([1,2,3], [4,5,6], [7,8,9])))     # [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
print(list(zip("abc", "def")))                  # [('a', 'd'), ('b', 'e'), ('c', 'f')]