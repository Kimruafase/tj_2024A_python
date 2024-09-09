# day17 > 4_한글_기사_분석.py
import urllib.request

# 주제 : 다음 경제 뉴스의 최신 10페이지 기사들 제목의 단어 빈도 수 분석

from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. 데이터 준비
text_data = []
for page in range(1,11) :
    url = f"https://news.daum.net/breakingnews/economic?page={page}"
    resp = urllib.request.urlopen(url)
    html_data = resp.read()

    soup = BeautifulSoup(html_data, "html.parser")
    # print(soup)
    # print(soup)
    # print(soup.select("a"))
    list_news2 = soup.select_one(".list_news2")
    for a in list_news2.select("li") :
        # print(a.select_one(".tit_thumb > a").string)
        title = a.select_one(".tit_thumb > a").string
        text_data.append(title)

# print(text_data)

# 2. 품사 태깅
    # 2 - 0. 정규 표현식
message = ""
for i in text_data :
    message += re.sub(r"[^\w]", " ", i)

okt = Okt()
tag_words = okt.nouns(message)
# print(tag_words)

# 3. 분석(빈도수)
    # 3 - 1. 빈도수 분석
word_counts = Counter(tag_words)

    # 3 - 2. 상위 n개 추출
most_commons = word_counts.most_common(30)
# print(most_commons)

word_dict = {}
for w , c in most_commons :
    if len(w) > 1 :
        word_dict[w] = c

# 4. 시각화, (히스토그램, 워드 클라우드)
wc = WordCloud("c:/windows/fonts/malgun.ttf", background_color="white").generate_from_frequencies(word_dict)

plt.imshow(wc)
plt.show()