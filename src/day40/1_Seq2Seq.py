# day39 > 1_Seq2Seq.py

import numpy as np
import warnings
import tensorflow as tf
import pandas as pd
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Attention, Input
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from tensorflow.python.keras.utils.version_utils import training
from tensorflow.keras.utils import plot_model

# 1. 데이터 수집
# > 질문과 답변이 있는 말뭉치(대화내용)를 가져오기
    # Q : 질문, A : 답변, label : (0 -> 일상다반사, 1 -> 부정, 2 -> 긍정
corpus = pd.read_csv("https://raw.githubusercontent.com/songys/Chatbot_data/master/ChatbotData.csv")
# print(corpus["Q"].head()) # "질문" 열의 상단 5개 데이터 확인
"""
0     하루가 또 가네요.
1      위로해 드립니다.
2    여행은 언제나 좋죠.
3    여행은 언제나 좋죠.
4     눈살이 찌푸려지죠.
Name: A, dtype: object

"""
# print(corpus["A"].head()) # "답변" 열의 상단 5개 데이터 확인
"""
0     하루가 또 가네요.
1      위로해 드립니다.
2    여행은 언제나 좋죠.
3    여행은 언제나 좋죠.
4     눈살이 찌푸려지죠.
Name: A, dtype: object
"""
# 확인 -> 같은 인덱스로 질문과 답변이 구성됨
# print(f"Q : {corpus['Q'][0]}")
# print(f"A : {corpus['A'][0]}")
"""
Q : 12시 땡!
A : 하루가 또 가네요.
"""

# 확인
# print(corpus.shape) # (11823, 3)

# 샘플링 (1000개 사용)
texts = []   # 질문 리스트
pairs = []  # 답변 리스트

# print(zip(corpus["Q"], corpus["A"]))    # <zip object at 0x0000015041EB4240>
for i, (text, pair) in enumerate(zip(corpus["Q"], corpus["A"])):
    texts.append(text)
    pairs.append(pair)
    if i >= 1000 :   # 1000개의 인덱스만 사용
        break

# 2. 데이터 전처리
def clean_sentence(sentence):
    # 한글 숫자 제외한 모든 문자 제거
    sentence = re.sub(r"[^0-9ㄱ-ㅎㅏ-ㅣ가-힣 ]", r'', sentence)

    return sentence

# print(clean_sentence("안녕하세요~:)"))   # 안녕하세요
# print(clean_sentence("텐서플로^@^%#@!"))    # 텐서플로

okt = Okt()

# Okt 형태소 변환
def process_morph(sentence):

    return " ".join(okt.morphs(sentence))   # 형태소 분석 결과를 하나의 문자열로 합치기

def clean_and_morph(sentence, is_question = True):  # 매개변수명 = 초기값, 매개변수명에 초기값 넣기
    # 한글 문장 전처리
    sentence = clean_sentence(sentence)

    # 형태소 변환
    sentence = process_morph(sentence)

    # Question 인 경우, Answer 인 경우를 분기하여 처리
    if is_question:

        return sentence

    else :

        # Start 토큰은 decoder input 에, End 토큰은 decoder output 에 추가
        return (f"<START> {sentence}", f"{sentence} <END>")

def preprocess(texts, pairs):
    # 인코더에 입력할 질문 전체 리스트
    questions = []
    # 디코더에 입력할 데이터셋(답변의 시작), <START> 토큰을 문장 처음에 추가
    answer_in = []
    # 디코더에 입력할 데이터셋(답변의 끝), <END> 토큰을 문장 마지막에 추가
    answer_out = []

    # 질의에 대한 전처리
    for text in texts:
        # 전처리와 morphs 진행
        question = clean_and_morph(text, is_question=True)
        questions.append(question)

    # 답변에 대한 전처리
    for pair in pairs:
        in_, out_ = clean_and_morph(pair, is_question=False)
        answer_in.append(in_)
        answer_out.append(out_)

    return questions, answer_in, answer_out

questions, answer_in, answer_out = preprocess(texts, pairs)

