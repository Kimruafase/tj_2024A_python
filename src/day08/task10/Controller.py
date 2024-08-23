# day08 > task10 > Controller.py

from App import app # Flask 객체 호출
from Service import personData # Service 파일에서 personData 클래스 가져오기


@app.route("/", methods=["GET"])
def index() :
    data = personData() # Service 처리 후 결과 받기
    # for i in data:  # 반복문
    #     ratio = i.ratio(i.people, i.man)  # 반복변수의 ratio 메소드 호출해서 반복변수의 people 객체와 man 객체 매개변수로 보내고 계산값 반환받음
    #     data.append(ratio)
    # 파이썬 객체로는 JSON 전송이 불가능하다.

    # 방법 1. 일반적인 파이썬의 반복문 활용해서 리스트 생성
    # 파이썬 객체를 딕셔너리로 변경, 객채명.__dict__
    # newData = []
    # for o in data :
    #     dic = o.__dict__
    #     newData.append(dic)

    # 방법 2. map() 활용해서 새로운 리스트 생성
    return list(map(lambda o : o.__dict__, data))