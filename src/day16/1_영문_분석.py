# day16 > 1_영문_분석.py
from lzma import LZMAFile

import pandas as pd
import glob
import re
from functools import reduce
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt
from pandas.core.config_init import styler_precision
from wordcloud import STOPWORDS, WordCloud

# 최초 1번만 실행

import nltk
# nltk.download()

# [1] 여러 개의 파일명을 불러오기, glob.glob() -> 특정 패턴과 일치한 파일명을 모두 찾는 함수
    # * : 와일드 카드(모든 문자 대응), myCabinetExcelData* : myCabinetExcelData 로 시작하는 파일명 검색
all_files = glob.glob("myCabinetExcelData*.xls")
# print(all_files)  # 확인 후 주석

# [2] 여러개 파일명에 해당하는 엑셀파일을 호출해서 pd로 변환하기, 엑셀파일 -> pd
all_files_data =[]
for file in all_files : # 모든 파일명을 하나씩 반복한다.
    # print(file)
    df = pd.read_excel(file)    # 엑셀 모듈 : xlrd 모듈 설치
    # print(df)
    all_files_data.append(df)   # 울러온 엑셀 DataFrame 을 리스트에 담는다.

# print(all_files_data)

# [3] DataFrame 합치기,    .concat(여러 개의 프레임이 저장된 리스트, axis = 0(세로) 1(가로))
all_files_data_concat = pd.concat(all_files_data, axis=0, ignore_index=True)
# print(all_files_data_concat)

# [4] DataFrame 을 csv 로 변환 / 내보내기
all_files_data_concat.to_csv("riss_bigdata.csv", encoding="utf-8", index=False)

# > (프로젝트 목표 : 학술 문서의 제목 분석) 데이터 전처리
# [5] DataFrame 의 제목 열만 추출
all_title = all_files_data_concat["제목"]
# print(all_title)

# [6] 단어 토큰화 준비
    # stopwords.words("english") : "영어" 불용어 목록 가져오는 함수
    # WordNetLemmatizer() : 표제어 추출기 객체 생성
        # 표제어 : 단어의 원형(기본형) 찾는 과정, ex_ running -> run, better -> good 변환
        # 시제, 단 / 복수, 진행어 등등의 일반화 과정
eng_stop_words = stopwords.words("english")
# print(eng_stop_words)
lemma = WordNetLemmatizer()

# [7] 단어 토큰화
words = []
for title in all_title :    # 제목 목록에서 제목 하나씩 반복하기
    # print(title)
    # [7-1] 영문이 아닌 것을 정규 표현식을 이용해서 치환
    eng_words = re.sub(r"[^a-zA-Z]", " ", str(title))
    # print(eng_words)

    # [7-2] 소문자로 변환 후 토큰화, word_tokenize(문자열) : 지정한 문자열을 토큰(단어) 추출하여 리스트로 변환
    eng_words_token = word_tokenize(eng_words.lower())
    # print(eng_words_token)

    # [7-3] 불용어 제거 (해당 토큰 리스트에 불용어가 포함되어 있으면 제외)
    # 반복문을 이용한 조건에 다른 새로운 리스트 생성
        # 리스트 컴프리헨션 사용 X
    # eng_words_token_stop = []           # 불용어가 제거된 토큰을 저장하는 리스트
    # for w in eng_words_token :
    #     if w not in eng_stop_words :    # 해당 토큰(단어)이 불용어 목록에 포함되어 있지 않다면
    #         eng_words_token.append(w)

        # 리스트 컴프리헨션 사용 O
            # if 값 in 리스트     -> 리스트 내 해당 값이 있다면 True 아니면 False
            # if 값 not in 리스트 -> 리스트 내 해당 값이 없다면 True 아니면 False
    eng_words_token_stop = [w for w in eng_words_token if w not in eng_stop_words]

    # [7-4] 표제어 추출, 표제어 객체.lemmatize(단어) -> 단어에서 시제, 단 / 복수, 진행형 등을 일반화 단어로 추출
        # 리스트 컴프리헨션 사용 O
        # 불용어가 제거된 리스트(eng_words_token_stop)에서 표제어 추출
    eng_words_token_stop_lemma = [lemma.lemmatize(w) for w in eng_words_token_stop]

        # 리스트 컴프리헨션 사용 X
    # eng_words_token_stop_lemma = []
    # for w in eng_words_token_stop :
    #     # 불용어가 제거된 리스트(eng_words_token_stop)에서 표제어 추출
    #     eng_words_token_stop_lemma.append(lemma.lemmatize(w))

    # print(eng_words_token_stop_lemma)
    # 정규화 -> 토큰화 -> 불용어 제거 -> 표제어 추출한 결과를 리스트에 담기
    words.append(eng_words_token_stop_lemma)