# print(questions[:2])    # ['12시 땡', '1 지망 학교 떨어졌어']
# print(answer_in[:2])    # ['<START>하루 가 또 가네요', '<START>위로 해 드립니다']
# print(answer_out[:2])   # ['하루 가 또 가네요<END>', '위로 해 드립니다<END>']

all_sentences = questions + answer_in + answer_out

warnings.filterwarnings("ignore")
# 단어 사전 만들기
    # filters='' : 토큰화 할때 특정 기호를 제거(필터) # 필터링 하지 안겠다는 뜻
    # lower = False : 토큰화 할때 소문자로 변환하지 여부 # 기본값 true 이므로 모든 영문을 소문자로 변환
        # false 이므로 변환하지 않는다.
    # oov_token : 단어 사전에 없는 단어를 매칭할 때 그 단어를 대체할 문자<OOV> 표현
tokenizer = Tokenizer(filters="", lower=False, oov_token="<OOV>")
tokenizer.fit_on_texts(all_sentences)

for word, idx in tokenizer.word_index.items():
    # print(f"{word}\t -> \t{idx}")
    if idx > 10 :
        break

"""
<OOV>	 -> 	1
<START>	 -> 	2
<END>	 -> 	3
이	 -> 	4
거	 -> 	5
을	 -> 	6
가	 -> 	7
나	 -> 	8
예요	 -> 	9
사람	 -> 	10
요	 -> 	11
"""


# print(len(tokenizer.word_index))    # 2898

# .texts_to_sequence() : 등록된 단어사전에 따라 문장의 단어들을 벡터(숫자)로 매칭하여 변환
question_sequence = tokenizer.texts_to_sequences(questions)
answer_in_sequence = tokenizer.texts_to_sequences(answer_in)
answer_out_sequence = tokenizer.texts_to_sequences(answer_out)

# 패딩 (문장 길이 맞춰서 학습 데이터들의 차원을 일치화함으로써 모델 성능 향상)
MAX_LENGTH = 30 # 문장 내 최대 길이를 임의로 30, "post" -> 빈 칸을 뒤에 0으로 채우기
question_padded = pad_sequences(question_sequence, maxlen=MAX_LENGTH, truncating= "post", padding="post")
answer_in_padded = pad_sequences(answer_in_sequence, maxlen=MAX_LENGTH, truncating= "post", padding="post")
answer_out_padded = pad_sequences(answer_out_sequence, maxlen=MAX_LENGTH, truncating= "post", padding="post")

# print(question_padded.shape) # (1001, 30)
# print(answer_in_padded.shape)   # (1001, 30)
# print(answer_out_padded.shape)  # (1001, 30)

