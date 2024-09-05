# day16 > 3_영문_분석.py

# 한국학술연구학술정보원(https://riss.kr) 에서 ai 검색해서
# 해외학술논문에서 작성언어가 "영어"인 500개 논문 엑셀 다운받아서 진행

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
from statsmodels.iolib.summary import summary
from wordcloud import STOPWORDS, WordCloud
from xlrd import xldate

# glob 메소드를 이용해서 문자열 exportExcelData 이 포함된 모든 파일 이름을 저장함
all_files = glob.glob("exportExcelData*.xls")
# print(all_files)

# 엑셀파일을 읽어서 담을 리스트 선언
all_files_data = []

# 엑셀 파일 이름이 담기 리스트를 반복문 돌려서
# pd.read_excel()로 하나씩 엑셀 파일 읽고
# 읽은 엑셀 파일을 리스트에 저장
for file in all_files :
    data_frame = pd.read_excel(file)
    all_files_data.append(data_frame)

# print(all_files_data)

# 전체 읽은 DataFrame을 pd.concat()을 통해 합침
all_files_data_concat = pd.concat(all_files_data, axis = 0, ignore_index=True)
# print(all_files_data_concat)

# 합친 DataFrame을 csv 파일로 저장
all_files_data_concat.to_csv("AI_bigdata.csv", encoding="utf-8",index = False)

title = all_files_data_concat["제목"]
# print(title)

eng_stop_words = stopwords.words("english")
# print(eng_stop_words)
lemma = WordNetLemmatizer()

words_list = []

for t in title :
    # print(t)
    eng_words = re.sub(r"[^a-zA-Z]", " ", str(t))
    # print(eng_words)

    eng_words_token = word_tokenize(eng_words.lower())
    # print(eng_words_token)

    eng_words_token_stop = [word for word in eng_words_token if word not in eng_stop_words]
    # print(eng_words_token_stop)

    eng_words_token_stop_lemma = [lemma.lemmatize(word) for word in eng_words_token_stop]
    # print(eng_words_token_stop_lemma)

    words_list.append(eng_words_token_stop_lemma)

# print(words_list)

words_list2 = reduce(lambda x , y : x + y, words_list)
# print(words_list2)

words_count = Counter(words_list2)
# print(words_count)

words_count_dic = dict()

for t, c in words_count.most_common(52) :
    if len(str(t)) > 1:
        words_count_dic[t] = c

# print(words_count_dic)
del words_count_dic["intelligence"]
del words_count_dic["artificial"]

# print(words_count_dic)

plt.bar(range(len(words_count_dic)), words_count_dic.values())
plt.xticks(range(len(words_count_dic)), list(words_count_dic.keys()), rotation = 85)

# plt.show()

all_files_data_concat["doc_count"] = 0

summary_year = all_files_data_concat.groupby("출판일", as_index=False)["doc_count"].count()
# print(summary_year)

plt.plot(range(len(summary_year)), summary_year["doc_count"])
plt.xticks(range(len(summary_year)), [t for t in summary_year["출판일"]], rotation = 85)

# plt.show()

stopwords = set(STOPWORDS)

wc = WordCloud(stopwords= stopwords).generate_from_frequencies(words_count_dic)
plt.imshow(wc)
plt.axis("off")

plt.show()
