# day36 > 1_감성분석.py

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import warnings

from click.core import batch

warnings.filterwarnings(action="ignore")

import konlpy
from konlpy.tag import Kkma, Komoran, Okt

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Bidirectional

# 1. 데이터 다운로드
train_file = tf.keras.utils.get_file("rating_train.txt",    # 다운로드된 파일의 이름 저장
                                     origin="https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt",  # 파일 다운로드하는 url 주소
                                     extract=True)  # 만약 압축파일이면 자동으로 압축풀기 설정
# 2. 다운로드한 파일 읽기
train = pd.read_csv(train_file, sep="\t")

# 3. 데이터 확인
# print(train.shape)  # (150000, 3)
# print(train.head()) # id : 게시물 번호, document : 리뷰내용, label : 긍정, 부정
"""
         id                                           document  label
0   9976970                                아 더빙.. 진짜 짜증나네요 목소리      0
1   3819312                  흠...포스터보고 초딩영화줄....오버연기조차 가볍지 않구나      1
2  10265843                                  너무재밓었다그래서보는것을추천한다      0   
3   9045019                      교도소 이야기구먼 ..솔직히 재미는 없다..평점 조정      0
4   6483659  사이몬페그의 익살스런 연기가 돋보였던 영화!스파이더맨에서 늙어보이기만 했던 커스틴 ...      1
"""

# 4. label 별 개수
cnt = train["label"].value_counts()
# print(cnt)
"""
label
0    75173
1    74827
Name: count, dtype: int64
"""

# 5. label 별 비율 시각화
sns.countplot(x="label", data = train)
# plt.show()

# 6. 결측치 확인, 데이터가 없는 빈 값 확인, pd객체.isnull()
# print(train.isnull().sum())
"""
id          0
document    5
label       0
dtype: int64
"""

# 7. 결측지가 특정 label 값만 있는지 확인
# print(train[train["document"].isnull()])
"""
             id document  label
25857   2172111      NaN      1
55737   6369843      NaN      1
110014  1034280      NaN      0
126782  5942978      NaN      0
140721  1034283      NaN      0
"""

# 8. label 별 텍스트 길이
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
data_len = train[train["label"] == 1]["document"].str.len() # pd 객체 내 "label" 필드값이 1인 "document" 필드의 텍스트 길이 구하기
ax1.hist(data_len)  # 히스토그램 차트
ax1.set_title("positive")

data_len = train[train["label"] == 0]["document"].str.len() # pd 객체 내 "label" 필드값이 0인 "document" 필드의 텍스트 길이 구하기
ax2.hist(data_len)
ax2.set_title("negative")

fig.suptitle("Number of characters")
# plt.show()


# 9. 형태소 분석기 생성
# ex_ "오늘날씨어떄" -> "오늘", "날씨" vs "오늘날", "씨" -> 이처럼 띄어쓰기가 안 되어 있을 경우 형태소 분석이 어렵다.
kkma = Kkma()
komoran = Komoran()
okt = Okt()

text = "영실아안녕오늘날씨어때?"

def sample_ko_pos(text):
    print(f"==== {text} ====")
    print(f"kkma: {kkma.pos(text)}")
    print(f"komoran: {komoran.pos(text)}")
    print(f"okt: {okt.pos(text)}")

# sample_ko_pos(text)
"""
==== 영실아안녕오늘날씨어때? ====
kkma: [('영', 'MAG'), ('싣', 'VV'), ('아', 'ECD'), ('안녕', 'NNG'), ('오늘날', 'NNG'), ('씨', 'VV'), ('어', 'ECD'), ('때', 'NNG'), ('?', 'SF')]
komoran: [('영', 'NNP'), ('실', 'NNP'), ('아', 'NNP'), ('안녕', 'NNP'), ('오늘날', 'NNP'), ('씨', 'NNB'), ('어떻', 'VA'), ('어', 'EF'), ('?', 'SF')]
okt: [('영', 'Modifier'), ('실아', 'Noun'), ('안녕', 'Noun'), ('오늘날', 'Noun'), ('씨', 'Suffix'), ('어때', 'Adjective'), ('?', 'Punctuation')]
"""

