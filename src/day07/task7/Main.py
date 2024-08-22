# day07 > task7 > Main.py

from User import Name

# 전역 변수
names = []  # 샘플 데이터

def nameCreate() :
    name = input("이름을 입력해주세요.\n")
    age = input("나이를 입력해주세요.\n")
    new = Name(name, age)
    return names.append(new)

def nameRead() :
    for i in names :
        print(f"name : {i.name}, age : {i.age}")
    return

def nameUpdate() :
    oldName = input("수정할 이름을 입력해주세요.\n")
    for i in names :
        if oldName == i.name :
            newName = input("새로운 이름을 입력해주세요.\n")
            newAge = input("새로운 나이를 입력해주세요.\n")
            i.name = newName
            i.age = newAge
            return names
    return

def nameDelete() :
    deleteName = input("삭제할 이름을 입력해주세요.\n")
    for i in names :
        if deleteName == i.name :
            names.remove(i)
            return names
    return


# 해당 파일을 다른 파일에서 호출했을 때 호출되지 않는 구역
    # 해당 파일을 직접 실행했을 때 실행되는 구역
    # 해당 파일을 다른 파일에서 호출할 때 실행되지 않는 구역(모듈)
if __name__ == "__main__" :
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