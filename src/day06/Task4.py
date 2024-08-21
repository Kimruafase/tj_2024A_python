# Task2.py


# 함수 정의, def 함수명(매개변수, 매개변수) :

# 전역 변수
names = {"유재석" : "유재석", "강호동" : "강호동", "신동엽" : "신동엽" }  # 샘플 데이터
    # 하나의 변수에 여러개의 이름을 저장하는 방법
    # 변수란? 하나의 자료에 저장하는 메모리 공간
    # 하나의 자료에 여러가지 속성을 담는 방법 : 1. 객체 2. JSON, CSV 형식의 문자열 3. 리스트 4. 튜플
        # 타입(자료 분류) vs 형식(자료 모양)
        # "10" : 문자열 타입, 숫자 형식
        # 10   : 정수 타입, 숫자 형식
        # "{key : value}" : 문자열 타입, JSON 형식
        # {key : value}   : JSON or 딕셔너리 타입, JSON or 딕셔너리 형식
    # CSV 란? 몇 가지 필드를 쉼표(",")로 구분한 텍스트
def nameCreate() :
    name = input("이름을 입력해주세요. \n")
    names[name] = name
    return names

def nameRead() :
    nameList = list(names.values())
    for name in nameList :
        print(f"name : {name}")
    return

def nameUpdate() :
    oldName = input("수정할 이름을 입력해주세요. \n")
    if oldName in names :
        newName = input("새로운 이름을 입력해주세요. \n")
        names[oldName] = newName
        names[newName] = names[oldName]
        del names[oldName]
        return names
    return

def nameDelete() :
    deleteName = input("삭제할 이름을 입력해주세요. \n")
    if deleteName in names :
        del names[deleteName]
        return names
    return

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