# 인코더, 텐서플로의 Model 클래스로부터 상속받아서 인코더 클래스 정의
class Encoder(tf.keras.Model):

        # units : LSTM 에서 사용할 유닛 / 노드 / 뉴런 수
            # "안녕하세요, 오늘 날씨 어때요?" 라는 문장이라고 가정
        # vocab_size : 임베딩 레이어의 입력으로 들어가는 크기
            # "안녕하세요", "오늘", "날씨", "어때요" -> 4
        # embedding_dim : 임베딩 레이어의 각 단어 크기를 나타내는 벡터 차원
            # 밀집 행렬을 처리할 때 한 단어를 표현할 차원의 수, "안녕하세요"를 몇 차원으로 구성할 지 결정
        # timp_steps : 임베딩 레이어의 입력으로 sequence 의 길이
            # 한번에 몇 개의 단어를 모델이 학습하고 기억할 지 단위를 정함 -> 단위 2라면 "안녕하세요", "오늘"
    def __init__(self, units, vocab_size, embedding_dim, time_steps):

        # 상속받은 super 클래스의 생성자를 호출
        super(Encoder, self).__init__()

        # 임베딩 레이어
        self.embedding = Embedding(vocab_size, embedding_dim, input_length=time_steps, name = "Embedding")

        # 드롭아웃 레이어
        self.dropout = Dropout(0.2, name = "Dropout")

        # LSTM 레이어
            # return_state = True : 은닉 상태와 셀 상태 반환 설정
            # (Attention) 어텐션 추가 -> return_sequences = True 추가
        self.lstm = LSTM(units, return_state=True, return_sequences=True, name = "LSTM")

    # 실행 함수, call
    def call(self, inputs):
        x = self.embedding(inputs)  # 임베딩 레이어에 따른 밀집행렬 생성
        x = self.dropout(x)         # 드롭 아웃 레이어에 따른 무작위 노드 제외
            # x : LSTM 레이어에서 특정 단어들을 통해 도출해낸 특징(정보 / 패턴)
                # 문장 : "오늘 무엇을 먹을까?" -> 현재 문장의 분석 결과를 알려주는 출력값
            # hidden_state : LSTM 레이어가 현재 시점에서 기록한 특징(정보 / 패턴) -> 최종 은닉 상태
                # L(Long) S(Short) T(Term) M(Memory) : 앞 전 문장을 잊지 않고 지속하는 문장을 기록하는 메모리
            # cell_state : LSTM 레이어가 전체 단어들에서 기록한 중요한 특징(정보 / 패턴) -> 셀 상태
                # 앞 전 전체 분석된 문장들 중에서 중요한 단어들을 기억하는 메모리
            # 특징 / 패턴 분석
                # CNN : 이미지 분석, 곡선, 색감, 사이즈, 비율, 질감(텍스쳐) 등등, 컴퓨터는 0 ~ 255 사이의 숫자들로 RGB를 판단
                # RNN : 텍스트 분석, 빈도, 삼정, 형태소(동사, 형용사 등등), 단어의 의미, 컴퓨터는 텍스트 대신 벡터로 판단
        x, hidden_state, cell_state = self.lstm(x)  # LSTM 레이어에 따른 학습 실행

        # Dense 레이어가 없는 이유는 현재 클래스(인코더)의 목적이 입력 과정을 하기 위해서 -> 디코더에 전달
            # (Attention) x 값 리턴 추가
        return x, [hidden_state, cell_state]   #

# 디코더, 텐서플로의 Model 클래스로부터 상속받아서 디코더 클래스 정의
class Decoder(tf.keras.Model):
    def __init__(self, units, vocab_size, embedding_dim, time_steps):
        super(Decoder, self).__init__()
        self.embedding = Embedding(vocab_size, embedding_dim, input_length=time_steps, name = 'Embedding')

        self.dropout = Dropout(0.2, name = "Dropdout")

        # return_state=True : 생략가능(기본값) , 은닉 상태와 셀 상태 반환 설정
        # return_sequences=True : 모든 시점의 출력을 반환한다.
        self.lstm = LSTM(units, return_state= True, return_sequences=True, name = "LSTM")

        self.attention = Attention(name = "Attention")
        self.dense = Dense(vocab_size, activation = "softmax", name = "Dense")

    def call(self, inputs, initial_state):
        # encoder_inputs, decoder_inputs 추가
        encoder_inputs, decoder_inputs = inputs
        x = self.embedding(decoder_inputs)
        x = self.dropout(x)
        # initial_state : 초기화상태 속성, 인코더와 결합 이후에 인코더에 생성한 은닉 상태와 셀 상태를 대입한다.
        # LSTM 레이어 에 따른 학습
        x, hidden_state, cell_state = self.lstm(x, initial_state = initial_state)

            # (Attention) key_value, attention_matrix 추가
            # (Attention) 이전 hidden_state의 값을 concat 으로 만들어 vector 를 생성
        key_value = tf.concat([initial_state[0][:, tf.newaxis, :], x[:, :-1, :]], axis = 1)

            # (Attention) 이전 hidden_state 의 값을 concat 으로 만든 vector 와 encoder에서 나온 출력값들로 attention 을 구함
        attention_matrix = self.attention([key_value, encoder_inputs])

            # (Attention) 위에서 구한 attention_matrix 와 decoder 의 출력값을 합침(concat)
        x = tf.concat([x, attention_matrix], axis = -1)

        # 출력 레이어, 출력 : 학습된 모델에서의 최종 출력된 값 = x
        x = self.dense(x)

        # ( 최종 확률값 , 은닉 상태 , 셀 상태 )
        return x, hidden_state, cell_state

