# day27 > 1_심층_신경망.py
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# keras에 내장된 데이터셋에서 mnist(손글씨 이미지) 데이터셋 로드
mnist = tf.keras.datasets.mnist
# print(mnist)

# 데이터 로드
(x_train, y_train),(x_test, y_test) = mnist.load_data()
    # (데이터 크기, 세로 픽셀, 가로 픽셀) (28, 28) 픽셀 크기의 정사각형 이미지 6만개 저장된 상태
# print(x_train.shape)    # (60000, 28, 28)
# print(y_train.shape)    # (60000,)
# print(x_test.shape)     # (10000, 28, 28)
# print(y_test.shape)     # (10000,)

# 시각화
fig, axes = plt.subplots(3, 5)  # 3행 5열 여러개 차트 표현

fig.set_size_inches(8, 5)   # 전체 차트의 크기를 가로 8인치 세로 5인치

for i in range(15):
    ax = axes[i // 5, i % 5]    # i // 5 = 몫(행 인덱스), i % 5 = 나머지 (열 인덱스)
    # i = 0 -> 0 // 5 = 0, 0 % 5 = 0 -> [0, 0]
    # i = 1 -> 1 // 5 = 0, 1 % 5 = 1 -> [0, 1]
    # i = 2 -> 2 // 5 = 0, 2 % 5 = 2 -> [0, 2]
    ax.imshow(x_train[i])
    ax.axis("off")
    ax.set_title(y_train[i])

plt.show()

# 데이터 전처리, [0 -> 첫번째 이미지, 10:15 -> 특정한 픽셀만 확인하기 위해 범위 지정 10:15]
# print(x_train[0, 10:15, 10:15])
"""
[[  1 154 253  90   0]
 [  0 139 253 190   2]
 [  0  11 190 253  70]
 [  0   0  35 241 225]
 [  0   0   0  81 240]]
"""

# 0 ~ 255 사이가 아닌 0 ~ 1 사이를 가질 수 있도록 범위를 정규화
# print(x_train.min())    # 0
# print(x_train.max())    # 255

# 데이터 정규화
x_train = x_train / x_train.max() # 값 / 최댓값, 각 값들을 / 255
# print(x_train.min(), x_train.max()) # 0.0, 1.0

x_test = x_test / x_test.max() # 테스트용 데이터 정규화
# print(x_test.min(), x_train.max())  # 0.0, 1.0

# print(x_train[0, :, :]) # 손글씨 데이터 정규화한 후 출력

# Dense 레이어에는 1차원 배열만 들어갈 수 있으므로 2차원 데이터 배열을 1차원으로 변경
    # 방법 1) TensorFlow reshape()
# print(x_train.reshape(60000, -1).shape) # (60000, 784) -> 1차원 (데이터수 , 가로 * 세로)

    # 방법 2) Flatten 레이어
# print(tf.keras.layers.Flatten()(x_train).shape) # (60000, 784)

# 방법 1) 레이어에 활성화 함수 적용 -> relu 함수 적용
    # 128개의 노드, relu 활성화 함수를 적용하는 레이어
tf.keras.layers.Dense(128, activation="relu")

# 방법 2)
    # 출력층이 128개의 노드로 구성된 모델 직접 정의
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128),         # 128개 노드의 레이어 1개
    tf.keras.layers.Activation("relu")  # 별도로 활성화 함수 레이어 추가
])                                      # 입력층 명시된 상태 아니고, 1개의 레이어 정의는 출력층이다.

# 모델 생성
model1 = tf.keras.Sequential([
        # 2차원 (이미지)을 1차원 변환 : Flatten 패턴
        # 28 * 28 = 784 개의 데이터를 갖는 1차원 배열
    tf.keras.layers.Flatten(input_shape=(28, 28)),      # 입력층, 독립변수 784개
        # 각 레이어들 간의 연결된 완전 연결층이다.
        # 각 256, 64, 32 개의 노드를 갖는 은닉층 3개
        # 각 활성화 함수는 ReLU라는 비선형적 활성화 함수 적용
    tf.keras.layers.Dense(256, activation = "relu"),    # 은닉층
    tf.keras.layers.Dense(64, activation = "relu"),     # 은닉층
    tf.keras.layers.Dense(32, activation = "relu"),     # 은닉층
    tf.keras.layers.Dense(10, activation = "softmax")   # 출력층, 종속변수 10개로 분류
        # 정답은 0 ~ 9 사이의 손글씨 정답 # 0 or 1 or 2 or 3 --- or 9
])  # 각 레이어(은닉층) 갯수, 각 노드의 갯수는 중요한 하이퍼 파라미터가 된다.

