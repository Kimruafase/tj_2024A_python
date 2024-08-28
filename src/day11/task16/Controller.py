# [1] 플라스크 객체 가져오기
from App import app
# [2] (우리가 만든) 서비스 모듈 가져오기
from Service import *
# app.run 코드 위에 HTTP 매핑 주소 정의
@app.route('/jobkorea', methods=['get'])
def jobkorea():
    #(1) 만약 크롤링 된 csv 파일이 없거나 최신화 하고 싶을 대
    list2d_to_csv()

    #(2) csv 저장된 데이터를 JSON 으로 가져오기
    result2 = read_csv_to_json('jobkorea')
    #(3) 서비스로부터 받은 데이터로 http 응답하기
    return result2

@app.route('/count', methods=['get'])
def jobCount():
    #(1) 만약 크롤링 된 csv 파일이 없거나 최신화 하고 싶을 대
    result=load()
    return result