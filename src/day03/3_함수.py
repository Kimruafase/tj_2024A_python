# 3_함수.py

    # > 함수란 입력값을 가지고 어떤 일을 수행한 후에 그 결과물을 내어놓는 것
    # > 사용 목적 : 1. 코드 재활용(반복 사용) 2. 기능 분리 (가독성 good)

# 1. 파이썬의 함수 구조

"""
(1) python
def 함수명(매개변수1, 매개변수2) :
    실행문
    return 반환값 또는 생략

(2) JS
function 함수명(매개변수1, 매개변수2){
    실행문
    return 반환값 또는 생략
}

(3) JAVA
반환타입 함수명(타입 매개변수, 타입 매개변수){
    실행문;
    return 반환값 또는 생략
}

"""

# ex1
def add(a , b) :
    # {} 가 없으므로 들여쓰기 주의
    return a + b

# 함수 호출
add(3,4)        # add 함수에 3,4를 매개변수로 전달하여 7 반환 받음
print(add(1,2)) # add 함수가 반환한 결과값을 출력한다.

a = 3
b = 4
result = add(a,b)
print(result)   # 7

# 2. 입력값과 리턴값에 따른 함수의 형태
    # 1) 매개변수 O, 리턴값 O
def add(a, b) : # 함수 정의
    result = a + b
    return result

a = add(3,4)    # 함수 호출해서 반환값을 'a' 변수에 저장
print(a)

    # 2) 매개변수 X, 리턴값 O
def say() :         # 함수 정의
    return "HI"

a = say()           # 함수 호출 시 인수 전달이 없고 반환 값을 받아서 'a' 변수에 저장
print(a)

    # 3) 매개변수 O, 리턴값 X
def add(a,b) :      # 함수 정의
    print(f"{a}, {b}의 합은 {a+b}입니다.")

a = add(3,4)    # 함수 호출 시 인수 전달 2개 하고 반환값을 받지 않음

    # 4) 매개변수 X, 리턴값 X
def say() :         # 함수 정의
    print("HI")

say()               # 함수 호출 시 인수 전달 X 반환값 받는 것도 X

# 3. 매개변수를 지정하여 호출하기
def sub(a,b) :
    # print(a, b)
    return a - b
# 함수 호출 시 인수의 값에 따른 대입할 매개변수 지정이 가능하다
print(sub(b = 3, a = 7))

result = sub(a = 7, b = 3)
print(result)

# 4. 입력값이 몇 개인지 모를 때, 가변 매개변수
    # 1)
def add_many(*args) :       # 함수 정의, * 매개변수
    print(args)     # 여러 개의 매개변수 값이 들어있는 튜플
    result = 0  # 더할 값을 저장하기 위한 변수
    for i in args : # 여러 개의 매개변수 리스트를 반복 처리
        result += i
    # for 문 종료 후 result 반환
    return result

# 함수 호출
result = add_many(1,2,3)
print(result)

result = add_many(1,2,3,4,5,6,7,8,9,10)
print(result)

    # 2) 특정 매개변수를 먼젖 작성하고 뒤로 여러개의 매개변수 작성
def add_mul(choice, *args) :        # 여러개의 매개변수와 특정 매개변수가 존재할 때
    print(choice) # 1개의 자료 매개변수
    print(args)   # 여러개의 자료를 갖는 튜플(매개변수)
    if choice == "add" :        # 만약에 매개변수 값이 add이면
        result = 0
        for i in args :
            result += i         # 누적 합계
    elif choice == "mul" :      # 만약에 매개변수 값이 mul 이면
        result = 1
        for i in args :
            result *= i         # 누적 곱
    return result               # 반환값

result = add_mul("mul",1,2,3,4,5)   # choice = "mul", args = (1,2,3,4,5)
print(result)
result = add_mul("add",1,2,3,4,5)   # choice = "add", args = (1,2,3,4,5)
print(result)

# 5. 키워드 매개변수, kwargs 키워드, **
# 인수로 전달된 key 와 value 를 딕셔너리의 매개변수로 받는다.
def print_kwargs(**kwargs) :
    print(kwargs)       # {'a' : 1} 딕셔너리 타입으로 매개변수를 받는다.

print_kwargs(a=1)       # 인수로 전달 시 key 와 value 로 전달
print_kwargs(name="foo",age = 3)

# 6. 함수의 리턴 값은 언제나 하나이다. 여러개 일때는 [], (), {} 활용
# 1)
def add_and_mul(a,b) :
    t = 1, 2            # () 생략 시 튜플로 생성된다.
    print(t)            # (1,2)
    return a+b, a*b

# 호출
result = add_and_mul(3,4)
print(result)           # (7, 12), 튜플 1개(튜플 안에 요소 2개)

# 2) 동일한 수준의 return 은 하나만 존재해도 된다.
def add_and_mul(a,b) :
    return a + b
    # return a * b        # 위에 리턴이 존재하므로 해당 리턴은 실행 X

# 3) 서로 다른 수준의 return 은 여러 개 존재할 수 있다.
def add_and_mul(a,b) :
    if a < 0 :
        return         # 만약에 a 가 0보다 작으면 함수 강제 종료, 아래 코드는 실행 X
    return a + b

# 7. 매개변수에 초기값 미리 설정하기
    # 주의할 점 : 초기화하고 싶은 매개변수는 항상 뒤쪽에 놓아야한다.
        # say_myself(name, age, man = True) [O]
        # say_myself(name, man = True, age) [X] -> 인자값과 매개변수 식별이 불가능
def say_myself(name, age, man=True) :       # 함수 정의
    print(f"나의 이름은 {name}입니다.")
    print(f"나이는 {age}살입니다.")
    if man :
        print("남자입니다.")
    else :
        print("여자입니다.")

# 함수 호출
    # 만약에 해당 매개변수의 인자값이 없으면 default (초기값)값이 대입된다.
say_myself("박응용",27)    # 나의 이름은 박응용입니다. 나이는 27살입니다. 남자입니다.
say_myself("박응용",25,False)  # 나의 이름은 박응용입니다. 나이는 25살입니다. 여자입니다.

# 8. 함수 안에서 선언한 변수의 효력 범위
    # 함수 안에서 사용하는 매개변수는 함수 밖의 변수 이름과는 전혀 상관이 없다.
a = 1           # 전역변수 'a'
def vartest(a) :
    a += 1      # 지역변수 'a'  a = 2인데 지역변수는 함수 호출 종료 시 사라진다.

vartest(a)
print(a)        # 1 -> 전역변수 'a'의 값 확인

    # 함수 안에서 함수 밖 변수를 활용하는 방법
        # 1) *** return *** (권장)
a = 1
def vartest(a) :
    a += 1
    return a    # 지역변수는 함수 호출 종료 시 사라지므로 함수를 호출했던 곳으로 반환
a = vartest(a)
print(a)        # 2
        # 2) global : 함수 밖 변수를 함수 안으로 호출할 때 사용하는 키워드
a = 1
def vartest() :
    global a    # 함수 밖에 있는 변수 a를 함수 안으로 호출
    a += 1
vartest()
print(a)        # 2

        # 3) 함수 밖에서 함수 안으로 접근 가능하지만, 함수 안에서 함수 밖으로는 접근 불가능
b = 1
def vartest() :
    c = b + 1   # 함수 밖에 있는 b 변수를 함수 안에서 호출, global 없이도 가능
    return c

b = vartest()
print(b)        # 2