# print(model1.summary())
"""
Model: "sequential_1"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten (Flatten)               │ (None, 784)            │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_2 (Dense)                 │ (None, 256)            │       200,960 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_3 (Dense)                 │ (None, 64)             │        16,448 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_4 (Dense)                 │ (None, 32)             │         2,080 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_5 (Dense)                 │ (None, 10)             │           330 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 219,818 (858.66 KB)
 Trainable params: 219,818 (858.66 KB)
 Non-trainable params: 0 (0.00 B)
"""

# (1) 이진 분류 : 출력 노드가 1개, sigmoid 일 경우
model1.compile(loss = "binary_crossentropy")

# (2) y가 원 핫 벡터인 경우
    # y = 5 인 경우 원 핫 벡터 -> [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
model1.compile(loss = "categorial_crossentropy")
"""
    원 핫 벡터 / 인코딩
        > 결과 (0, 1, 2, 3, 4) 일 때
            [1, 0, 0, 0, 0]
            [0, 1, 0, 0, 0]
            > 특정 클래스에 해당하는 위치만 1이고 나머지가 모두 0으로 설정하는 방식
        
"""
# (3) y가 원 핫 벡터가 아닐 경우
    # y = 5
model1.compile(loss = "sparse_categorial_crossentropy")

# 옵티마이저
# (1) 클래스로 지정하는 방법
adam = tf.keras.optimizers.Adam(learning_rate = 0.001)
model1.compile(optimizer = adam)

# (2) 문자열로 지정하는 방법
model1.compile(optimizer = "adam")

# 평가지표
# (1) 클래스 지정 방식
acc = tf.keras.metrics.SparseCategoricalAccuracy()
model1.compile(optimizer = "adam",
               loss = "sparse_categorical_crossentropy",
               metrics = [acc])

# (2) 문자열 지정 방식
model1.compile(optimizer = "adam",
               loss = "sparse_categorical_crossentropy",
               metrics = ["accuracy"])

# 훈련, fit(훈련용 독립변수, 훈련용 종속변수, epochs = 반복 횟수, validation_data = (테스트용 독립변수, 테스트용 종속변수)
model1.fit(x_train, y_train, epochs = 10, validation_data = (x_test, y_test))
"""
Epoch 1/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 5s 2ms/step - accuracy: 0.8677 - loss: 0.4342 - val_accuracy: 0.9645 - val_loss: 0.1194

Epoch 10/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 4s 2ms/step - accuracy: 0.9955 - loss: 0.0134 - val_accuracy: 0.9751 - val_loss: 0.1125
    > Epoch : 현재 훈련중인 반복(에포크) 수
    > 35 / 1875 : 현재 진행중인 배치의 번호
        > 배치 번호 1875개 -> 총 데이터 갯수가 6만개 -> 총 배치 수 32개 -> 총 데이터 수 / 총 배치 수
    > 배치 : 모델 훈련에서 전체를 구분한 집합 수 -> 주로 32개 64개 128개를 사용 -> 기본값은 32개 사용한다.
"""

# 평가
test_loss, test_acc = model1.evaluate(x_test, y_test)
"""
313/313 ━━━━━━━━━━━━━━━━━━━━ 0s 1ms/step - accuracy: 0.9747 - loss: 0.1018
"""
# print(test_acc) # 0.9793999791145325

# 예측
predictions = model1.predict(x_test)
# print(predictions[0])
"""
[1.9102808e-17 9.5256246e-13 2.2058959e-08 2.4449614e-08 1.6589677e-14
 8.6278525e-14 4.2015531e-25 1.0000000e+00 1.3001281e-15 2.6053670e-10]
"""
# 가장 확률이 높은 것만 추출
print(np.argmax(predictions[0]))    # 7 (인덱스)

# 가장 앞에 있는 10개 예측값 확인 -> np.argmax( , axis = 차원 수)
print(np.argmax(predictions[:10], axis = 1))    # [7 2 1 0 4 1 4 9 5 9]

print(y_test[: 10]) # 실제 정답 확인 : [7 2 1 0 4 1 4 9 5 9]

# 시각화
def get_one_result(idx):
                                        # 테스트 독립변수, 테스트 종속변수 / 정답, 확률이 높은 인덱스 = 예측값, 확률이 높은 값의 백분율
    img, y_true, y_pred, confidence = x_test[idx], y_test[idx], np.argmax(predictions[idx]), 100 * np.max(predictions[idx])

    return img, y_true, y_pred, confidence

fig, axes = plt.subplots(3, 5)
fig.set_size_inches(12, 10)
for i in range(15):                         # 0 ~ 14 까지 반복
    ax = axes[i // 5, i % 5]
    img, y_true, y_pred, confidence = get_one_result(i)

    # imshow()로 시각화
    ax.imshow(img, cmap="gray")

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(f"True : {y_true}")        # 정답을 차트 제목
    ax.set_xlabel(f"Prediction : {y_pred}\nConfidence : {confidence:.2f}%")

plt.tight_layout()
plt.show()