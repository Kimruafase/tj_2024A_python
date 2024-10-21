# day35 > 1_RNN.py

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional


# 1. 임베딩 레이어 구현, Embedding(n, m) : 임베딩 클래스, n = 단어 수, m = 차원 수
embedding_layer = tf.keras.layers.Embedding(100, 3) # 100개의 단어, 3차원
result = embedding_layer(tf.constant([12, 8, 15, 20]))  # 숫자 4개를 입력 데이터를 임의로 넣어줌

# print(result) # 각 임의의 데이터 4개를 임베딩 layer를 통해 3개의 숫자로 변환하여 표현된다.
"""
tf.Tensor(
[[-0.00897998 -0.01044067 -0.00025607]
 [-0.04926343 -0.02560504  0.01989997]
 [ 0.00887088  0.02844012 -0.01358205]
 [-0.0385859   0.04946433  0.03304138]], shape=(4, 3), dtype=float32)
"""
# 결론 : 각 숫자(단어)를 의미하는 벡터로 바꾸어주는 임베딩 레이어 역할

# 2. Embedding Layer 활용 .add() 를 통해서 레이어 추가
model = tf.keras.Sequential()
    # 100개의 단어를 3차원 벡터로 변환하겠다는 속성값 대입, 최대 입력값 32개로 하겠다.
model.add(tf.keras.layers.Embedding(100, 3, input_length=32))
    # 32개의 결과를 예측
model.add(tf.keras.layers.LSTM(units=32))   # Long Short - Term Memory : 긴 문장에서 중요한 정보는 기억하는 RNN
    # 출력(결과) 레이어, 결과를 1개로 출력
model.add(tf.keras.layers.Dense(units=1))
# model.summary()
"""
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding_1 (Embedding)     (None, 32, 3)             300       
                                                                 
 lstm (LSTM)                 (None, 32)                4608      
                                                                 
 dense (Dense)               (None, 1)                 33        
                                                                 
=================================================================
Total params: 4,941
Trainable params: 4,941
Non-trainable params: 0
_________________________________________________________________
"""

# 2 - 1. 라이브러리 호출해서 모델 생성
model = Sequential()
model.add(Embedding(100, 3, input_length=32))
model.add(LSTM(32))
model.add(Dense(1))
# model.summary()
"""
Model: "sequential_1"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding_2 (Embedding)     (None, 32, 3)             300       
                                                                 
 lstm_1 (LSTM)               (None, 32)                4608      
                                                                 
 dense_1 (Dense)             (None, 1)                 33        
                                                                 
=================================================================
Total params: 4,941
Trainable params: 4,941
Non-trainable params: 0
_________________________________________________________________
"""

# 3. 양방향 순환 신경망
model = Sequential()
model.add(Embedding(100, 3)) # 임베딜 : 총 단어 수 -> 100, 차원 수 -> 3, 매개변수의 수 : 100 * 3 = 300
model.add(Bidirectional(LSTM(32)))  # LSTM 구조를 양방향으로 설정, 유닛의 개수가 32 * 2가 되어 64개가 된다.
model.add(Dense(1))
# model.summary()
"""
Model: "sequential_2"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding_3 (Embedding)     (None, None, 3)           300       
                                                                 
 bidirectional (Bidirectiona  (None, 64)               9216      
 l)                                                              
                                                                 
 dense_2 (Dense)             (None, 1)                 65        
                                                                 
=================================================================
Total params: 9,581
Trainable params: 9,581
Non-trainable params: 0
_________________________________________________________________
"""

# 4. Stacking RNN
model = Sequential()
model.add(Embedding(100 , 32))  # 총 100개의 단어, 32차원 사용
model.add(LSTM(32, return_sequences=True))  # 32개의 유닛, 모든 t에 대해서 출력 허용
model.add(LSTM(32)) # 최상단 RNN에서는 모든 상태를 전달할 필요가 없어 return_sequences 설정 필요 X
model.add(Dense(1))
# model.summary()
"""
Model: "sequential_3"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding_4 (Embedding)     (None, None, 32)          3200      
                                                                 
 lstm_3 (LSTM)               (None, None, 32)          8320      
                                                                 
 lstm_4 (LSTM)               (None, 32)                8320      
                                                                 
 dense_3 (Dense)             (None, 1)                 33        
                                                                 
=================================================================
Total params: 19,873
Trainable params: 19,873
Non-trainable params: 0
_________________________________________________________________
"""

# 5. 순환 드롭아웃
model = Sequential()
model.add(Embedding(100, 32))
    # recurrent_dropout = 0.2 -> LSTM의 순환 드롭아웃 비율
    # 순환 상태의 출력을 다음 상태의 입력으로 사용할 때, 20%를 무작위로 제거하여 과대적합 방지
    # dropout = 0.2 -> 일반 드롭아웃 비율
    # 입력으로 들어오는 데이터로 사용할 때 20%를 무작위로 제거하여 과대적합 방지
model.add(LSTM(32, recurrent_dropout=0.2, dropout=0.2))
model.add(Dense(1, activation="sigmoid"))
# model.summary()
"""
Model: "sequential_4"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding_5 (Embedding)     (None, None, 32)          3200      
                                                                 
 lstm_5 (LSTM)               (None, 32)                8320      
                                                                 
 dense_4 (Dense)             (None, 1)                 33        
                                                                 
=================================================================
Total params: 11,553
Trainable params: 11,553
Non-trainable params: 0
_________________________________________________________________
"""