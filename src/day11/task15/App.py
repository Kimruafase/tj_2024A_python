# day11 > task15 > App.py

# 1. Flask 모듈 가져오기

from flask import Flask

# 2. Flask 객체 생성, # 1과 # 2의 코드 고정
app = Flask(__name__)

# 2-1. CORS 허용, 서로 다른 port 간의 데이터 통신 허용
from flask_cors import CORS
# 모든 HTTP 에 대해 CORS 허용
CORS(app)

# 4. Controller 모듈 가져오기
from Controller import  *

# 3. Flask 웹 실행
if __name__ == "__main__" :
    app.run(host="0.0.0.0", debug=True)
    # http://127.0.0.1:5000
    # http://localhost:5000
    # http://192.168.30.239:5000