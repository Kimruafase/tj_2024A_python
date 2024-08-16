# 1_파일_읽기_쓰기.py

# 1. 파일 생성하기, open(파일 이름, 열기 모드)
    # 해당 파일 객체를 반환해주는 함수
    # 열기 모드 : r -> 읽기, w -> 쓰기, a -> 추가
    # 파일 열기 : 파일 객체 변수 = open(파일 이름, 열기 모드)
    # 파일 닫기 : 파일 객체 변수.close()

# 1) 파일 열기
f = open("새파일.txt", "w") # 쓰기 모드의 파일 객체 반환 함수
print(f)    # <_io.TextIOWrapper name='새파일.txt' mode='w' encoding='cp949'>

# 2) 파일 닫기
f.close()

# 3) 파일을 쓰기 모드로 열어서 내용 쓰기 -> 파일 객체 변수.write(내용)
f = open("C:/doit/새파일.txt", "w")    # 해당 경로의 파일을 쓰기모드로 열어서 객체 반환
    # 쓰기
for i in range(1,11) :  # 1부터 11 미만까지 -> 1 - 10까지 반복
    # 탭 키 주의
    data = f"{i}번째 줄입니다.\n"
    # 파일에 내용 쓰기
    f.write(data)

f.close()

# 4) 파일을 읽는 여러가지 방법
    # [1] .readline
    # 파일의 첫번째 줄을 읽어오는 함수
f = open("C:/doit/새파일.txt", "r")    # 해당 경로의 파일을 읽기모드로 열어서 객체 반환
line = f.readline()                   # 1번째 줄입니다.
print(line)
while True :    # 무한루프
    line = f.readline()     # 1줄씩 읽어온다
    if not line :           # 읽어온 문자가 "" 공백이면
        break               # 무한루프 종료
    print(line)             # 아니면 읽어온 문자 출력

f.close()       # 파일 닫기

    # [2] .readlines
    # 파일의 한줄씩 요소로 읽어와서 리스트로 반환
f = open("C:/doit/새파일.txt", "r")
lines = f.readlines()   # 한 줄당 요소 1개씩 해서 리스트로 반환함
print(lines)
for line in lines : # 리스트 요소를 하나씩 반복 변수에 대입하여 반복 처리
    print(line)

f.close()   # 파일 닫기

    # [3] .read
    # 파일의 내용 전체를 문자열로 반환하는 함수
f = open("C:/doit/새파일.txt", "r")
data = f.read()         # 파일 내 내용 전체를 문자열로 읽어온다.
print(data)

f.close()   # 파일 닫기

# 4. 파일 객체와 for 문
    # 파일 객체는 기본적으로 for 문과 함께 사용하여 줄 단위로 읽을 수 있다.
f = open("C:/doit/새파일.txt", "r")
for str in f :      # 파일 객체 내 한줄씩 반복 변수에 대입하여 반복 처리한다.
    print(str)

f.close()

# 5. 파일에 새로운 내용 추가
f = open("C:/doit/새파일.txt", "a")    # "a" 는 추가모드로 파일 객체를 반환함
for value in range(11,20) :           # 11부터 20 미만 -> 11 - 19
    data = f"{value}번째 줄입니다.\n"
    f.write(data)
f.close()

# 6. with, with 자료 as 변수 :  with 절에서 자료를 획득하고 사용한 다음 반납하는 구조
# 파일은 항상 파일을 열고 작업이 끝나면 파일 닫기를 해야한다.
    # with 자료 생성 as 변수 :
        # 해당 자료를 변수에 대입하고 with 종료되면 자동으로 변수는 초기화

    # open된 파일을 f 변수에 대입하고 with 작업이 종료되면 f 변수도 초기화, close 된다.
with open("foo.txt","w") as f :
    f.write("Life is too short, you need python")
# day04 폴더에 foo 라는 txt 파일 생성 됐는지 내용 확인