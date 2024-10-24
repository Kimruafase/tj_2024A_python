# day37 > 1_자연어_생성.py

import tensorflow as tf
import pandas as pd
import numpy as np
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout


# 1. 데이터 수집
    # utils.get_file()
    # 파일명, 다운로드 받을 링크, 압축 설정
file = tf.keras.utils.get_file("ratings_train.txt",
                               origin= "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt",
                               extract=True)

df = pd.read_csv(file, sep = "\t")
# print(df[1000:1007])
"""
           id                                       document  label
1000  9856453      정말 최고의 명작 성인이 되고 본 이집트의 왕자는 또 다른 감동 그자체네요      1
1001  6961803           이영화만 성공 했어도 스퀘어가 에닉스랑 합병 할일은 없었을텐데..      0
1002  8681713                                   울컥하는 사회현실 ㅠㅠ      1
1003  5348290                          기대를하나도안하면 할일없을때보기좋은영화      0
1004  9340549  소림사 관문 통과하기 진짜 어렵다는거 보여준 영화..극장에서 개봉하는거 반갑다..      1
1005  7357684                               시리즈안나오나 ㅠㅠㅠㅠㅠㅠㅠㅠ      1
1006  9303587               끝난다는 사실이 너무 슬퍼요. 가슴이 뻥 뚫려버린것같아..      1
"""
# 2. 데이터 전처리
okt = Okt() # 파이썬 객체 생성 : 변수명 = 클래스명()

def word_tokenization(text):
    # list = []
    # result = okt.morphs(text)
    # for word in result:
    #     list.append(word)
    # return list
    return [word for word in okt.morphs(text)]  # 리스트 컴프리헨션

def preprocessing(df):
    df = df.dropna()    # DataFrame의 결측값 제거 -> dropna()
    df = df[1000 : 2000]    # 샘플 데이터 1000개 사용
    # DataFrame["열 or 속성이름"]
    # "특정 문자열".replace() : 문자열을 치환하는 함수
    # df["document"].replace() : 특정 열 / 속성의 여러개 문자열 치환 함수
    # ** 서로 다른 객체들이 동일한 이름의 함수 / 기능을 제공하는 경우 -> 매개변수와 반환이 다를 수 있다.
    df["document"] = df["document"].str.replace("[^A-Za-z0-9가-힣ㄱ-ㅎㅏ-ㅣ ]", "", regex=True)
    # 람다식 활용
    data = df["document"].apply((lambda x : word_tokenization(x)))

    return data

review = preprocessing(df)
# print(len(review))  # 1000
# print(review[:10])
"""
1000    [정말, 최고, 의, 명작, 성인, 이, 되고, 본, 이집트, 의, 왕자, 는, 또...
1001    [이영화, 만, 성공, 했어도, 스퀘어, 가, 에, 닉스, 랑, 합병, 할, 일, ...
1002                                 [울컥, 하는, 사회, 현실, ㅠㅠ]
1003       [기대, 를, 하나, 도안, 하, 면, 할, 일, 없을, 때, 보기, 좋은, 영화]
1004    [소림사, 관문, 통과, 하기, 진짜, 어렵다는거, 보여준, 영화, 극장, 에서, ...
1005                              [시리즈, 안, 나오나, ㅠㅠㅠㅠㅠㅠㅠㅠ]
1006        [끝난다는, 사실, 이, 너무, 슬퍼요, 가슴, 이, 뻥, 뚫려, 버린것, 같아]
1007                                             [펑점, 조절]
1008                            [와이, 건, 진짜, 으리, 으리, 한, 데]
1009                                [손발, 이, 오, 그라드, 네, 요]
Name: document, dtype: object
"""

# 3. 토큰화 및 패딩
tokenizer = Tokenizer()

def get_tokens(review):
    # 토큰화 객체.fit_on_texts() : 각 단어의 인덱스에 해당하는 단어사전 생성
    tokenizer.fit_on_texts(review)
    total_words = len(tokenizer.word_index) + 1
    # 각 문장을 숫자(벡터)로 변환, .texts_to_sentences()
    # 위의 정의된 단어사전 기준으로 인덱스 변환
    tokenized_sentences = tokenizer.texts_to_sequences(review)

    input_sequences = []
    for token in tokenized_sentences:   # 문장(여러 벡트)을 하나씩 반복
        for t in range(1, len(token)):  #
            n_gram_sequences = token[:t+1]  # 토큰 리스트의 처음부터 t + 1번쨰 단어까지 슬라이싱
            input_sequences.append(n_gram_sequences) # 각 n_gram 형태의 sequences를 저장
    # 모든 연산 또는 함수는 항상 반환 값이 1개이다.
    return input_sequences, total_words # 튜플 1개로 반환

input_sequences, total_words = get_tokens(review)

# print(input_sequences[31 : 40])
"""
[[792, 25], 
[792, 25, 539], 
[792, 25, 539, 140], 
[792, 25, 539, 140, 109], 
[338, 9], 
[338, 9, 110], 
[338, 9, 110, 540], 
[338, 9, 110, 540, 90], 
[338, 9, 110, 540, 90, 148]]
"""

