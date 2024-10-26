# day37 > 2_챗봇.py

import pandas as pd
import numpy as np
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding , LSTM , Dense , Bidirectional


# RNN 기본 구조 : 1. 데이터 수집 2. 전처리 3. 토큰화 / 패딩 4. 모델 구축 5. 모델 학습 6. 모델 평가(튜닝)

# 현재 시간을 구하는 서비스 함수
def time_info(*kwargs):
    print("현재 시간 서비스 실행") # 현재 시간을 구하는 함수 호출
    result = "3시"

    return f"현재 시간은 {result}입니다."   # 챗봇이 응답하는 메시지 구성 반환

# 여러개의 매개변수를 받기, 가변 길이의 매개변수 : *매개변수명(튜플), **매개변수명(딕셔너리)
# JAVA에서는 dto를 주로 사용했기 때문에 자주 사용하지 않음
def stock_info(*kwargs):
    print("현재 재고 서비스 실행")

    result = 30
    if result == False:
        return "제품을 확인하기 위해서 제품 이름을 정확히 알려주세요."

    return f"{'콜라'}의 재고는 {result}개입니다."

# 예측한 확률의 질문과 함수를 매칭하는 딕셔너리 생성
response_functions = {
    2 : time_info,   # 지금 몇 시에요? 라는 예측 질문을 찾았을 때 함수 실행, "()" 제외
    5 : stock_info
}

# 1. 데이터 수집, ex_ CSV, DB, 함수(코드 / 메모리)
data = [
    {"user": "안녕하세요", "bot": "안녕하세요! 무엇을 도와드릴까요?"},
    {"user": "오늘 날씨 어때요?", "bot": "오늘은 맑고 화창한 날씨입니다."},
    {"user": "지금 몇 시에요?", "bot": "현재 시간을 알려드릴게요."},
    {"user": "좋은 책 추천해 주세요", "bot": "최근에 인기가 많은 책은 '파이썬 데이터 분석'입니다."},
    {"user": "고마워요", "bot": "천만에요! 더 필요한 것이 있으면 말씀해주세요."},
    {"user": "콜라의 재고를 알려주세요.", "bot": "제품의 재고를 알려드릴게요."}
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

    msg = outputs[max_index]

    # 만약 예측한 질문의 인덱스가 함수 매칭 딕셔너리 내에 존재하면
    if max_index in response_functions :
        msg += f"\n{response_functions[max_index](text)}" # 함수 호출 시에는 () 붙여야 함

    return msg

# 확인
print( response('안녕하세요') ) # 질문이 '안녕하세요' , 학습된 질문 목록중에 가장 높은 예측비율이 높은 질문의 응답을 출력한다.
# 서비스 제공한다. # 플라스크
while True :
    text = input( '사용자 : ' ) # 챗봇에게 전달할 내용 입력받기
    result = response( text ) # 입력받은 내용을 함수에 넣어 응답을 예측를 한다.
    print( f'챗봇 : { result }') # 예측한 응답 출력한다.