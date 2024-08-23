# day08 > 3_Flask_Cors.py

"""
    CORS : 교차 출처 자원 공유
        > Cross - Origin Resource Sharing
        > 현재 주소에서 다른 주소로부터 통신 요청하고 현재 주소로 응답 받기

    HTTP 통신
        > (유재석) 안녕 ---- 요청 ---->
                    <---- 응답 ----
        > :8080 -------------------> :8080
                <------------------

    CORS 통신 제한
        > (유재석) 안녕 ---- 요청 ----> (강호동)
                    <---- 응답 ----
        > :5000 ------------------> :5000
          :8080 <------------------ :8080

    CORS 허용
        > (1) CORS 설치
            > 방법 1 : from flask_cors import CORS -> install package
            > 방법 2 : 상단 메뉴 -> file -> python interpreter -> [+] 버튼 클릭 후 Flask-Cors 검색 후 패키지 선택 -> 설치
                > pip : 파이썬에서 패키지 소프트웨어를 설치 / 관리하는 시스템

        > (2) Flask-Cors 모듈 가져오기
            > from flask_cors import CORS

        > (3) CORS 허용
            CORS(app)


"""

from flask_cors import CORS
from flask import Flask

app = Flask(__name__)

CORS(app) # 모든 경로에 대해 CORS 허용

@app.route("/", methods=["GET"])
def index1() :
    return "Hello Python Flask CORS"

if __name__ == "__main__" :
    app.run(debug=True)