# 6_if.py

"""
    1. 자바
    boolean money = true;
    if(money){
        System.out.print("택시를 타고 가라");
    } else{
        System.out.print("걸어가라");
    }
"""
from operator import truediv

money = True        # 변수
if money:
    print("택시를 타고 가라")
else:
    print("걸어가라")

# money 변수의 값이 True 이므로 "택시를 타고 가라" 가 출력된다.

# 1. if의 기본 구조
"""
if 조건문 :
(tab) 수행뭉
(tab) 수행문 
(tab) 수행문
else :
(tab) 수행문
(tab) 수행문
(tab) 수행문
"""

# 2. 들여쓰기 방법
    # 1) if 문에 속하는 모든 실행문은 (tab) 들여쓰기 해야함
    # 2) 다른 프로그래밍 언어를 사용해 온 사람들은 간과할 수 있다.
    # 3) tab(탭)키, 범위 드래그 후 ctrl + alt + l -> 자동 tab
    # 4) 들여쓰기 깊이 / 수준을 속해있는 범위에 맞게 사용해야한다.
if money:
    print("택시를")
    print("타고")  # unexpected indent
    print("가라")
else:
    print("걸어가라")

if money:
    print("택시를")
    print("타고")
    print("가라")  # unexpected indent


# 3. 조건문이란 무엇인가?
    # > 조건문이란 참과 거짓을 판단하는 문장
    # 1) 비교 연산자, > 초과, < 미만, >= 이상, <= 이하, == 같다, != 같지 않다
x = 3
y = 2
print(x > y)        # True
print(x < y)        # False
print(x == y)       # False
print(x != y)       # True
print(x >= y)       # True
print(x <= y)       # False

# 예제1
money1 = 2000
if money1 >= 3000:          # money = 2000 이기 때문에 else 문 실행
    print("택시를 타고 가라")
else:
    print("걸어 가라")

    # 2) 논리 연산자, and 이면서, or 이거나, not 부정
money2 = 2000
card = True
if money2 > 3000 or card:   # card = True 이기 때문에 if 문이 True 이므로 if 문 실행
    print("택시를 타고 가라")
else:
    print("걸어 가라")

    # 3) 기타 연산자, value in list / tuple / 문자열, not in list / tuple / 문자열
print(2 in [1,2,3])         # True
print(2 not in [1,2,3])     # False
print('a' in ('a', 'b', 'c'))   # True, tuple 에 'a' 가 있는가?
print('j' not in 'python')      # True, 문자열에 'j'가 있는가?

pocket = ['paper', 'cellphone', 'money']
if 'money' in pocket :          # pocket list 에 'money' 가 있다면 if 문 실행
    print("택시를 타고 가라")
    pass
else :                          # pocket list 에 'money' 가 없다면 else 문 실행
    print("걸어 가라")

    # 4) 다양한 조건을 판단하는 elif
pocket1 = ['paper', 'cellphone']
card1 = True
if 'money' in pocket1 :
    print("택시를 타고 가라")
else :
    if card1 :
        print("택시를 타고 가라")
    else :
        print("걸어 가라")

if 'money' in pocket1 :
    print("택시를 타고 가라")
elif card1 :
    print("택시를 타고 가라")
else:
    print("걸어 가라")

    # 5) 조건부 표현식, if 대신에 간단한 조건문 표현
        # 참일 경우 if 조건문 else 거짓일 경우
score = 60
message = 'success' if score >= 60 else 'failure'
print(message)      # success