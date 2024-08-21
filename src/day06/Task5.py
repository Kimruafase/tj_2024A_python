# Task5.py


# 함수 정의, def 함수명(매개변수, 매개변수) :

# 새로운 조건 : 파일처리 프로그램이 종료되도 기존의 데이터가 저장될 수 있도록 파일처리하시오.



# 전역 변수
names = []  # 샘플 데이터
    # 하나의 변수에 여러개의 이름을 저장하는 방법
    # 변수란? 하나의 자료에 저장하는 메모리 공간
    # 하나의 자료에 여러가지 속성을 담는 방법 : 1. 객체 2. JSON, CSV 형식의 문자열 3. 리스트 4. 튜플
        # 타입(자료 분류) vs 형식(자료 모양)
        # "10" : 문자열 타입, 숫자 형식
        # 10   : 정수 타입, 숫자 형식
        # "{key : value}" : 문자열 타입, JSON 형식
        # {key : value}   : JSON or 딕셔너리 타입, JSON or 딕셔너리 형식
    # CSV 란? 몇 가지 필드를 쉼표(",")로 구분한 텍스트
        # CSV : 필드 구분은 ","로 하고 객체 구분은 "\n"
        # ex : 유재석20강호동30 -> 유재석,20\n 강호동,30\n


def dataLoad() :
    f = open("data.txt", "r")       # 파일 읽기모드로 객체 반환
    name = f.read()           # 파일 내 제이터 전체 읽어오기, 파일객체.read~~()
    for line in name.split("\n")[ : len(name.split("\n"))-1] :  # 읽어온 파일 내용을 \n 기준으로 분해 \n 으로 객체 구분하기 때문에
        # 해당 줄에 쉼표 분해로 [0] 이름 [1] 나이로 구분해서 딕셔너리 생성
        dic = {"name" : line.split(",")[0], "age" : line.split(",")[1]}
        names.append(dic)
    f.close()
    return names

def dataSave() :                # 데이터를 파일 내 저장하기, 사용처는 nameCreate, nameUpdate, nameDelete 3곳
    f = open("data.txt","w")    # 파일 쓰기 모드로 객체 반환
    outStr = ""
    # 파이썬의 딕셔너리 -> 문자열 만들고 파일쓰기
    for name in names :
      outStr += f"{name["name"]},{name["age"]}\n"   # 딕셔너리를 CSV 형식의 문자열로 반환 ","로 필드 구분, "\n"로 객체 / 딕셔너리 구분
    f.write(outStr)                                 # 파일 객체 이용한 데이터 쓰기, 파일객체.write(data)
    f.close()
    return

def nameCreate() :
    name = input("이름을 입력해주세요. \n")
    age = input("나이를 입력해주세요. \n")
    names.append({"name": name, "age" : age})
    dataSave()
    return names

def nameRead() :
    for name in names:
        print(f"name : {name.get("name")}")  # 딕셔너리 변수명에 [key]나 .get(key) 사용
        print(f"age : {name.get("age")}")
    return

def nameUpdate() :
    oldName = input("수정할 이름을 입력해주세요. \n")
    for name in names:
        if oldName in name.get("name"):  # 만약 name.get("name") 통해 나온 value 가 oldName 이 포함된다면
            newName = input("새로운 이름을 입력해주세요. \n")  # 새로운 이름을 입력받아서
            newAge = input("새로운 나이를 입력해주세요. \n")    # 새로운 나이를 입력받아서
            name["name"] = newName  # 그 부분에 해당하는 key 의 value 에 새로운 이름을 대입
            name["age"] = newAge
            dataSave()
            return names
    return

def nameDelete() :
    deleteName = input("삭제할 이름을 입력해주세요. \n")
    for name in names:
        if deleteName in name.get("name"):  # 만약 name.get("name") 통해 나온 value 가 deleteName 이 포함된다면
            names.remove(name)  # 그에 해당하는 리스트의 요소를 삭제
            dataSave()
            return names
    return


dataLoad()
while True :    # 무한 루프 # {} 대신 : 과 들여쓰기(tab)을 사용해서 구분 # True 소문자가 아니고 대문자로 해야함
    # int() : 문자열 타입 -> 정수형 타입 반환 함수
    # input() : 입력 함수, 입력 받은 데이터를 문자열 반환
    # ch : "ch" 변수에 특정한 타입을 작성 or 명시하지 않는다
    ch = int(input("1. create 2. read 3. update 4. delete \n"))
    if ch == 1 :    # 만약에, 조건문
        # 주의할 점 : 들여쓰기 (tab)에 주의해야한다.
    # 들여쓰기 1번 -> while 문에 포함
        # 들여쓰기 2번 -> while 문 안에 if 문에 포함
        nameCreate()
    elif ch == 2 :
        nameRead()
    elif ch == 3 :
        nameUpdate()
    elif ch == 4 :
        nameDelete()
    else :
        print("프로그램을 종료합니다.")
        break