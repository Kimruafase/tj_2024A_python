# day07 > task8 > Main.py


"""
    User.py : user 정보를 갖는 클래스 정의
    file.py : save(), load() 함수를 정의
    [조건 1] 이름과 나이를 입력받아 저장
    [조건 2] 프로그램이 종료되도 names 의 데이터가 유지되도록 파일처리
"""
from User import User
from File import *

names = [ ]
def nameCreate( ) :
    name = input("이름을 입력해주세요.\n")
    age = input("나이를 입력해주세요.\n")
    new = User(name, age)
    names.append(new)
    dataSave(names)
    return names

def nameRead( ) :
    for i in names :
        print(f"name : {i.name}, age : {i.age}")
    return

if __name__ == "__main__" :
    names = dataLoad()
    while True :
        ch = int( input('1.create 2.read') )
        if ch == 1 : nameCreate()
        elif ch == 2 : nameRead( )