# 모델 결합
class Seq2Seq(tf.keras.Model):
    def __init__(self, units, vocab_size, embedding_dim, time_steps, start_token, end_token):
        super(Seq2Seq, self).__init__()

        # 객체의 속성를 정의후 매개변수 대입, 시작 토큰, 모델이 문장을 생성할때 시작을 식별하기 위해 사용
        self.start_token = start_token

        # 끝나는 토큰, 모델이 문장을 생성할때 끝마침을 식별하기 위해 사용
        self.end_token = end_token
        self.time_steps = time_steps

        # 인코더 객체 생성 -> 각 매개변수 대입
        self.encoder = Encoder(units, vocab_size, embedding_dim, time_steps)

        # 디코더 객체 생성 -> 각 매개변수 대입
        self.decoder = Decoder(units, vocab_size, embedding_dim, time_steps)

    def call(self, inputs, training = True):
        # inputs : 모델객체 안으로 들어오는 입력 데이터
        # training = True : true 훈련중 일때 , false 훈련중이 아닐때, 매개변수 = 초기값, 훈련 중을 기본값으로 사용한다.

        # 훈련중이면, fit()
        if training :

            # 현재 모델이 주어진 인코더와 디코더의 입력, fit() 메소드 호출시 들어오는 데이터
            encoder_inputs, decoder_inputs = inputs

            # encoder 객체의 call 함수 호출 하고 결과 받기
                # (Attention) encoder 출력 값 수정
            encoder_outputs, context_vector = self.encoder(encoder_inputs)

            # decoder 객체의 call 함수 호출 하고 결과 받기, initial_state : 인코더 결과 값
                # _(언더바) : 변수 생략, for _ in 리스트, ( 값 , _ , _ ) = 함수( )
                # (Attention) decoder 입력 값 수정
            decoder_outputs, _, _ = self.decoder((encoder_outputs, decoder_inputs), initial_state = context_vector)

            # 디코더의 출력을 반환, 최종 예측한 확률값
            return decoder_outputs

        # 훈련이 아닐떄, 예측모드, 추론모드, 문장을 생성 하기 위한 생성할 문장을 예측 하는 코드
        else :
            x = inputs

                # (Attention) encoder 출력 값 수정
            encoder_outputs, context_vector = self.encoder(x)

            # 시작 토큰을 이용한 2차원 텐서를 생성한다. tf.constant() : 차원 만들기 함수
            target_seq = tf.constant([[self.start_token]], dtype = tf.float32)

            # 디코더의 출력 결과를 저장하기 위한 배열 생성한다. tf.TensorArray() 텐서 배열 만들기 함수
            results = tf.TensorArray(tf.int32, self.time_steps)

            # 디코더가 다음 단어(문장 만들기)를 예측하는 과정 반복
            for i in tf.range(self.time_steps):

                # ( 최종확률값 , 은닉상태 , 셀상태 ) = 디코더객체
                decoder_output, decoder_hidden, decoder_cell = self.decoder((encoder_outputs, target_seq), initial_state = context_vector)

                # 예측결과에서 가장 확률이 높은 인덱스 찾기 : tf.argmax( decoder_output , axis=1 ), tf.argmax() 가장 높은 값의 인덱스 반환함수
                decoder_output = tf.cast(tf.argmax(decoder_output, axis= -1), dtype = tf.int32)

                # tf.reshape() 차원을 변경 함수
                decoder_output = tf.reshape(decoder_output, shape = (1, 1))

                # (TensorArray).write() : i번째 인덱스의 예측한 단어를 텐서배열에 저장
                results = results.write(i, decoder_output)

                # 예측한 단어가 종료 토큰( <END> 포함 )과 일치하면 반복문 종료
                if decoder_output == self.end_token:
                    break

                # 종료 토큰이 아니면
                # 현재 예측된 단어를 다음 반복에 입력으로 사용한다.
                target_seq = decoder_output

                # 디코더의 상태를 업데이터 하여 다음 반복에 사용한다.
                context_vector = [decoder_hidden, decoder_cell]

            # 반복문이 종료되면 모든 예측 결과를 스택으로 반환한다. 이 결과에 모든 시퀀스를 예측한 결과를 포함
            return tf.reshape(results.stack(), shape = (1, self.time_steps))

