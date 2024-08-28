

# [1] App.py 에서 Flask 객체 가져오기
from App import app

# [2] (내가 만든) Service 모듈 가져오기
import Service

@app.route("/qooqoo", methods=["GET"])  # http://localhost:5000/qooqoo
def qooqoo_store():
    # (1) 만약에 크롤링 된 CSV 파일이 없거나 최신화를 하고 싶을 때
    result = []
    Service.qooqoo_store_info(result)   # 크롤링해서 CSV 파일 생성
    Service.list2d_to_csv(result,"전국_쿠우쿠우_매장", ["번호", "지점명", "연락처", "주소", "영업시간"])

    # (2) CSV 에 저장된
    result2 = Service.read_csv_to_json("전국_쿠우쿠우_매장")

    # (3) Service 로 부터 받아온 데이터로 HTTP 응답하기
    return result2