#day10 > 3_할리스커피_매장.py

# 1. 모듈
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd



# result = [] # 할리스 매장 정보 리스트를 여러 개 저장하는 리스트 변수 선언
#
# for page in range(1,51) : # 1 ~ 50 까지 반복
#     # 할리스 매장 정보 url
#     url = f"https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={page}"
#     resp = urllib.request.urlopen(url)
#     htmlData = resp.read()
#     soup = BeautifulSoup(htmlData, "html.parser")
#     # print(soup)
#     tbody = soup.select_one("tbody")
#     # print(tbody)
#     for row in tbody.select("tr") :
#         # print(row)
#         tds = row.select("td")
#         store_sido = tds[0].string
#         # print(store_sido)
#         store_name = tds[1].string
#         # print(store_name)
#         store_address = tds[3].string
#         # print(store_address)
#         store_phone = tds[5].string
#         # print(store_phone)
#         store = [store_name,store_sido,store_address,store_phone]
#         result.append(store)    # 리스트 안에 리스트 추가, 2차원 리스트 [[], [], []]
#
# print(result)

# [CODE 1]
def hollys_store(result) :
    for page in range(1, 51):  # 1 ~ 50 까지 반복
        # 할리스 매장 정보 url
        url = f"https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={page}"
        resp = urllib.request.urlopen(url)
        htmlData = resp.read()
        soup = BeautifulSoup(htmlData, "html.parser")
        # print(soup)
        tbody = soup.select_one("tbody")
        if not tbody:
            continue
        # print(tbody)
        for row in tbody.select("tr"):
            if len(row) <= 3 :
                break
            tds = row.select("td")
            print(tds)
            store_sido = tds[0].string
            # print(store_sido)
            store_name = tds[1].string
            # print(store_name)
            store_address = tds[3].string
            # print(store_address)
            store_phone = tds[5].string
            # print(store_phone)
            store = [store_name, store_sido, store_address, store_phone]
            result.append(store)  # 리스트 안에 리스트 추가, 2차원 리스트 [ [], [], [] ]


# [CODE 0]
def main() :
    result = []
    print("Hollys store crawling >>>>>>>>>>>>>>>>>>>")
    hollys_store(result)    # [CODE 1] 호출
    # print(result)
    # hollys_tb1 = pd.DataFrame(result, columns = ("store", "sido-gu","address", "phone"))
    # hollys_tb1.to_csv("C:/Users/tj-bu-703-17/Desktop/tj_2024A_python/src/day10/hollys1.csv", encoding="cp949",mode= "w", index=True)

if __name__ == "__main__" :
    main()