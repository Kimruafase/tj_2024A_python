# day37 > 2_챗봇.py

import pandas as pd
import numpy as np
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding , LSTM , Dense , Bidirectional

# 1. 데이터 수집
data = [
    {"user": "안녕하세요", "bot": "안녕하세요! 무엇을 도와드릴까요?"},
    {"user": "오늘 날씨 어때요?", "bot": "오늘은 맑고 화창한 날씨입니다."},
    {"user": "지금 몇 시에요?", "bot": "현재 시간은 오후 3시입니다."},
    {"user": "좋은 책 추천해 주세요", "bot": "최근에 인기가 많은 책은 '파이썬 데이터 분석'입니다."},
    {"user": "고마워요", "bot": "천만에요! 더 필요한 것이 있으면 말씀해주세요."}
]

# DataFrame 으로 변환
data = pd.DataFrame(data)

# 2. 데이터 전처리
inputs = list(data["user"])
outputs = list(data["bot"])

okt = Okt()

def preprocess(text):
    # 1) 한글과 띄어쓰기를 제외한 문자 제거
    # 정규표현식, 일반적인 문자열 정규표현식
    result = re.sub(r"[^가-힣\s]", "", text)

    # 2) 형태소 분석
    result = okt.pos(result)

    # 3) 명사(Noun)와 동사와 형용사 외 제거
    # 형태소 분석기가 각 형태소들을 명칭하는 단어들의 (pos) 변수가 존재한다.
    result = [word for word, pos in result if pos in ["Noun", "Verb", "Adjective"]]

    # 4) 불용어 생략

    # 5) 반환
    return " ".join(result).strip() # .strip() 앞뒤 공백 제거 함수

processed_inputs = [preprocess(word) for word in inputs]
# print(processed_inputs) # ['안녕하세요', '오늘 날씨 어때요', '지금 몇 시', '좋은 책 추천 해 주세요', '고마워요']

# 3. Tokenizer
tokenizer = Tokenizer()
# 전처리된 단어 목록들로 단어사전 생성
tokenizer.fit_on_texts(processed_inputs)
# print(tokenizer.word_index)
"""
{'안녕하세요': 1, '오늘': 2, '날씨': 3, '어때요': 4, '지금': 5, '몇': 6, '시': 7, '좋은': 8, '책': 9, '추천': 10, '해': 11, '주세요': 12, '고마워요': 13}
"""

# 벡터화
input_sequences = tokenizer.texts_to_sequences(processed_inputs)
# print(input_sequences)  # [[1], [2, 3, 4], [5, 6, 7], [8, 9, 10, 11, 12], [13]]

# 여러 문장중에 가장 긴 단어의 개수 찾기
max_len = max([len(word) for word in input_sequences])
# print(max_len)  # 5

# 패딩화, 가장 길이가 긴 문장 기준으로 0 채우기
input_sequences = pad_sequences(input_sequences, maxlen = max_len)
# print(input_sequences)
"""
[[ 0  0  0  0  1]
 [ 0  0  2  3  4]
 [ 0  0  5  6  7]
 [ 8  9 10 11 12]
 [ 0  0  0  0 13]]
"""

# 종속변수, DataFrame -> 일반 배열로 변경
output_sequences = np.array(range(len(outputs)))
# print(output_sequences)
"""
['안녕하세요! 무엇을 도와드릴까요?' '오늘은 맑고 화창한 날씨입니다.' '현재 시간은 오후 3시입니다.'
 "최근에 인기가 많은 책은 '파이썬 데이터 분석'입니다." '천만에요! 더 필요한 것이 있으면 말씀해주세요.']
"""

# 1. 모델
model = Sequential( )
model.add( Embedding( input_dim= len(tokenizer.word_index ) , output_dim = 50 , input_length=max_len))
model.add( Bidirectional( LSTM( 256 ) ) ) ,  #  256 , 128 , 64 , 32
model.add( Dense( len(outputs)  , activation='softmax') ) # 종속변수의 값 개수는 응답 개수
# 2. 컴파일
model.compile( loss='sparse_categorical_crossentropy' , optimizer='adam' , metrics=['accuracy'] )

# 3. 학습
model.fit( input_sequences , output_sequences , epochs= 10  )

# 4. 예측하기
def response( text ) :
    text = preprocess( text )# 1. 예측할 값도 전처리 한다.
    text = tokenizer.texts_to_sequences( [ text ] )  # 2. 예측할 값도 토큰 과 패딩  # 학습된 모델과 데이터 동일
    text = pad_sequences( text , maxlen= max_len)
    result = model.predict( text ) # 3. 예측
    max_index = np.argmax( result )  # 4. 결과 # 가장 높은 확률의 인덱스 찾기
    return outputs[max_index]  # 5.
# 확인
print( response('안녕하세요') ) # 질문이 '안녕하세요' , 학습된 질문 목록중에 가장 높은 예측비율이 높은 질문의 응답을 출력한다.
# 서비스 제공한다. # 플라스크
while True :
    text = input( '사용자 : ' ) # 챗봇에게 전달할 내용 입력받기
    result = response( text ) # 입력받은 내용을 함수에 넣어 응답을 예측를 한다.
    print( f'챗봇 : { result }') # 예측한 응답 출력한다.