text2 = "영실아안뇨오늘날씨어때?"

# sample_ko_pos(text2)
"""
==== 영실아안뇨오늘날씨어때? ====
kkma: [('영', 'MAG'), ('싣', 'VV'), ('아', 'ECD'), ('안', 'VV'), ('뇨', 'EFQ'), ('오늘', 'MAG'), ('날씨', 'NNG'), ('어', 'XSN'), ('때', 'NNG'), ('?', 'SF')]
komoran: [('영', 'NNP'), ('실', 'NNP'), ('아', 'NNP'), ('안', 'NNP'), ('뇨', 'NNG'), ('오늘날', 'NNP'), ('씨', 'NNB'), ('어떻', 'VA'), ('어', 'EF'), ('?', 'SF')]
okt: [('영', 'Modifier'), ('실아', 'Noun'), ('안뇨', 'Noun'), ('오늘날', 'Noun'), ('씨', 'Suffix'), ('어때', 'Adjective'), ('?', 'Punctuation')]
"""

text3 = "정말 재미있고 매력적인 영화에요 추천합니다."

# sample_ko_pos(text3)
"""
==== 정말 재미있고 매력적인 영화에요 추천합니다. ====
kkma: [('정말', 'MAG'), ('재미있', 'VA'), ('고', 'ECE'), ('매력적', 'NNG'), ('이', 'VCP'), ('ㄴ', 'ETD'), ('영화', 'NNG'), ('에', 'JKM'), ('요', 'JX'), ('추천', 'NNG'), ('하', 'XSV'), ('ㅂ니다', 'EFN'), ('.', 'SF')]
komoran: [('정말', 'MAG'), ('재미있', 'VA'), ('고', 'EC'), ('매력', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ㄴ', 'ETM'), ('영화', 'NNG'), ('에', 'JKB'), ('요', 'JX'), ('추천', 'NNG'), ('하', 'XSV'), ('ㅂ니다', 'EF'), ('.', 'SF')]
okt: [('정말', 'Noun'), ('재미있고', 'Adjective'), ('매력', 'Noun'), ('적', 'Suffix'), ('인', 'Josa'), ('영화', 'Noun'), ('에요', 'Josa'), ('추천', 'Noun'), ('합니다', 'Verb'), ('.', 'Punctuation')]
"""

# 텍스트 전처리(한글과 영어만 남기고 삭제)
    # regex = True -> 정규표현식 사용하겠다는 속성 추가
train["document"] = train["document"].str.replace("[^A-Za-z가-힣ㄱ-ㅎㅏ-ㅣ ]","", regex = True)
# print(train["document"].head())
"""
0                                    아 더빙 진짜 짜증나네요 목소리
1                           흠포스터보고 초딩영화줄오버연기조차 가볍지 않구나
2                                    너무재밓었다그래서보는것을추천한다
3                            교도소 이야기구먼 솔직히 재미는 없다평점 조정
4    사이몬페그의 익살스런 연기가 돋보였던 영화스파이더맨에서 늙어보이기만 했던 커스틴 던...
Name: document, dtype: object
"""

# 결측지 제거
train = train.dropna()
# print(train.shape)  # (149995, 3)

def word_tokenization(text):
    # 불용어 목록 : 관사, 전치사, 조사, 접속사 등 의미가 없는 단어 제거
    stop_words= ["는", "을", "를" ,"이", "가", "의", "던", "고", "하", "다", "은", "에", "들", "지", "게", "도"]

    # okt.morphs() : 리스트 반환 , okt.pos() : 튜플 반환
    return [word for word in okt.morphs(text) if word not in stop_words]

