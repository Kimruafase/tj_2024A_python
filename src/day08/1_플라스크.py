# day08 > 1_플라스크.py

"""
    Flask
        > 파이썬으로 만들어진 웹 프레임워크 (vs JAVA Spring)
        > Flask vs 장고

    설치 방법
        > (1) flask 모듈 설치
            > 방법 1. from flask 에 커서를 두고 빨간 느낌표 출력 후 -> install package
            > 방법 2. 상단 메뉴 -> file -> python interpreter -> [+] 버튼 클릭 후 Flask 검색 후 패키지 선택 -> 설치
                > pip : 파이썬에서 패키지 소프트웨어를 설치 / 관리하는 시스템

        > (2) Flask 모듈 가져오기
            > from flask import Flask

        > (3) Flask 객체 생성
            > app = Flask(__name__)

        > (4) Flask 프레임워크 실행
            > if __name__ == "__main__" :
                app.run(debug=True)

        > HTTP GET 매핑
        @app.route("/")
        def index() :
            return

"""

# Flask 모듈 가져오기
from flask import Flask #

# Flask 객체 생성
app = Flask(__name__)

# HTTP GET 매핑 설정
@app.route("/")
def index() :
    return "Hello Flask"

# flask 웹 실행
if __name__ == "__main__" :
    app.run(debug=True)

# 콘솔 확인, port 번호 : 5000 http 주소 : 127.0.0.1:5000
# 테스트 (1) : 크롬 웹 주소에 http://127.0.0.1:5000 접속
# 테스트 (2) : Talend API 에 GET method 로 http://127.0.0.1:5000 접속
# 테스트 (3) : JS - AJAX 로 GET method 를 통해 http://127.0.0.1:5000 확인
"""
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 306-613-144
    127.0.0.1 - - [23/Aug/2024 10:16:03] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [23/Aug/2024 10:16:03] "GET /favicon.ico HTTP/1.1" 404 -
"""