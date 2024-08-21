# Task1.py


# 함수 정의, def 함수명(매개변수, 매개변수) :

# 전역 변수
names = ""     # 샘플 데이터
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
    global names    # 전역변수 호출
    newName = input("이름을 입력하세요")    # 저장할 새로운 이름 입력받기
    # 첫 들록일 시 가장 앞에 쉼표(",")가 없어도 된다.
        # 삼항연산자 : 참 if 조건문 else 거짓
        # 문자열.count(문자) : 해당 문자열 내 문자 갯수 반환
    names += f",{"" if names.count(",") == 0  else ","}{newName}"   # "," (쉼표) 여러 개의 이름을 구분짓는 구분문자 (CSV 형식)
    return

def nameRead() :
    # for 반복변수 in 리스트명 : 리스트 내 요소 하나씩 반복변수에 대입
    # for 반복변수 in 문자열 : 문자열 내 요소 하나씩 반복변수에 대입
    # 문자열.split("특정문자") : 문자열 내 특정문자 기준으로 분해해서 리스트로 반환하는 함수
    for name in names.split(",") :
        print(f"name : {name}")     # f포메팅 : f"문자열{코드}문자열" # js 의 `문자열${코드}` 와 유사하다
    return

def nameUpdate() :
    global names    # 전역변수 호출
    # 문자열(불변성 특징), 부분 수정 불가능, 문자열 내 중간에 다른 문자열 수정 불가
    # 만약에 동일한 문자열을 찾아서 새로운 문자열로 변경
    oldName = input("oldName : \n")
    if names.find(oldName) == -1 :
        return
    else :
        newName = input("newName : \n")
        # names = names.replace(oldName,newName)
        newNames = ""
        for name in names.split(",") :  # 이름 하나씩 반복
            if name == oldName :            # 수정할 이름과 같다면
                newNames += f"{""if newNames == "" else " ,"}{newName}"    # 새로운 이름 대입
            else :
                newNames += f"{""if newNames == "" else " ,"}{name}"   # 기존 이름 그대로 대입
        names = newNames
    return

def nameDelete() :
    global names    # 전역변수 호출
    # 만약에 동일한 문자를 찾아서 ""로 변경
    deleteName = input("deleteName : \n")
    # 문자열.find(문자) : 문자열 내 찾을 문자가 존재하면 인덱스 반환, 없으면 -1 반환
    if names.find(deleteName) == -1 :
        return
    else :
        # 문자열.replace(기존 문자, 새로운 문자) : 문자열 내 기존 문자가 존재하면 새로운 문자로 치환해서 반환
        # names = names.replace(f",{deleteName}", "").strip()
        newNames = ""
        for name in names.split(",") :
            if name == deleteName :
                continue
            else :
                newNames += f"{""if newNames == "" else " ,"}{name}"
        names = newNames
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