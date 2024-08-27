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

def QooQoo_store(result) :
    n = 0
    for page in range(1,7) :
        url = f"http://www.qooqoo.co.kr/bbs/board.php?bo_table=storeship&&page={page}"
        resp = urllib.request.urlopen(url)
        htmlData = resp.read()
        soup = BeautifulSoup(htmlData, "html.parser")
        # print(soup)
        tbody = soup.select_one("tbody")
        if not tbody:
            continue
        # print(tbody)
        tr = tbody.select("tr")
        for row in tr :
            tds = row.select("td")
            # print(tds)
            if len( tds ) <= 1 :
                continue
            #print( tds )
            num = tds[0].string.strip()
            name = tds[1].select('a')[1].string.strip()
            phone = tds[2].select_one('a').string.strip()
            address = tds[3].select_one('a').string.strip()
            time = tds[4].select_one('a').string.strip()
            #print( name )
            result.append([num, name, phone, address, time])
            # num = tds[0].text
            # print(num)


            # print(row)
        # print(tr)
        #n += 1
        #print(n)
        # tr = tbody.select("tr")
        # print(tr)
        # print()
        # print(tr[0])
        # print(tr[0].text)


        # for i in tr :
        #     print(i.select_one(".td-num").text)
        #     n += 1
        # print(tr[1])
        # for row in tbody.select("tr") :
        #     # print(row)
        #     tds = row.select("td")
        #     print(tds)
        #     num = tds[0].text
        #     print(num)
        #     name = tds[1].text
        #     print(name)
            # phone = tds[2].string
            # print(phone)
            # address = tds[3].string
            # print(address)
            # time = tds[4].string
            # print(time)


def main() :
    result = []
    print("QooQoo store crawling >>>>>>>>>>>>>>>>>>>")
    QooQoo_store(result)
    print(result)
    QooQoo_tb1 = pd.DataFrame(result, columns=("num", "name", "phone", "address", "time"))
    QooQoo_tb1.to_csv("QooQoo.csv", encoding="cp949",mode= "w", index=True)



if __name__ == "__main__" :
    main()