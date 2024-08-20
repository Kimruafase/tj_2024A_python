# Task1.py
from os.path import split

# 문자열 활용 , p.50 ~ p.76
# [조건 1] : 각 함수들을 구현해서 프로그램 완성
# [조건 2] : 1. 이름을 입력 받아서 여러 명의 이름을 저장
#           2. 저장된 여러명의 이름을 모두 출력
#           3. 수정할 이름과 새로운 이름을 입력받아 수정
#           4. 삭제할 이름을 입력받아 존재하면 삭제

# 하나의 변수에 여러가지 정보를 담을 때 ","로 구분해서 담는다. 주로 CSV 파일 방식

names = ""      # 여러개의 name 들을 저장하는 문자열 변수.

def nameCreate() :
    name = input("이름을 입력해주세요. \n")
    return names + "," + name

def nameRead() :
    return print(names.split(","))  # 문자열 내 "," 기준으로 분해

def nameUpdate() :
    name = input("수정할 이름을 입력해주세요. \n")
    if names.count(name) >= 1 :
        newName = input("새로운 이름을 입력해주세요. \n")
        return names.replace(name,newName)
    return

def nameDelete() :
    name = input("삭제할 이름을 입력해주세요. \n")
    if names.count(name):
        return names.replace(name, "").strip()
    return


while True : # 무한루프
    ch = input(" 1. create 2. read 3. update 4. delete \n")
    if ch == "1" :
        names = nameCreate()
    elif ch == "2" :
        nameRead()
    elif ch == "3" :
        names = nameUpdate()
    elif ch == "4" :
        names = nameDelete()