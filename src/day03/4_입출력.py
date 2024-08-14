# 4_입출력.py

# 1. 사용자 입력, input() 함수
    # input("안내 문구")
    # 콘솔에 입력받은 값을 문자열(str)로 반환
    # 자료형 확인 함수 : type(데이터)
a = input()
print(a)
number = input("숫자를 입력하세요")
print(number)
print(type(number))

# 2. print() 함수 자세히 보기
    # print(리터럴 또는 변수명 또는 연산식)
    # print(f"문자열{리터럴 또는 변수명 또는 연산식}문자열") : f포메팅
    # print(리터럴 또는 변수명 또는 연산식, end = "출력 후 대입할 문자열"(기본 : \n))
print(123)          # 숫자 출력
print("python")     # 문자열 출력
print([1,2,3])      # 리스트 출력
print("python" + " is fun") # '+' 연산자를 이용한 문자열 연결
print("python", "is", "fun") # ','(쉼표)를 이용한 문자열 연결
print("python", end=" ")    # end = "\n" 이 기본값 이지만 변경이 가능하다.
print("is fun")