# 시퀀스란 : 문장을 정해진 순서대로 나열된 단어를 의미, 알고리즘,자료구조,딥러닝 등등 에서 사용되는 용어
# 예] 반가워 사랑해 좋아 => ["반가워" , "사랑해" , "좋아" ]

# 디코더의 결과를 원핫 인코딩 벡터로 변환
VOCAB_SIZE = len(tokenizer.word_index) + 1  # tokenizer.word_index 단어사전 # 단어사전의 단어 개수 + 1 <OOV>를 추가했으므로

# 디코더의 결과를 원 핫 인코딩 벡터로 변환
    # 컴퓨터가 이해하는 언어인 벡터로 변경하는 방법
    # 임베딩(밀집행렬) : 주로 챗봇의 질문에서 사용된다.(학습 데이터) -> 임베딩은 단어간의 유사성 파악에 유리
    # 원핫 인코딩 : 주로 챗봇의 답변에서 사용된다. (결과 데이터) -> 유사성 파악이 아닌 단순 분류에서 유리

def convert_to_one_hot(padded):
    # 1. 응답 개수만큼의 차원수를 0으로 채우기
    # 원 핫 인코딩 초기화
        # (데이터1, 데이터2, 데이터3) : 3차원 배열을 초기화
        # len(answer_out_padded) : 총 응답의 개수, (1001, 30)
        # MAX_LENGTH : 문장 내 최대 길이
        # VOCAB_SIZE : 단어 사전의 단어 수
        # (응답 단어의 총 개수, 최대 길이, 단어 사전의 단어 수)

    # np.zeros(차원수) : 지정한 차원 수만큼 0으로 채운다.
        # ex_1 np.zeros(5) : [0 0 0 0 0]
        # ex_2 np.zeros(3, 4) : [[0 0 0 0], [0 0 0 0], [0 0 0 0]]
        # ex_3 np.zeros(2, 3, 4) : [[[0 0 0 0], [0 0 0 0], [0 0 0 0]], [[0 0 0 0], [0 0 0 0], [0 0 0 0]]]
    one_hot_vector = np.zeros((len(answer_out_padded), MAX_LENGTH, VOCAB_SIZE))

    # 2. 단어 사전이 존재하는 경우에는 해당 인덱스를 1로 변경
    # 디코더 목표를 원 핫 인코딩으로 변환
    # 학습 시 입력은 인덱스 이지만 출력은 원 핫 인코딩 형식임
        # 2-1. 행, i는 현재 시퀀스의 인덱스, sequence : 현재 시퀀스의 단어
    for i, sequence in enumerate(answer_out_padded):
        # 2-2. 열, j는 현재 단어의 인덱스
        # 2-3. 높이, index
        for j, index in enumerate(sequence):
            one_hot_vector[i, j, index] = 1 # 지정한 인덱스를 1로 변경하여 원 핫 인코딩 완성

    return one_hot_vector

answer_in_one_hot = convert_to_one_hot(answer_in_padded)
answer_out_one_hot = convert_to_one_hot(answer_out_padded)
# print(answer_in_one_hot[0].shape)   # (30, 2303)
# print(answer_out_one_hot[0].shape)  # (30, 2303)

