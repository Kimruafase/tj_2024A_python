# 7_while.py

    # > 문장을 반복해서 수행해야 할 경우

    # 1. while 문의 기본 구조

"""
1. 자바
초기값;
while(조건문){
    실행문;
    증감식;
}

2. 파이썬
초기값
while 조건문 :
    실행문
    증감식
"""

# 예제 1
treeHit = 0
while treeHit < 10 :        # 변수가 10 미만이면 반복하고 아니면 반복을 종료한다는 뜻
    treeHit += 1            # 파이썬은 증감연산자가 없으므로 += 으로 처리함
    print(f'나무를 {treeHit}번 찍었습니다.')  # f 포메팅 : f'문자열{코드}문자열'
    if treeHit == 10 :
        print("나무가 넘어갔습니다.")
# while, if 문 사용할 때 주의할 점 : {} 없고 들여쓰기를 이용한 실행문을 제어문에 포함시켜야 함

"""
int treeHit = 0;
while(treeHit < 10){
    treeHit++;
    System.out.println("나무를 " + treeHit + "번 찍었습니다.")
    if(treeHit == 10){
        System.out.println("나무가 넘어갔습니다.")
    }
}
"""

# 2. while 문 만들기
number = 0              # 변수
while number != 4 :     # 변수가 4가 아니면 반복하고 4이면 종료
    print("1. ADD 2. DEL 3. LIST 4. QUIT")
    number = int(input())
    # input() : 콘솔에서 입력을 받는 함수
    # int()   : 자료를 정수 타입으로 반환하는 함수
    # while, if : 들여쓰기 주의

# 3. break 키워드 : 가장 가까운 반복문 강제 종료 vs return 함수 종료
coffee = 1 # 변수
while True :        # 무한루프, java : while(true){}
    money = int(input("돈을 넣어 주세요."))    # input('입력 전 출력 문구') : 콘솔에 입력된 값을 반환하는 함수
    # int(데이터) : 자료를 정수형으로 바꿔주는 함수, java : Integer.parseInt(), js : int()
    if money == 300 :                               # 300원을 받았다면
        print("돈을 받았으니 커피를 줍니다.")           # 커피를 줬다는 것을 출력
        coffee -= 1                                 # 커피 갯수 1 차감
        print(f"남은 커피의 양은 {coffee}개입니다.")    # 남은 커피 갯수 출력
    elif money > 300 :                              # 300원을 초과해서 받았다면
        print(f"거스름돈 {money - 300}원을 주고 커피를 줍니다.")  # 받은 돈 - 300원 계산해서 출력
        coffee -= 1                                 # 커피 갯수 1 차감
        print(f"남은 커피의 양은 {coffee}개입니다.")    # 남음 커피 갯수 출력
    else :                                             # 받은 돈이 300원 미만이라면
        print("돈을 다시 돌려주고 커피를 주지 않습니다.")    # 커피를 주지 않음을 출력
        print(f"남은 커피의 양은 {coffee}개입니다.")       # 남은 커피 갯수 출력
    if coffee == 0 :                                   # 남은 커피 갯수가 0개라면
        print("커피가 다 떨어졌습니다. 판매를 종료합니다...") # 판매를 종료함을 출력
        break

# 4. continue 키워드 : 가장 가까운 반복문으로 강제 이동
a = 0                   # 1번 초기값, 반복 변수
while a < 10 :          # 2번 조건문, 반복 조건
    a += 1              # 3번 증감식, 반복 변수를 1 증가
    if a % 2 == 0 :     # 반복 변수의 값이 짝수라면
        continue        # while 문으로 이동한다. continue 아래 코드는 실행 X
    print(a)            # 반복 변수가 짝수일 경우는 출력되지 않고 홀수만 출력된다.

# 5. 무한루프 : 조건이 항상 True 이므로 while 문 안에 있는 실행문을 무한히 수행하게 된다.
"""
while True :
    실행문
"""

