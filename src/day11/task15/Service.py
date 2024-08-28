# day11 > task15 > Service.py

# http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship

# 1. BeautifulSoup 이용한 쿠우쿠우 전국 매장 정보 크롤링
# 2. 전국 쿠우쿠우 매장 정보(번호, 매장명, 연락처, 주소, 영업시간)
# 3. pandas 이용한 csv 파일로 변환
# 4. Flask 를 이용한 쿠우쿠우 전국 매장 정보를 반환하는 HTTP 매핑 정의
    # URL : (ip 주소):5000/qooqoo
    # getMapping
    # 3번을 통해 생성된 csv 파일을 읽어서 json 형식으로 반환

"""
1. URL 확인
http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship&&page=1
http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship&&page=2
....
http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship&&page=6
매개변수 파악 -> http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship&&page={매개변수}

2. 정보의 html 식별자 확인
    1) 정보가 있는 위치가 tbody
    2) <tr> 한 개당 매장 정보 홀수 : pc , 짝수 : 모바일
    3) <td> 하나의 매장에 각 속성 [1] 번호 [2] 지점 [3] 연락처 [4] 주소 [5] 영업시간
    4) 연락처, 주소, 영업시간 데이터는 <td> 안에 <a> 안에 있다.
    5) 지점은 <td> -> <div> -> <a> 2번째에 있다.

3. BeautifulSoup 이용한 구현
"""


# 1. 모듈 가져오기
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import json

# [1] 쿠우쿠우 매장 정보 가져오기
def qooqoo_store_info(result) :
    for page in range(1, 7) :

        # 2. 지정한 url 을 호출해서 응답받기
        url = f"http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship&&page={page}"
        resp = urllib.request.urlopen(url)
        if resp.getcode() == 200 :
            print(">> 통신 성공")
            # 3. 통신 응답 결과를 읽어와서 크롤링 파싱하기
            soup = BeautifulSoup(resp.read(), "html.parser")
            # print(soup)

            # 4. 분석한 HTML 식별자들을 파싱, find, findall, select, select_one
            # 4-1 테이블 전체 파싱
            tbody = soup.select_one("tbody")
            # print(tbody)

            # 4-2 테이블(전체 매장)마다 행(각 매장) 파싱
            rows = tbody.select("tr")
            # print(rows)

            # 4-3 행(각 매장)마다 열(각 매장의 정보) 파싱
            for row in rows :
                # print(row)

                # 4-4. 열(각 매장의 정보) 파싱
                cols = row.select("td")
                # print(cols)

                # 만약 열의 갯수가 1개이면 모바일이라고 가정하고 파싱 제외
                if len(cols) <= 1 :
                    continue

                # 각 정보들을 파싱
                num = cols[0].string.strip()
                name = cols[1].select("a")[1].string.strip()    # 2번째 열에 2개의 <a> 가 존재하는데 2번째 <a> 태그의 텍스트 파싱
                phone = cols[2].select_one("a").string.strip()
                address = cols[3].select_one("a").string.strip()
                time = cols[4].select_one("a").string.strip()

                # 4-5. 리스트에 담기
                list = [num, name, phone, address, time]
                # print(list)
                result.append(list)

        else :
            print(">> 통신 실패")
    # 5. 리스트 반환
    return

# [2] 2차원 리스트를 csv 반환해주는 서비스, 데이터, csv 파일명, 열(제목) 목록
def list2d_to_csv(result, fileName, colsNames) :
    try :
        # 1. import pandas as pd
        # 2. 데이터 프레임 객체 생성
        df = pd.DataFrame(result, columns=colsNames)
        # 3. 데이터 프레임 객체를 csv 파일로 생성
        df.to_csv(f"{fileName}.csv", encoding="utf-8", mode="w")
        return True
    except Exception as e :
        print(e)
        return False

# [3] 파일을 JSON 형식의 python 타입으로 가져오기, 매개변수로는 파일명
def read_csv_to_json(fileName) :
    # 1. pandas 의 dataFrame 을 이용해서 csv 파일 읽어오기
    df = pd.read_csv(f"{fileName}.csv",encoding="utf-8",engine="python",index_col=0)
        # index_col = 0 : pandas 의 dataFrame 형식 유지 (테이블 형식)
    # 2. dataFrame 객체를 JSON 으로 가져오기
    jsonResult = df.to_json(orient="records", force_ascii=False)
        # to_json() : dataFrame 객체 내 데이터를 JSON 변환 함수
            # orient = "records" -> 각 행마다 하나의 JSON 객체로 구성하겠다는 의미
            # force_ascii = False -> JSON 파일을 만들 때 아스키 문자 대신에 원래의 문자를 사용하겠다는 의미, True (아스키 코드), False(유니코드 utf-8)
    # 3. JSON 타입을 python 타입으로 변환
    result = json.loads(jsonResult)  # json.loads() 문자열 타입(JSON 형식) ----> python 타입(JSON 형식) 변환
    return result
# 서비스 테스트 확인 구역
# if __name__ == "__main__" :
#     result = []
#     qooqoo_store_info(result)
#     print(result)
#     list2d_to_csv(result,"전국_쿠우쿠우_매장", ["번호", "지점명", "연락처", "주소", "영업 시간"])
#     # csv 파일을 json 형식으로 가져오는 서비스 호출
#     result2 = read_csv_to_json("전국_쿠우쿠우_매장")
#     print(result2)