# 모델이 예측한 단어 목록(indexs : 예측한 단어의 인덱스)을 이용한 새로운 문장 만들기 함수
def convert_index_to_text(indexs, end_token):

    sentence = "" # 생성된 문장을 저장할 변수를 선언, 처음에는 빈 문자열

    # 모든 문장에 대해서 반복
        # indexs 배열의 각 인덱스를 반복, 해당 배열에는 예측된 단어가 위치한 배열
    for index in indexs:

        # 만약에 현재 인덱스가 end_token(마지막 문장)이면 문장 생성을 종료
        if index == end_token:

            # 끝 단어이므로 예측 준비
            break

        # 사전에 존재하는 단어의 경우 단어 추가
            # 예측한 인덱스가 0보다 크고 (tokenizer) 단어 사전 내 지정한 인덱스의 단어가 None 이 아니라면
        if index > 0 and tokenizer.index_word[index] is not None :
            # 찾았으면 찾은 단어를 생성한 문장 변수에 '+=' 을 통해 누적으로 더한다.
            sentence += tokenizer.index_word[index]

            # 단어 사전에 없는 인덱스라면 빈 문자열 추가
        else:
            # 사전에 없는 인덱스면 빈 문자열 추가
            sentence += ""

        # 빈 칸 추가
            # 다음 반복으로(다음 단어 생성) 이동하기 전에 띄어쓰기 추가
        sentence += " "

    # 전체 반복문이 종료하면 생성된 문장 변수 반환
    return sentence

# 훈련 시 필요한 파라미터 값 정의
    # buffer : 모델이 훈련 중에 저장할 (무작위) 샘플의 최대 개수
    # buffer 가 클수록 다양하게 잘 섞여서 학습의 성능을 향상시킬 수 있지만 메모리 소모가 크다. 조절이 필요하다.
BUFFER_SIZE = 1000

    # batch : 모델이 훈련 중에 훈련 1번에 있어서 사용되는 샘플의 개수
    # batch 가 클수록 안정적이지만 메모리 소모가 크다. 8, 16, 32, 64 단위로 주로 사용된다. 조절이 필요하다.
BATCH_SIZE = 16

    # embedding 차원 : 단어를 벡터로 인코딩하는 과정에 있어서 한 단어가 사용할 차원 수
    # 벡터로 표현할 차원 수가 크면 표현 성능이 좋아지지만 메모리 소모와 계산 비용이 증가한다.
    # 단어들 간의 의미 관계를 파악할 수 있다.
EMBEDDING_DIM = 100

    # 문장 내 단어의 최대 개수를 MAX_LENGTH 로 설정 -> 30
TIME_STEPS = MAX_LENGTH

    # 문장의 시작을 알리는 토큰(단어)의 인덱스
        # 단어 생성(예측) 시 시작 위치를 알림
START_TOKEN = tokenizer.word_index["<START>"]

    # 문장의 끝을 알리는 토큰(단어)의 인덱스
        # 단어 생성(예측) 시 해당 토큰을 만나면 문장 생성 종료
END_TOKEN = tokenizer.word_index["<END>"]

    # 유닛 수 : RNN(유닛), CNN(노드) -> 뉴런의 개수
    # 각 모델이 학습하는 layer에 사용될 뉴런의 개수
    # 많은 유닛 수를 사용하면 더 복잡한 학습이 가능하지만, 과대적합에 빠질 수 있다.
    # 주로 32, 64, 128 지정
UNITS = 128

    # tokenizer 단어 사전 내 단어 수, + 1을 하는 이유는 <OOV>가 추가되었기 때문
VOCAB_SIZE = len(tokenizer.word_index) + 1

    # 질문의 총 개수
DATA_LENGTH = len(questions)

    # 샘플 개수
SAMPLE_SIZE = 3

    # 반복 횟수
NUM_EPOCHS = 20

# 모델 저장할 수 있도록 체크포인트 생성
    # .ckpt -> .weight.h5 변경
checkpoint_path = "model/seq2seq-chatbot-checkpoint.weight.h5"

    # filepath : 모델 가중치를 지정할 파일 경로 지정
    # save_weight_only : True 면 모델의 구조 저장 X, 가중치만 저장, False 는 구조 저장 O
    # save_best_only : 훈련 중 모니터 값이 개선될 때만 가중치를 저장, 성능이 향상될 때 체크 포인트를 업데이트
    # monitor : 어떤 값을 모니터링할지 지정함, loss -> 손실함수
    # verboss : 과정 로그 수준을 출력할지 말지 지정, 생략 가능
checkpoint = ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, save_best_only= True, monitor="loss", verbose=1)

# seq2seq 모델 객체 생성
seq2seq = Seq2Seq(UNITS, VOCAB_SIZE, EMBEDDING_DIM, TIME_STEPS, START_TOKEN, END_TOKEN)

