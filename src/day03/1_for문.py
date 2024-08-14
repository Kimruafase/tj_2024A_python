# 1_for문.py

    # > while 문과 비슷한 반복문
    # > 한 눈에 들어온다는 장점이 있다.

# 1. for 문의 기본 구조

"""
for 변수 in 리스트(or 튜플, 문자열) :
    실행문
"""

# 예제1
test_list = ['one', 'two', 'three']
# 'test_list' 라는 변수가 ['one', 'two', 'three'] 를 참조한다.
# JS -> let test_list = ['one', 'two', 'three']
for i in test_list :
    # 콜론 다음의 실행문 작성 시 들여쓰기 주의, {} 가 없다.
    # 리스트 내 문자열을 하나씩 문자열 타입으로 반환해서 반복 처리한다.
    print(i)

"""
(JS 방식)
let test_list = ['one', 'two', 'three']
test_list.forEach(i=>{
    console.log(i);
})
for(let i in test_list){
    console.log(test_list[i]);
}
"""

# 예제2
a = [(1,2), (3,4), (5,6)]
# [요소1, 요소2, 요소3] : 리스트 타입 (여러 요소를 저장, 요소 수정 / 삭제 가능)
# (요소1, 요소2, 요소3) : 튜플 타입 (여러 요소를 저장, 요소 수정 / 삭제 불가능) -> 고정형
for (first, last) in a :
    # 리스트 내 튜플을 하나씩 (요소1, 요소2) 튜플 타입으로 반환 해서 반복 처리한다.
    print(first + last)

# 예제3
marks = [90, 25, 67, 45, 80]    # 학생들의 점수 리스트
number = 0                      # 학생들 번호
for mark in marks :
    # 들여쓰기 주의
    number += 1
    if mark >= 60 :     # 만약 mark번째 학생이 60점 이상이라면 아래 실행 아니라면 else 문 실행
        print(f"{number}번 학생은 합격입니다.")
    else :
        print(f"{number}번 학생은 불합격입니다.")
    # 파이썬의 if 조건문에는 () 가 없다.

# 예제4
# 2. continue : 가장 가까운 for 문의 처음으로 돌아가게 되는 키워드
marks1 = [90, 25, 67, 45, 80]
number1 = 0
for i in marks1 :
    number1 += 1
    if i < 60 :
        continue    # 아래 코드는 실행되지 않고 for 문의 처음으로 돌아감
    print(f"{number1}번 학생 축하합니다. 합격입니다.")

# 3. range() : 숫자 리스트를 생성하여 반환해주는 함수
    # range(숫자)                     : 0 부터 숫자 미만까지 포함하는 range 객체를 생성
    # range(시작 숫자, 끝 숫자)         : 시작 숫자부터 끝 숫자 미만까지 포함하는 range 객체 생성
    # range(시작 숫자, 끝 숫자, 증감식)  : 시작 숫자부터 끝 숫자 미만까지 증감식 만큼 증감하는 range 객체 생성
print(range(10))    # 0,1,2,3,4,5,6,7,8,9
print(range(1,11))  # 1,2,3,4,5,6,7,8,9,10


# 예제5
for value in range(10) :         # 0 - 9
    print(value, end=" ")        # print(    , end=" ") : 줄바꿈 처리를 하지 않는 출력문

print()

for value in range(1, 11) :      # 1 - 10
    print(value, end=" ")

print()

for value in range(1, 11, 2) :   # 1 3 5 7 9 (2씩 증가)
    print(value, end=" ")

print()

sum = 0
for i in range(1, 11) :
    sum += i

print(sum)

print()

sum1 = 0
for i in range(1, 101) :
    sum1 += i

print(sum1)

print()


# 예제6
for i in range(2, 10) :         # 단 (2 - 9)
    for j in range(1, 10) :     # 곱 (1 - 9)
        print(f"{i} x {j} = {i * j:>2}")
    print()

# 4. 리스트 컴프리헨션 사용
    # [] 안에서 for 문 사용
    # [ for 반복변수 in 리스트명 ]
    # [표현식 for 반복변수 in 리스트]
    # [연산식 for 반복변수 in 리스트]
    # 2개 이상도 가능
        # [표현식 for 항목1 in 반복가능객체1 if 조건문1
        #        for 항목2 in 반복가능객체2 if 조건문2]
# 예제7
a = [1,2,3,4]
result = [i * 3 for i in a]
print(result)

# 반복되고 있는 i 값을 하나씩 리스트 요소로 대입하여 리스트를 생성
result = [i for i in a]
print(result)

# 기존 리스트를 반복문을 활용하여 새로운 리스트 생성
print([i for i in a])       # JAVA / JS : 리스트명.map()

result = [num * 3 for num in a if num % 2 == 0]
print(result)

print()

result = [x * y for x in range(2 , 10)
                for y in range(1, 10)]
print(result)