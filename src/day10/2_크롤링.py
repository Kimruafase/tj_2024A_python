# day10 > 2_크롤링.py

from bs4 import BeautifulSoup # 모듈 가져오기
import urllib.request

# [실습 1] http://quotes.toscrape.com

url = "http://quotes.toscrape.com"      # 크롤링할 url
resp = urllib.request.urlopen(url)      # 지정한 url 요청 후 응답 받기
htmlData = resp.read()                  # 응답받은 내용물 전체 읽어오기
# print(htmlData)                       # 확인용

soup = BeautifulSoup(htmlData,"html.parser")    # 지정한 html 문자열로 html 파싱 객체 생성
# print(soup.prettify())                               # 확인용

# 특정 마크업 / 태그 파싱
quoteDivs = soup.select(".quote")
for quote in quoteDivs :
    # 각 명언의 문구만 추출
    print(quote.select_one(".text").string)

    # 각 명언의 저자만 추출
    print(quote.select_one(".author").string)


    # 각 명언의 태그 추출
    for tag in quote.select(".tag") :
        print(tag.string , end="\t")

    print("\n")


# [실습 2] https://v.daum.net/v/20240827074833139

url1 = "https://v.daum.net/v/20240827074833139"
resp1 = urllib.request.urlopen(url1)
htmlData1 = resp1.read()

soup1 = BeautifulSoup(htmlData1, "html.parser")
# print(soup1)

# 파싱하기
ps = soup1.select("p")
# print(ps)

# 기사 제목
# print(soup1.select_one(".tit_view").string)
# print(soup1.select_one(".news_view").text)

# for p in ps :
#     # 본문 내용 프린트
#     print(p.text)

# [3] 부평구 날씨 https://search.naver.com/search.naver?&query=%EB%B6%80%ED%8F%89%EA%B5%AC+%EB%82%A0%EC%94%A8
text = "부평구 날씨"
url2 = f"https://search.naver.com/search.naver?&query={urllib.parse.quote(text)}"
resp2 = urllib.request.urlopen(url2)
htmlData2 = resp2.read()
# print(htmlData2)
soup2 = BeautifulSoup(htmlData2, "html.parser")
# print(soup2)

# 온도 추출
print(soup2.select_one(".temperature_text"))
    # <div class="temperature_text"> <strong><span class="blind">현재 온도</span>27.2<span class="celsius">°</span></strong> </div>
print(soup2.select_one(".temperature_text").text)   # 현재 온도27.2°

# 습도 추출
print(soup2.select_one(".summary_list").select(".sort")[1].text)    # 습도 68%