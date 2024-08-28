# 취업공고 정보 파싱: 회사명, 공고명, 경력, 학력, 계약유형, 지역, 채용기간
# 페이지수 계산 총 채용공고수/페이지당 공고수
# 크롤링 한 결과를 csv 변환 서비스
# csv 파일을 json 변환 서비스
# spring에서 index5.html, py에서 task16> appstart.py, service.py, controller.py

# [1] [java]검색결과의 모든 채용공고를 spring web html 테이블 에 출력하시오.
# [2] py 서비스추가 총채용공고수, 경력별 공고수, 학력별 공고수를 [1]번 테이블 위에 출력 하시오.
# [3] html 에서 input 박스로 입력받아 검색 버튼을 클릭했을 대 입력받은 값으로 검색결과를 크롤링]

from flask import Flask # 1. 플라스크 모듈 가져오기
from flask_cors import CORS # 3. CORS 모듈 가져오기
app = Flask(__name__)   # 2. 플라스크 객체 생성
CORS(app)   # 4. 모든 HTTP 경로의 CORS 허용.

# controller 모듈 가져오기
from Controller import *


if __name__ == "__main__" : # 6. Flask 실행
    app.run(host='0.0.0.0', debug=True)
    # http://127.0.0.1:5000
    # http://localhost:5000
    # http://192.168.30.21:5000
# 서버 재실행시 직접 현재 실행 중지하기