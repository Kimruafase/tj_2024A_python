# day26 > 2_단순_신경망.py
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# 1. 임의 데이터, x와 임의의 1차 함수
x = np.arange(1, 6)
print(x)

y = (3 * x) + 2
print(y)

# 2. 시각화
plt.plot(x, y)
plt.show()

# 3. Sequential API 모델, 여러 층을 이어붙이듯 시퀀스에 맞게 일렬로 연결하는 방식
    # 입력 레이어 / 층 -> 출력 레이어 / 층까지 순서를 갖는다.
    # 순서대로 각 층 / 레이어를 하나씩 통과하면서 딥러닝 연산을 수행한다.

# (1) 방법 1 : 리스트형
# model = tf.keras.Sequential([tf.keras.layers.Dense(10), tf.keras.layers.Dense(5), tf.keras.layers.Dense(1)])
                                # 레이어 1                     # 레이어 2                 # 레이어 3

# (2) 방법 2 : add 함수 사용
# model1 = tf.keras.Sequential()
# model1.add(tf.keras.layers.Dense(10))   # 레이어 1
# model1.add(tf.keras.layers.Dense(5))    # 레이어 2
# model1.add(tf.keras.layers.Dense(1))    # 레이어 3
# tip : 레이어의 갯수는 제한이 없다.

# (3) 입력 데이터의 형태
    # 데이터셋 (150, 4) -> 150개의 데이터(행), 4개의 입력변수 / 독립변수(열)
# model2 = tf.keras.Sequential([tf.keras.layers.Dense(10, imput_shape = [4]), tf.keras.layers.Dense(5), tf.keras.layers.Dense(1)])
           # 레이어 1 : 첫번째 레이어가 입력 레이어, 반드시 input_shape 매개변수를 지정해야함   # 레이어 2                 # 레이어 3

# (4) 단순 선형회귀 모델 정의
    # 1개의 노드(뉴런)를 갖는 레이어는 1개의 출력값을 가지므로 출력값은 y에 대한 모델의 예측값이다.
    # 모델 생성
model3 = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape = [1])])
# print(model3.summary())
"""
Model: "sequential"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense (Dense)                   │ (None, 1)              │             2 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 2 (8.00 B)
 Trainable params: 2 (8.00 B)
 Non-trainable params: 0 (0.00 B)
"""

    # 모델 컴파일
# model3.compile(optimizer = "sgd", loss = "mse", metrics = ["mae"])

    # 모델 훈련
# history = model3.fit(x, y, epochs = 1200)   # x(독립변수), y(종속변수) 를 1200번 학습, loss(오차), mae(평균 제곱 오차)

    # 시각화
# plt.plot(history.history["loss"], label="loss")
# plt.plot(history.history["mae"], label = "mae")
# plt.show()

# (5) 컴파일
    # 1. 긴 문자열 지정
model3.compile(optimizer = "sgd", loss="mean_squared_error", metrics = ["mean_squared_error", "mean_absolute_error"])

    # 2. 짧은 문자열 지정
model3.compile(optimizer = "sgd", loss="mse", metrics= ["mse", "mae"])

    # 3. 클래스 인스턴스 지정
model3.compile(optimizer = tf.keras.optimizers.SGD(learning_rate=0.005), # 텐서플로2 에서는 lr 대신 learning_rate로 작성한다.
               loss = tf.keras.losses.MeanAbsoluteError(),
               metrics = [tf.keras.metrics.MeanAbsoluteError(), tf.keras.metrics.MeanSquaredError()])

    # optimizer = "sgd" -> 확률적 경사하강법 알고리즘
    # 4. 단순선형회귀 모델의 컴파일
model3.compile(optimizer= "sgd", loss="mse", metrics=["mae"])

    # (6) 훈련
history = model3.fit(x, y, epochs = 1200)
print(history)

    # (7) 시각화
plt.plot(history.history["loss"])
plt.plot(history.history["mae"])
plt.xlim(-1,20)
plt.show()

    # (8) 검증
print(model3.evaluate(x, y))    # [5.1232091209385544e-05, 0.006143665406852961]

    # (9) 예측
print(model3.predict(np.array([10])))   # epochs = 1200, x = 10 일 때 y 예측값 = [[32.029694]]