data = train["document"].apply((lambda x : word_tokenization(x)))   # document 열에 데이터 하나씩 불용어 제거 함수에 대입
# print(data.head())
"""
0                              [아, 더빙, 진짜, 짜증나네요, 목소리]
1        [흠, 포스터, 보고, 초딩, 영화, 줄, 오버, 연기, 조차, 가볍지, 않구나]
2                     [너, 무재, 밓었, 다그, 래서, 보는것을, 추천, 한]
3                  [교도소, 이야기, 구먼, 솔직히, 재미, 없다, 평점, 조정]
4    [사이, 몬페, 그, 익살스런, 연기, 돋보였던, 영화, 스파이더맨, 에서, 늙어,...
Name: document, dtype: object
"""

# train 과 validation 분할
training_size = 120000

# train 분할
train_sentences = data[:training_size] # 0 ~ 119999
valid_sentences = data[training_size:] # 119999 ~ 끝

# label 분할
train_labels = train["label"][:training_size] # 0 ~ 119999
valid_labels = train["label"][training_size:] # 119999 ~ 끝


# vocab_size 설정
tokenizer = Tokenizer()

tokenizer.fit_on_texts(data)
# print(f"총 단어 개수 : {len(tokenizer.word_index)}") # 총 단어 개수 : 102194

# threshold 횟수 이상만 vocab_size에 포함하게 설정하는 함수
def get_vocab_size(threshold):
    cnt = 0
    for x in tokenizer.word_counts.values():
        if x >= threshold:
            cnt += 1

    return cnt

vocab_size = get_vocab_size(5) # 5회 이상 출현한 단어
# print(f"vocab_size : {vocab_size}") # vocab_size : 22116

oov_tok = "<OOV>" # 사전에 없는 단어
vocab_size = 15000
tokenizer = Tokenizer(oov_token = oov_tok, num_words = vocab_size + 1)
tokenizer.fit_on_texts(data)
# print(tokenizer.word_index)
# print(f"단어 사전 개수 : {len(tokenizer.word_counts)}") # 단어 사전 개수 : 102194

# 문자를 숫자로 표현
# print(train_sentences[:2])
"""
0                          [아, 더빙, 진짜, 짜증나네요, 목소리]
1    [흠, 포스터, 보고, 초딩, 영화, 줄, 오버, 연기, 조차, 가볍지, 않구나]
"""
train_sequences = tokenizer.texts_to_sequences(train_sentences)
valid_sequences = tokenizer.texts_to_sequences(valid_sentences)
# print(train_sequences[:2])
"""
[[42, 428, 8, 6671, 635], [905, 430, 34, 576, 2, 183, 1547, 14, 957, 6109, 1]]
"""

# 문장의 최대 길이
# 모든 문장들의 길이가 일치하면 모델 성능에 도움이 된다. 최대 길이의 문자로 일치화
max_length = max(len(x) for x in train_sequences)
# print(f"문장의 최대 길이 : {max_length}")  # 문장의 최대 길이 : 69


# 문장 길이를 동일하게 맞추기
    # 길이를 초과하는 자료는 속성 : "post", 뒤에 자르기
    # 길이를 미달하는 경우 0으로 채우는 속성 : "post", 뒤에 채운다
trunc_type = "post"
padding_type = "post"

train_padded = pad_sequences(train_sequences, truncating= trunc_type, padding = padding_type, maxlen = max_length)
valid_padded = pad_sequences(valid_sequences, truncating= trunc_type, padding = padding_type, maxlen = max_length)

    # np.asarray() : 배열로 변환
train_labels = np.asarray(train_labels)
valid_labels = np.asarray(valid_labels)

# print(f"샘플 : {train_padded[:1]}")
"""
샘플 : [[  42  428    8 6671  635    0    0    0    0    0    0    0    0    0
     0    0    0    0    0    0    0    0    0    0    0    0    0    0
     0    0    0    0    0    0    0    0    0    0    0    0    0    0
     0    0    0    0    0    0    0    0    0    0    0    0    0    0
     0    0    0    0    0    0    0    0    0    0    0    0    0]]
"""

