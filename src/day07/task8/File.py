# day07 > task8 > File.py

import Main
from User import User
def dataLoad() :
    names = []
    try :       # 예외가 발생할 것 같은 코드
        f = open("data.txt", "r")       # 파일 읽기모드로 객체 반환
        name = f.read()           # 파일 내 제이터 전체 읽어오기, 파일객체.read~~()
        lines = name.split("\n")
        for i in lines :
            if i :
                cols = i.split(",")
                user = User(cols[0],cols[1])
                names.append(user)
        f.close()
        return names
    except FileNotFoundError :    # 예외가 발생했을 때 실행되는 구역
        return names

def dataSave(names) :                # 데이터를 파일 내 저장하기, 사용처는 nameCreate, nameUpdate, nameDelete 3곳
    f = open("data.txt","w",encoding="utf-8")    # 파일 쓰기 모드로 객체 반환
    outStr = ""
    # 파이썬의 딕셔너리 -> 문자열 만들고 파일쓰기
    for name in names :
        outStr += f"{name.name},{name.age}\n"   # 딕셔너리를 CSV 형식의 문자열로 반환 ","로 필드 구분, "\n"로 객체 / 딕셔너리 구분
    f.write(outStr)                                 # 파일 객체 이용한 데이터 쓰기, 파일객체.write(data)
    f.close()
    return