# 단어 사전
# print(f"감동 : {tokenizer.word_index['감동']}") # 감동 : 46
# print(f"영화 : {tokenizer.word_index['영화']}") # 영화 : 2
# print(f"코믹 : {tokenizer.word_index['코믹']}") # 코믹 : 415

# 문장의 길이 동일하게 맞추기
max_len = max([len(word) for word in input_sequences])
# print(f"max_len : {max_len}")   # max_len : 59

input_sequences = np.array(pad_sequences(input_sequences, maxlen= max_len, padding="pre"))

# x 는 독립변수 데이터로 각 sequence의 마지막 단어를 제외함 (마지막 단어는 예측으로 사용하기 위해)
# sequence는 처음부터 마지막 단어 직전까지 학습
x = input_sequences[:, :-1]   # 마지막 값 제외
# y 는 종속변수 데이터로 각 시퀀스의 마지막 단어를 원 핫 인코딩으로 변환한다 (위치를 찾기 위해)
# to_categorical() : 레이블 값을 원 핫 인코딩을 통해 반환하는 함수
y = to_categorical(input_sequences[:, -1], num_classes=total_words) # 마지막 값만 이진 클래스의 벡터로 변환

# y 를 설명하기 위한 예시
a = to_categorical([0, 1, 2, 3], num_classes=4)
# print(a)
"""
[[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]
"""

# 모델 생성 및 훈련
embedding_dim = 256

model = Sequential( # 딥러닝 모델
    # 1. 임베딩 layer(원 핫 인코딩(벡터) vs 밀집 인코딩(벡터)) : 밀집 벡터로 변환하는 역할
    # input_dim : 입력받을 단어의 총 개수, output_dim : 밀집 벡터로 변환된 벡터의 차원
    # input_length : 입력 데이터의 최대 길이 (마지막 단어 제외한) 지정
    [Embedding(input_dim=total_words,
               output_dim=embedding_dim,
               input_length=max_len - 1),

     # 2. 양방향(Bidirectional), RNN 알고리즘(LSTM) -> Bidirectional(LSTM()) : 양방향 RNN 알고리즘
     # unit(유닛 / 노드 / 뉴런) : 학습하면서 특징 / 파라미터 / 값을 지정하는 개수 -> 양방향일 경우 * 2
     Bidirectional(LSTM(units=256)),
     # 3. 출력 layer : 출력 개수는 이진분류가 아닌 다중분류이므로 활성화함수는 "softmax"이다.
     # units = 마지막 출력 layer의 유닛 / 노드 / 뉴런의 종속 변수 개수
     Dense(units=total_words, activation="softmax")])

# 컴파일(머신러닝과 다르게 딥러닝은 학습도중에 손실함수(loss)와 평가지표(accuracy, 정확도) 확인 / 모니터링할 수 있는 함수 / 기능
model.compile(loss = "categorical_crossentropy", optimizer="adam", metrics = ["accuracy"])
# x : 독립변수, y : 종속변수, epochs : 학습 횟수
# 딥러닝 : 머신러닝보다 조금 더 복잡(다차원)하고 복잡한 학습을 함으로 패턴 찾기
history = model.fit(x, y, epochs = 20, verbose = 1)

# 문장 생성 함수(시작 텍스트, 생성 단어 개수)
def text_generation(sos, count):
    # count : 생성할 단어의 개수
    for _ in range(1, count):   # 단어 사전은 인덱스 1부터 시작하기 때문에 1부터 시작
        # sos(새로운 문장)를 벡터로 변환
        token_list = tokenizer.texts_to_sequences([sos])[0]
        # 새로운 문장을 패딩화해서 학습된 문장들과 동일하게 일치
        token_list = pad_sequences([token_list],
                                   maxlen= max_len - 1,
                                   padding="pre")
        # 예측하기, 모델 객체명.predict(예측할 데이터)
        # 예측한 데이터 중 가장 확률이 높은 단어 확인
        predicted = np.argmax(model.predict(token_list), axis = 1)

        # 반복문을 이용한 단어 사전에서 비율이 높은 예측 단어 찾기
        # Tokenizer 객체.word_index.items() : 단어 사전들의 단어
        for word, idx in tokenizer.word_index.items():
            # 만약 단어 사전 내 인덱스가 예측 인덱스와 같으면
            if idx == predicted:
                # 찾은 인덱스의 단어를 output 변수에 저장
                output = word
                break
        # 새로운 문장 뒤에 예측한 단어 연결
        sos += " " + output

    return sos

# argmax 설명 : 최대값의 인덱스 반환
data = [[0.1, 0.2, 0.7], [0.3, 0.5, 0.2], [0.4, 0.3, 0.3]]
print(np.argmax([data], axis= -1))    # [[2 1 0]]

print(text_generation("연애 하면서", 12))    # 연애 하면서 없는데 뭘 10 자 이상 쓰라는 거 야 추천 갈수록 사람
print(text_generation("꿀잼", 12))    # 꿀잼 영화 추억 이다 ㅜㅜ 봤는데 안나 띠띠디띠 재밌다 제 거 은
print(text_generation("최고의 영화", 12))    # 최고의 영화 춘향전 을 고발 한다 연예가중계 에서 정 사신 을 강요 하며
print(text_generation("손발 이", 12))  # 손발 이 오 그라드 네 요 요 1 부터 평점 을 위해 보고