def create_model():
    model = Sequential([
        Embedding(vocab_size, 32),
        # 양방향 LSTM 학습 시키고 싶을 경우 Bidirectional 사용
        Bidirectional(LSTM(32, return_sequences=False)),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid")
    ])
    model.compile(loss = "binary_crossentropy", optimizer="adam", metrics = ["accuracy"])

    return model

model = create_model()
# model.summary()
"""
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding (Embedding)       (None, None, 32)          480000    
                                                                 
 bidirectional (Bidirectiona  (None, None, 32)         6272      
 l)                                                              
                                                                 
 dense (Dense)               (None, None, 32)          1056      
                                                                 
 dense_1 (Dense)             (None, None, 1)           33        
                                                                 
=================================================================
Total params: 487,361
Trainable params: 487,361
Non-trainable params: 0
_________________________________________________________________
"""

# 가장 좋은 loss의 가중치 저장
checkpoint_path = "best_performed_model.ckpt"
checkpoint = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                save_weights_only= True,
                                                save_best_only= True,
                                                monitor= "val_loss",
                                                verbose= 1)
# 학습 조기종료
early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience= 2)

# 학습
history = model.fit(train_padded,   # 훈련용 데이터
                    train_labels,
                    validation_data= (valid_padded, valid_labels),  # 학습 중 사용할 테스트용 데이터
                    callbacks=[early_stop, checkpoint], # 최적의 가중치 찾을 시 바로 종료
                    batch_size=64,  # 모델이 한번에 처리할 데이터 수
                    epochs=10,  # 반복 횟수
                    verbose=2)  # 학습시 console 에 요약 정도 0 : 출력 x, 1 : 진행 바, 2 : 결과 요약

# 새로운 리뷰 텍스트 감정 분석하기, 예측
new_reviews = ["영화 정말 재미있다", "정말 지루하다", "그냥 보통 이었어요", "생각보다 재미가 없다"]

new_sequences = tokenizer.texts_to_sequences(new_reviews)               # 문자를 숫자 벡터로 변환 함수
new_padded_sequences = pad_sequences(new_sequences, maxlen=max_length)  # 문자열 길이를 맞춰주는 함수

# 모델 이용한 감성분석 결과 예측
result = model.predict(new_padded_sequences)

# 예측 결과 출력
for i, review in enumerate(new_reviews):
    print(f"리뷰 : {review}, 확률 : {result[i]}")
"""
리뷰 : 영화 정말 재미있다, 확률 : [0.4516246]
리뷰 : 정말 지루하다, 확률 : [0.48909876]
리뷰 : 그냥 보통 이었어요, 확률 : [0.45626032]
리뷰 : 생각보다 재미가 없다, 확률 : [0.47670415]
"""

# 테스트 데이터 불러오기
test_file = tf.keras.utils.get_file("ratings_test.txt",
                                    origin="https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt",  # 파일 다운로드하는 url 주소
                                     extract=True)  # 만약 압축파일이면 자동으로 압축풀기 설정
test = pd.read_csv(test_file, sep="\t")
print(test.head())

# 데이터 전처리
def preprocessing(df):
    df["document"] = df["document"].str.replace("[^A-Za-z가-힣ㄱ-ㅎㅏ-ㅣ ]","", regex=True)
    df = df.dropna()
    test_label = np.asarray(df["label"])
    test_data = df["document"].apply((lambda x : word_tokenization(x)))
    test_data = tokenizer.texts_to_sequences(test_data)

    test_data = pad_sequences(test_data,
                              truncating= trunc_type,
                              padding= padding_type,
                              maxlen= max_length)
    return test_data, test_label

test_data, test_label = preprocessing(test)
print(model.evaluate(test_data, test_label))    # [0.2221933901309967, 0.9099703431129456]

# 기본 모델 load 후 평가
model2 = create_model()

print(model2.evaluate(test_data, test_label))   # [0.6931633353233337, 0.49798327684402466]

# 저장된 가중치 적용된 모델 load 후 평가
model2.load_weights(checkpoint_path)
model2.evaluate(test_data, test_label)  # [0.2763, 0.8843]

