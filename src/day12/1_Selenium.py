# day12 > 1_Selenium.py

# 1. 모듈 가져오기
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

"""
> selenium 모듈 설치
    > 방법 1. from bs4 에 커서를 두고 빨간 느낌표 출력 후 -> install package
    > 방법 2. 상단 메뉴 -> file -> python interpreter -> [+] 버튼 클릭 후 selenium 검색 후 패키지 선택 -> 설치
        > pip : 파이썬에서 패키지 소프트웨어를 설치 / 관리하는 시스템
"""
def coffeeBean_store(result) :
    # 2. webdriver 객체 생성
    wd = webdriver.Chrome()

    # 3. webdriver 객체를 이용한 웹페이지 접속, .get(URL)
    # wd.get("http://www.hanbit.co.kr")
    for i in range(1, 10) :
        # 실습 : 커피빈 매장 정보(동적 웹 페이지 = JS 이벤트) 크롤링
        # 1. 커피빈 웹페이지 연결
        wd.get("https://www.coffeebeankorea.com/store/store.asp")
        time.sleep(2)   # n초간 일시 정지(대기 상태)
        try:
            # 2. 커피빈 웹 페이지의 자바스크립트 함수 호출, .execute_script("JS함수 호출")
            wd.execute_script(f"storePop2({i})")  # 31번 매장인 "삼성 봉은사거리점" 모달 창이 열림
            time.sleep(2)   # n초간 일시 정지(대기 상태)  # 스크립트가 실행이 끝날 떄까지 2초 대기

            # 3. 자바스크립트 함수가 수행된 페이지의 소스 코드를 저장
            html = wd.page_source

            # 4. Beautiful 객체 생성
            soupCB1 = BeautifulSoup(html, "html.parser")

            # 5. html 소스 확인
            # print(soupCB1.prettify())

            # 6. 특정 매장 정보의 모달 창에서 매장 정보 파싱하기
            store_name_h2 = soupCB1.select("div.store_txt > h2")
            # print(store_name_h2)    # [<h2>삼성봉은사거리점</h2>]

            store_name = store_name_h2[0].string
            # print(store_name)       # 삼성봉은사거리점

            store_info = soupCB1.select("div.store_txt > table.store_table > tbody > tr > td")
            # print(store_info)
            """
            [<td> 평일 07:00-22:30 | 주말/공휴일 07:00-22:00</td>, 
            <td>건물뒷편주차장(기계주차식)<br/>평일 최초 30분 2,000원 / 1시간 5,000원 (구매영수증 지참시 30분 2,000원 / 1시간 3,500원)<br/>1시간 초과시 10분당 1,000원 (평일,주말 동일)</td>, 
            <td>서울시 강남구 영동대로 607 1,2층  <!--span class="lot">(서울시 강남구 영동대로 607 1,2층)</span--></td>, 
            <td>02-3443-5618</td>, <td class="best">식약처 인증 위생등급 매우 우수매장</td>, 
            <td class="hallcake">홀케익 당일 수령가능</td>]
            """
            store_address_list = list(store_info[2])
            # print(store_address_list)   # ['서울시 강남구 영동대로 607 1,2층  ', 'span class="lot">(서울시 강남구 영동대로 607 1,2층)</span']

            store_address = store_address_list[0]
            # print(store_address)    # 서울시 강남구 영동대로 607 1,2층

            store_phone = store_info[3].string
            # print(store_phone)      # 02-3443-5618

            # 매장 정보의 리스트 선언해서 매장 정보 담기
            store = [store_name, store_address, store_phone]
            result.append(store)
        except Exception as e:
            print(e)

    # for end
    return result


def main() :
    result = []
    coffeeBean_store(result)
    print(result)
    # pandas 이용한 2차원 리스트를 DataFrame 객체로 생성
    CB_tbl = pd.DataFrame(result, columns=["store", "address", "phone"])
    # DataFrame 객체 정보를 csv 파일로 저장
    CB_tbl.to_csv("coffeeBean.csv", encoding="utf-8", mode="w", index=True)

if __name__ == "__main__" :
    main()