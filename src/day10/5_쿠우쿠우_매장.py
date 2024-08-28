# day10 > 5_쿠우쿠우_매장.py

# http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship

# 1. BeautifulSoup 이용한 쿠우쿠우 전국 매장 정보 크롤링
# 2. 전국 쿠우쿠우 매장 정보(번호, 매장명, 연락처, 주소, 영업시간)
# 3. pandas 이용한 csv 파일로 변환
# 4. Flask 를 이용한 쿠우쿠우 전국 매장 정보를 반환하는 HTTP 매핑 정의
    # URL : (ip 주소):5000/qooqoo
    # getMapping
    # 3번을 통해 생성된 csv 파일을 읽어서 json 형식으로 반환

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from flask import Flask# 1. 플라스크 모듈 가져오기
from flask_cors import CORS # 3. CORS 모듈 가져오기

def QooQoo_store(result) :
    # 페이지 수 만큼 반복문 진행
    for page in range(1, 7) :
        # url 주소 page -> 페이지 번호
        url = f"http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship&&page={page}"
        # urllib 의 요청 객체의 urlopen 메소드에 url 보내서 응답 객체에 저장
        resp = urllib.request.urlopen(url)
        # 응답 객체를 읽어서 htmlData 변수에 저장
        htmlData = resp.read()
        # BeautifulSoup 을 통해 html 파싱하고 soup 변수에 저장
        soup = BeautifulSoup(htmlData, "html.parser")
        # print(soup)
        # "tbody" 하나 셀렉트해서 tbody에 html 저장
        tbody = soup.select_one("tbody")
        # "tbody" 가 아니라면 반복문으로 돌아감
        if not tbody:
            continue
        # print(tbody)
        # "tbody" 안에서 "tr" 마크업 선택해서 리스트 저장
        tr = tbody.select("tr")
        # "tr" 마크업 리스트 반복문 돌림
        for row in tr :
            # 리스트의 반복변수 row 의 "td" 마크업 선택해서 tds 리스트에 저장
            tds = row.select("td")
            # print(tds)
            # "td" 마크업 선택한 변수의 길이가 1 이하라면 가장 최근의 반복문으로 돌아감(모바일 전용 <td> 라고 판단)
            if len( tds ) <= 1 :
                continue
            #print( tds )
            # tds 리스트의 첫번째 인덱스의 양쪽 공백 제거 후 num에 대입
            num = tds[0].string.strip()
            # tds 리스트의 두번째 인덱스에서 "a" 태그 마크업 선택 후 양쪽 공백 제거 후 쉼표를 띄어쓰기로 변경 후 name에 대입
            name = tds[1].select('a')[1].string.strip().replace(",", " ")
            # tds 리스트의 세번째 인덱스에서 "a" 태그 마크업 선택 후 양쪽 공백 제거 후 phone에 대입
            phone = tds[2].select_one('a').string.strip()
            # tds 리스트의 네번째 인덱스에서 "a" 태그 마크업 선택 후 양쪽 공백 제거 후 쉼표를 띄어쓰기로 변경 후 address에 대입
            address = tds[3].select_one('a').string.strip().replace(",", " ")
            # tds 리스트의 다섯번째 인덱스에서 "a" 태그 마크업 선택 후 양쪽 공백 제거 후 쉼표를 띄어쓰기로 변경 후 time에 대입
            time = tds[4].select_one('a').string.strip().replace(",", "")
            #print( name )
            # num, name, phone, address, time 의 값을 담은 리스트를 result 리스트에 append 메소드를 통해 대입함.
            result.append([num, name, phone, address, time])
            # num = tds[0].text
            # print(num)


def main() :
    # 크롤링한 데이터 받을 리스트 선언
    result = []
    print("QooQoo store crawling >>>>>>>>>>>>>>>>>>>")
    # 리스트를 QooQoo_store 메소드에 매개변수로 보내서 리스트에 크롤링한 데이터 담음
    QooQoo_store(result)
    # 크롤링한 데이터가 제대로 담아 왔는 지 확인
    print(result)
    # pandas 의 DataFrame 을 통해 2차원 배열로 만듬
    QooQoo_tb1 = pd.DataFrame(result, columns=("num", "name", "phone", "address", "time"))
    # 2차원 배열을 csv 파일로 생성
    QooQoo_tb1.to_csv("QooQoo.csv", encoding="cp949",mode= "w", index=False)

app = Flask(__name__)

CORS(app) # 모든 경로에 대해 CORS 허용

def load():
    list =[]
    f = open("QooQoo.csv","r")      # QooQoo.csv 파일 열기
    next(f)                         # 파일 첫 줄 스킵
    readlines = f.read()            # 파일 전체 가져오기
    rows = readlines.split("\n")    # "\n" 기준으로 자르기
    for i in rows :                 # 반복문
        if i :
            cols = i.split(",")     # "," 기준으로 자르기
            dic = {
                "num" : cols[0],                # 1번째 인덱스에 번호
                "name" : cols[1],               # 2번째 인덱스에 이름
                "phone" : cols[2],              # 3번째 인덱스에 전화번호
                "address" : cols[3],            # 4번째 인덱스에 주소
                "time" : cols[4].strip("\"")    # 5번째 인덱스에 시간 \"으로 따옴표 제거
            }
            list.append(dic)                # 생성한 딕셔너리를 리스트에 대입
    f.close()                           # 파일 닫기
    print(f"리스트는 {list}")            # 리스트 확인용
    return list                         # 리스트 반환

@app.route("/qooqoo", methods=["GET"])
def index() :
    data = load()                   # 리스트를 data 변수에 대입
    return data                     # data 변수 반환

if __name__ == "__main__" :
    main()
    app.run(debug=True)