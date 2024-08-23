# day08 > task11 > App.py

"""
    삼성전자주가.csv 파일의 정보를 테이블 형식으로 localhost:8080/index3.html 에 출력
        > 1. csv 파일을 읽어서 딕셔너리[행]로 만들기
        > 2. 플라스크 이용한 해당 정보 HTTP 매핑 정의
        > 3. Spring 서버에서 AJAX 이용한 플라스크 서버로 부터 삼성전자 주가 정보 JSON 형식으로 응답 받기
"""

from flask import Flask # 1. 플라스크 모듈 가져오기
from flask_cors import CORS # 3. CORS 모듈 가져오기

app = Flask(__name__)   # 2. 플라스크 객체 생성

CORS(app)   # 4. 모든 HTTP 경로의 CORS 허용.

def load() :
    list = []
    f = open("삼성전자주가.csv", "r")         # 파일 읽기 모드
    next(f)                                 # 첫번째 줄 스킵
    readlines = f.read()                    # 파일 읽기
    rows = readlines.split("\n")            # 행 구분해서 저장
    for i in rows :
        if i :
            cols = i.split(",")             # 쉼표 구분해서 저장
            # 딕셔너리에 저장
            dic = {"일자" : cols[0].strip("\""),
                   "종가" : format(int(cols[1].strip("\"")),','),
                   "대비" : cols[2].strip("\""),
                   "등락률" : cols[3].strip("\""),
                   "시가" : format(int(cols[4].strip("\"")),','),
                   "고가" : format(int(cols[5].strip("\"")),','),
                   "저가" : format(int(cols[6].strip("\"")),','),
                   "거래량" : format(int(cols[7].strip("\"")),','),
                   "거래대금" : format(int(cols[8].strip("\"")),','),
                   "시가총액" : format(int(cols[9].strip("\"")),','),
                   "상장주식수" : format(int(cols[10].strip("\"")),',')}
            list.append(dic)                # 리스트에 저장
    f.close()
    return list

@app.route("/", methods=["GET"])
def index() :
    data = load()
    return data

if __name__ == "__main__" : # 6. Flask 실행
    app.run(debug=True)