# 모델 컴파일
seq2seq.compile(optimizer="adam", loss = "categorical_crossentropy", metrics=["acc"])

# 모델 학습 후 예측한 단어 출력
    # model : 모델, question_inputs : 예측할 새로운 질문
def make_prediction(model, question_inputs):

    # 모델에 새로운 질문과 training = False 값을 주어 예측할 단어라는 것을 알림
        # Seq2Seq 클래스 내 call 함수 내 else 부분의 코드들이 실행
    results = model(inputs = question_inputs, training = False)

    # 변환된 인덱스를 문장으로 변환
        # 예측 결과를 np(넘파이) 배열로 변환하고 차원을 1차원 (-1)로 변경한다.
        # 나중에 문장 조회시 평탄화(1차원 배열)하고 convert_index_to_text() 에게 전달한다.
    results = np.asarray(results).reshape(-1)

    return results

# 훈련 과정
    # 총 NUM_EPOCHS 회 반복
for epoch in range(NUM_EPOCHS):
    print(f"processing epoch: {epoch * 10 + 1}...")

    # fit() 모델 훈련 함수
        # 1. [question_padded, answer_in_padded] : 입력 데이터
        # 2. answer_out_one_hot : 결과 데이터
        # 3. callbacks : 훈련 중 지정할 체크포인트, 가중치만 저장
    seq2seq.fit([question_padded, answer_in_padded], answer_out_one_hot, epochs = 10, batch_size = BATCH_SIZE, callbacks = [checkpoint])

    # 랜덤한 샘플 번호 추출, 훈련 후 사용할 샘플 수 만큼 난수의 질문을 이용하여 성능 예측하기
        # 전체 질문에서 3개의 질문을 난수로 추출
        # np.random.randint(전체 개수, size = 추출할 난수의 개수) : 0부터 전채 개수까지 추출할 난수의 개수만큼 정수 배열로 반환함
    samples = np.random.randint(DATA_LENGTH, size = SAMPLE_SIZE)

    # 예측 성능 테스트
        # 임의의 3개에 질문이 있는 리스트
    for idx in samples:
        # question_padded[idx] : 선정된 질문의 인코딩(패딩)된 단어 가져오기
        question_inputs = question_padded[idx]

        # 문장 예측
            # np.expand_dims(배열, 0) : 새로운 차원 추가, 0 -> 첫번째 자리에 차원 추가
            # (1, 패딩화 된 단어 값) : 2차원으로 배열 만든다. -> 모델의 예측 매개변수가 2차원이라서(입력차원, 응답차원)
        results = make_prediction(seq2seq, np.expand_dims(question_inputs, 0))

        # 변환된 인덱스를 문장으로 변환
        results = convert_index_to_text(results, END_TOKEN)

        # 확인
        print(f"Q : {questions[idx]}")
        print(f"A : {results}\n")
        print()



# 자연어(질문 입력)에 대한 전처리 함수
def make_question(sentence):
    # 형태소 분석 함수 실행
    sentence = clean_and_morph(sentence)

    # 벡터화
    question_sequence = tokenizer.texts_to_sequences([sentence])

    # 패딩
    question_padded = pad_sequences(question_sequence, maxlen = MAX_LENGTH, truncating="post", padding = "post")

    return question_padded

# 챗봇
def run_chatbot(question):

    # make_question() 함수를 호출하여 질문을 전처리한다.
    question_inputs = make_question(question)

    # make_prediction() 함수에 학습된 모델과 전처리된 질문을 대입하여 응답을 예측한다.
    results = make_prediction(seq2seq, question_inputs)

    # convert_index_to_text() 함수를 이용한 예측 응답 결과를 문장으로 변환한다.
    results = convert_index_to_text(results, END_TOKEN)

    return results

while True:
    user_input = input("<< 말을 걸어보세요!\n")
    # "q" 입력시 종료
    if user_input == "q":
        break
    # 입력받은 질문을 run_chatbot() 함수에 대입하고 예측한 문장을 출력한다.
    print(f">> 챗봇 응답 : {run_chatbot(user_input)}")