

from flask import Flask # 1. 플라스크 모듈 가져오기
from flask_cors import CORS # 3. CORS 모듈 가져오기

app = Flask(__name__)   # 2. 플라스크 객체 생성

CORS(app)   # 4. 모든 HTTP 경로의 CORS 허용.

class apartment():
    def __init__(self,시군구,단지명,전용면적,계약년월,계약일,거래금액,층):
        self.시군구 = 시군구
        self.단지명 = 단지명
        self.전용면적 = 전용면적
        self.계약년월 = 계약년월
        self.계약일 = 계약일
        self.거래금액 = 거래금액
        self.층 = 층

@app.route("/", methods=["GET"])
def load() :
    list = []
    f = open("아파트(매매)_실거래가_20240823153532.csv", "r")  # 파일 읽기 모드
    next(f)  # 첫번째 줄 스킵
    readlines = f.read()  # 파일 읽기
    rows = readlines.split("\n")  # 행 구분해서 저장
    for i in rows :
        if i :
            cols = i.split(",")             # 쉼표 구분해서 저장
            dic = apartment(cols[1],cols[5],cols[6],cols[7],cols[8],cols[9],cols[12])
            list.append(dic)
    return list



def condition2() :
    list2 = []
    list = load()
    for i in list :
        if max() == i.거래금액 :
            dic = {"시군구" : i.시군구, "전용면적" : i.전용면적, "단지명" : i.단지명}
            list2.append(dic)
    for i in list :
        if min(i.거래금액) == i.거래금액 :
            dic = {"시군구": i.시군구, "전용면적": i.전용면적, "단지명": i.단지명}
            list2.append(dic)
    return list2

# print(condition2())

if __name__ == "__main__" : # 6. Flask 실행
    app.run(debug=True)