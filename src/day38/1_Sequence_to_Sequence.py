# day39 > 1_Sequence_to_Sequence.py

import numpy as np
import warnings
import tensorflow as tf
import pandas as pd
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.utils.version_utils import training

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

    return " ".join(okt.morphs(sentence))   # 형태소 분석 결과를 하나의 문자열로 합기치

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
        self.embedding = Embedding(vocab_size, embedding_dim, input_length=time_steps)

        # 드롭아웃 레이어
        self.dropout = Dropout(0.2)

        # LSTM 레이어
        self.lstm = LSTM(units, return_state=True)

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
        return [hidden_state, cell_state]   #

# 디코더, 텐서플로의 Model 클래스로부터 상속받아서 디코더 클래스 정의
class Decoder(tf.keras.Model):
    def __init__(self, units, vocab_size, embedding_dim, time_steps):
        super(Decoder, self).__init__()
        self.embedding = Embedding(vocab_size, embedding_dim, input_length=time_steps)

        self.dropout = Dropout(0.2)
        self.lstm = LSTM(units, return_state= True, return_sequences=True)

        self.dense = Dense(vocab_size, activation = "softmax")

    def call(self, inputs, initial_state):
        x = self.embedding(inputs)
        x = self.dropout(x)
        x, hidden_state, cell_state = self.lstm(x, initial_state = initial_state)
        x = self.dense(x)
        return x, hidden_state, cell_state

# 모델 결합
class Seq2Seq(tf.keras.Model):
    def __init__(self, units, vocab_size, embedding_dim, time_steps, start_token, end_token):
        super(Seq2Seq, self).__init__()
        self.start_token = start_token
        self.end_token = end_token
        self.time_steps = time_steps

        self.encoder = Encoder(units, vocab_size, embedding_dim, time_steps)
        self.decoder = Decoder(units, vocab_size, embedding_dim, time_steps)

    def call(self, inputs, training = True):
        if training :
            encoder_inputs, decoder_inputs = inputs
            context_vector = self.encoder(encoder_inputs)
            decoder_outputs, _, _ = self.decoder(inputs = decoder_inputs, initial_state = context_vector)

            return decoder_outputs
        else :
            context_vector = self.encoder(inputs)
            target_seq = tf.constant([[self.start_token]], dtype = tf.float32)
            results = tf.TensorArray(tf.int32, self.time_steps)

            for i in tf.range(self.time_steps):
                decoder_output, decoder_hidden, decoder_cell = self.decoder(target_seq, initial_state = context_vector)

                decoder_output = tf.cast(tf.argmax(decoder_output, axis= -1), dtype = tf.int32)

                decoder_output = tf.reshape(decoder_output, shape = (1, 1))

                results = results.write(i, decoder_output)

                if decoder_output == self.end_token:
                    break

                target_seq = decoder_output
                context_vector = [decoder_hidden, decoder_cell]

            return tf.reshape(results.stack(), shape = (1, self.time_steps))


VOCAB_SIZE = len(tokenizer.word_index) + 1
def convert_to_one_hot(padded):
    # 원 핫 인코딩 초기화
    one_hot_vector = np.zeros((len(answer_out_padded), MAX_LENGTH, VOCAB_SIZE))

    # 디코더 목표를 원 핫 인코딩으로 변환
    # 학습 시 입력은 인덱스 이지만 출력은 원 핫 인코딩 형식임
    for i, sequence in enumerate(answer_out_padded):
        for j, index in enumerate(sequence):
            one_hot_vector[i, j, index] = 1

    return one_hot_vector

answer_in_one_hot = convert_to_one_hot(answer_in_padded)
answer_out_one_hot = convert_to_one_hot(answer_out_padded)
# print(answer_in_one_hot[0].shape)   # (30, 2303)
# print(answer_out_one_hot[0].shape)  # (30, 2303)

def convert_index_to_text(indexs, end_token):

    sentence = ""

    # 모든 문장에 대해서 반복
    for index in indexs:
        if index == end_token:
            # 끝 단어이므로 예측 준비
            break

        # 사전에 존재하는 단어의 경우 단어 추가
        if index > 0 and tokenizer.index_word[index] is not None :
            sentence += tokenizer.index_word[index]

        else:
            # 사전에 없는 인덱스면 빈 문자열 추가
            sentence += ""

        # 빈 칸 추가
        sentence += ""

    return sentence

# 훈련 시 필요한 파라미터 값 정의
BUFFER_SIZE = 1000
BATCH_SIZE = 16
EMBEDDING_DIM = 100
TIME_STEPS = MAX_LENGTH
START_TOKEN = tokenizer.word_index["<START>"]
END_TOKEN = tokenizer.word_index["<END>"]

UNITS = 128

VOCAB_SIZE = len(tokenizer.word_index) + 1
DATA_LENGTH = len(questions)
SAMPLE_SIZE = 3
NUM_EPOCHS = 20

# 모델 저장할 수 있도록 체크포인트 생성
checkpoint_path = "model/seq2seq-chatbot-checkpoint.ckpt"
checkpoint = ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, monitor="loss", verbose=1)

# seq2seq
seq2seq = Seq2Seq(UNITS, VOCAB_SIZE, EMBEDDING_DIM, TIME_STEPS, START_TOKEN, END_TOKEN)
seq2seq.compile(optimizer="adam", loss = "categorical_crossentropy", metrics=["acc"])

def make_prediction(model, question_inputs):
    results = model(inputs = question_inputs, training = False)
    # 변환된 인덱스를 문장으로 변환
    results = np.asarray(results).reshape(-1)

    return results

for epoch in range(NUM_EPOCHS):
    print(f"processing epoch: {epoch * 10 + 1}...")
    seq2seq.fit([question_padded, answer_in_padded], answer_out_one_hot, epochs = 10, batch_size = BATCH_SIZE, callbacks = [checkpoint])

    # 랜덤한 샘플 번호 추출
    samples = np.random.randint(DATA_LENGTH, size = SAMPLE_SIZE)

    # 예측 성능 테스트
    for idx in samples:
        question_inputs = question_padded[idx]

        # 문장 예측
        results = make_prediction(seq2seq, np.expand_dims(question_inputs, 0))

        # 변환된 인덱스를 문장으로 변환
        results = convert_index_to_text(results, END_TOKEN)

        print(f"Q : {questions[idx]}")
        print(f"A : {results}\n")
        print()

