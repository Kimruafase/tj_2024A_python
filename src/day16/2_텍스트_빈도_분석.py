#day16 > 2_텍스트_빈도_분석.py

import re                           # 파이썬에 내장된 라이브러리, 정규표현식에 사용
from collections import Counter     # 컬렉션(리스트 / 딕셔너리 / 집합)

from nltk.corpus import words

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. 분석할 텍스트 준비
textData = """Big data refers to the large volume of data – both structured and unstructured – that inundates a business on a day-to-day basis.
But it’s not the amount of data that’s important. It’s what organizations do with the data that matters.
Big data can be analyzed for insights that lead to better decisions and strategic business moves."""

# 2. 다양한 전처리
    # (1) 정규화 : 모든 대소문자를 소문자로 변환
    # "문자열".lower() -> 문자열을 소문자로 변경
    # "문자열".upper() -> 문자열을 대문자로 변경
textData = textData.lower()
# print(textData)

    # (2) 정규화2 : 구두점(. , ? ! : ; ' " () 등)과 불필요한 특수문자 / 기호 제거 -> 정규 표현식 사용
    # "\w" : 문자 혹은 숫자, "\s" : 공백(스페이스 바, 탭) 의미, "^" : 부정의 의미
    # ex_ [^\w\s] : 문자, 숫자, 공백이 아닌 것을 찾는다는 의미
    # re.sub(r"정규표현식", "대체문자", "기존문자")
    # 기존 문자열에서 정규 표현식을 이용한 문자를 찾아 대체하는 함수
textData = re.sub(r"[^\w\s]", "", textData)
print(textData)

    # (3) 문자열을 토큰(단어)화
words = textData.split(" ") # 띄워쓰기 기준으로 문자 구분
print(words)

# 3. 문자 갯수 세기
word_count = Counter(words) # 중복된 요소들의 갯수를 반환해주는 함수
print(word_count)           # [(단어, 갯수), (단어, 갯수)]

# 4. 빈도가 높은 단어 상위 n개 만큼 출력, .most_common(n) : 상위 n개를 반환해주는 함수
print(word_count.most_common(5))    # [('data', 5), ('the', 3), ('that', 3), ('to', 2), ('of', 2)]

# 5. 시각화
    # (1) 워드_클라우드 객체 생성, WordCloud(width = 가로사이즈, height = 세로사이즈, background_color = 배경색).generate(시각화할 문자열)
word_cloud = WordCloud(width=800, height=800, background_color="white").generate(textData)

    # (2) 차트 보기
plt.imshow(word_cloud)
plt.axis("off") # 축 숨기기
plt.show()