# day08 > task10 > App.py

from flask import Flask # 1. 플라스크 모듈 가져오기
from flask_cors import CORS # 3. CORS 모듈 가져오기

app = Flask(__name__)   # 2. 플라스크 객체 생성

CORS(app)   # 4. 모든 HTTP 경로의 CORS 허용

# 5. 매핑, Controller 가져오기
from Controller import *


if __name__ == "__main__" : # 6. Flask 실행
    app.run(debug=True)