# 반복문 종료되고나서 제대로 담겼는지 확인
# print(words)

# [8] 2차원 리스트를 1차원으로 변환, reduce
    # reduce 사용 O, reduce(람다식 함수, 2차원 리스트)
words2 = reduce(lambda x, y : x+y, words)
# print(words2)

"""
> 파이썬 람다식   # lambda 매개변수1, 매개변수2 : 실행문
    > 매개변수의 제곱을 하는 함수를 람다식 표현
변수명 = lambda x : x**2     # JS : x => x**2    # JAVA : x -> x**2 
"""
# square = lambda x : x**2
# print(square(2))    # 4


    # reduce 사용 X
# words2 = []
# for w in words :
#     # 리스트1.extend(리스트2) -> 두개의 리스트를 하나의 리스트로 반환하는 함수
#     words2.extend(w)
# print(words2)

# [9] 리스트 내 요소 갯수 세기 (단어 빈도 구하기)
    # Count(리스트) : 리스트 내 요소들의 빈도수를 튜플로 해서 여러 개의 튜플을 가진 리스트로 반환해주는 함수
word_count = Counter(words2)
    # Count(리스트) 결과 : Counter({단어 : 수}, {단어 : 수}, {단어 : 수})
# print(word_count)

# [10] 빈도 수가 높은 것만 추출, 빈도 수가 높은 상위 50개 단어 추출
    # most_common(50) 결과 : [('단어', '수'), ('단어', '수'), ('단어', '수')]
# print(word_count.most_common(50))

word_count2 = dict()

# for i in word_count.most_common(50) :
#     print(i)

for tag, counts in word_count.most_common(50) :
    if len(str(tag)) > 1 :      # 만약 단어 길이가 1 미만 시 제외
        word_count2[tag] = counts

print(word_count2)
"""
> 파이썬의 반복문 리스트와 튜플
    1. for i in list / tuple / str :
    2. for i1, i2 in tuple : 
"""
# [11] 히스토그램
# plt.bar(x축값, y축값)
    # 딕셔너리.keys()   : 딕셔너리 내 모든 key 값 호출해서 반환
    # 딕셔너리.values() : 딕셔너리 내 모든 value 값 호출해서 반환
    # x축에 단어(keys), y축에는 단어의 빈도수
    # 딕셔너리 정렬 방법 : sorted(딕셔너리, key = 정렬기준, reverse = True)
    # key = word_count2.get 은 get 메소드를 참조하여 value(빈도수) 기준으로 정렬
    # reverse = True 는 내림차순을 뜻한다. 기본값은 오름차순
sorted_keys = sorted(word_count2, key = word_count2.get, reverse = True)
# print(sorted_keys)    # ['data', 'big', 'analytics', 'analysis']
sorted_values = sorted(word_count2.values(), reverse = True)
# print(sorted_values)  # [1645, 1354, 137, 67]

# range(0, 50) : 0 ~ 49까지
plt.bar(range(len(word_count2)), sorted_values, align = "center")
plt.xticks(range(len(word_count2)), list(sorted_keys), rotation = 85)

# plt.show()

# [12] 결과 시각화
    # DataFrame 의 필드(열) 추가
all_files_data_concat["doc_count"] = 0
    # DataFrame 에서 "출판일" 열 기준으로 그룹화하고
    # as_index = False : 그룹화할 때 인덱스는 제외하겠다는 의미
    # .count() : 행 갯수
summary_year = all_files_data_concat.groupby("출판일", as_index = False)["doc_count"].count()
print(summary_year)

plt.figure(figsize = (12, 5))
plt.xlabel("year")
plt.ylabel("doc-count")

plt.grid(True)

plt.plot(range(len(summary_year)), summary_year["doc_count"])
plt.xticks(range(len(summary_year)), [text for text in summary_year["출판일"]])

# plt.show()

# [13] 워드 클라우드
    # 문자열 타입의 텍스트들의 워드 클라우드
        # wc = WordCloud().generate("문자열 타입")
    # 딕셔너리 타입의 텍스트들의 워드 클라우드
        # wc = WordCloude().generate_from_frequencies("딕셔너리 타입")
stopwords = set(STOPWORDS)

wc = WordCloud(background_color="ivory", stopwords= stopwords, width=800, height=600)
cloud = wc.generate_from_frequencies(word_count2)
plt.figure(figsize=(8, 8))
plt.imshow(cloud)
plt.axis("off")

plt.show()

# 워드 클라우드 결과 이미지를 저장하기
cloud.to_file("워드_클라우드.jpg")