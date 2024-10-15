# day30 > 1_CNN.py

"""
    > 딥러닝 프로세스(절차)
        > 1. 데이터 수집
        > 2. 데이터 전처리 : 수집된 데이터를 신경망 모델에 적합하게 수정
        > 3. 데이터 분할 : 훈련용 데이터와 검증 / 테스트용 데이터로 분할, 주로 7 : 3 or 8 : 2
        > 4. 모델 설계(구축)
            > 1) Sequential API, Functional API
            > 2) 레이어 구성 : 입력층 -> 은닉층(conv2D, MaxPooling2D, Flatten) 등등 -> 은닉층 -> 출력층 구성
            > 3) 활성화 함수 : 각 레이어에서 학습된 값을 비선형으로 변환할 때 사용, 주로 Relu, softmax 함수 상ㅇ
            > 4) 손실 함수

        > 5. 모델 컴파일 : 모델을 어떻게 학습하고 평가하는 지 설명
            > 1) 옵티마이저 : 모델의 가중치를 업데이트하는 계산법, adam : 학습률을 기반으로 하는 최적화 알고리즘, sgd : 확률적 경사 하강법
            > 2) 손실 함수 : 실제값과 예측값의 차이, 분류 모델 : spare_categorical_crossentropy, 회귀 : mean_squared_error
            > 3) 평가 지표 : 모델의 성능을 평가하는 지표, 분류 모델 : accuracy, 회귀 : mse
        > 6. 모델 학습
            > 1) epoch : 전체 훈련 데이터를 1번 학습하는 횟수
            > 2) 검증 : validation_data 학습 중에 검증 / 테스트 데이터를 사용하여 모델의 손실, 평가를 확인할 수 있다.
        > 7. 모델 평가 -> 모델 튜닝(최적의 하이퍼 파라미터)
            > 1) evaluation() : 최종 성능의 손실 함수와 평가 지표 결과를 볼 수 있다.
            -> 모델 튜닝(하이퍼 파라미터)
                > 학습률, 배치 크기, 레이어 수, 뉴런(노드) 수, 할성화 함수, 에포크 등을 여러 하이퍼 파라미터 조정
        > 8. 모델 예측
            > 1) predict()
"""

# 1. 데이터셋 준비

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_valid, y_valid) = mnist.load_data()

# print(x_train.shape, y_train.shape) # (60000, 28, 28) (60000,)
# print(x_valid.shape, y_valid.shape) # (10000, 28, 28) (10000,)

y_train_odd = []

for y in y_train:
    if y % 2 == 0:
        y_train_odd.append(0)
    else:
        y_train_odd.append(1)

y_train_odd = np.array(y_train_odd)

# print(y_train_odd.shape)    # (60000,)

# print(y_train[:10])     # [5 0 4 1 9 2 1 3 1 4]
# print(y_train_odd[:10]) # [1 0 0 1 1 0 1 1 1 0]

y_valid_odd = []

for y in y_valid:
    if y % 2 == 0:
        y_valid_odd.append(0)
    else:
        y_valid_odd.append(1)

y_valid_odd = np.array(y_valid_odd)

# print(y_valid_odd.shape)    # (10000,)

x_train = x_train / 255.0
x_valid = x_valid / 255.0

x_train_in = tf.expand_dims(x_train, -1)
x_valid_in = tf.expand_dims(x_valid, -1)

# print(x_train_in.shape, x_valid_in.shape)   # (60000, 28, 28, 1) (10000, 28, 28, 1)

# 모델 생성
    # 입력 레이어
inputs = tf.keras.layers.Input(shape = (28, 28, 1))

    # 합성곱 레이어
conv = tf.keras.layers.Conv2D(32, (3, 3), activation = "relu")(inputs)
    # 풀링 레이어
pool = tf.keras.layers.MaxPooling2D((2, 2))(conv)
    # 플래튼 레이어
flat = tf.keras.layers.Flatten()(pool)

    # 단순 입력 구조 추가
flat_inputs = tf.keras.layers.Flatten()(inputs)
    # 2개 입력 구조를 1개 출력으로 만들기 -> 합치기
concat = tf.keras.layers.Concatenate()([flat, flat_inputs])
    # 출력 레이어
outputs = tf.keras.layers.Dense(10, activation = "softmax")(concat)

    # 모델 생성
model = tf.keras.models.Model(inputs = inputs, outputs = outputs)

# print(model.summary())
"""
Model: "functional"
┌─────────────────────┬───────────────────┬────────────┬───────────────────┐
│ Layer (type)        │ Output Shape      │    Param # │ Connected to      │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ input_layer         │ (None, 28, 28, 1) │          0 │ -                 │
│ (InputLayer)        │                   │            │                   │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ conv2d (Conv2D)     │ (None, 26, 26,    │        320 │ input_layer[0][0] │
│                     │ 32)               │            │                   │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ max_pooling2d       │ (None, 13, 13,    │          0 │ conv2d[0][0]      │
│ (MaxPooling2D)      │ 32)               │            │                   │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ flatten (Flatten)   │ (None, 5408)      │          0 │ max_pooling2d[0]… │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ flatten_1 (Flatten) │ (None, 784)       │          0 │ input_layer[0][0] │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ concatenate         │ (None, 6192)      │          0 │ flatten[0][0],    │
│ (Concatenate)       │                   │            │ flatten_1[0][0]   │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ dense (Dense)       │ (None, 10)        │     61,930 │ concatenate[0][0] │
└─────────────────────┴───────────────────┴────────────┴───────────────────┘
 Total params: 62,250 (243.16 KB)
 Trainable params: 62,250 (243.16 KB)
 Non-trainable params: 0 (0.00 B)
"""

# 모델 컴파일
# model.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics=["accuracy"])

# 모델 훈련
# history = model.fit(x_train_in, y_train, validation_data = (x_valid_in, y_valid), epochs = 10)

# 모델 성능 평가
# val_loss, val_acc = model.evaluate(x_valid_in, y_valid)
# print(val_loss, val_acc) # 0.0676252618432045 0.9818000197410583

# 다중 분류 출력 모델
    # 1. 다중분류[0 ~ 9], 이진분류[0, 1]
    
    # 1) 입력 1
inputs1 = tf.keras.layers.Input(shape = (28, 28, 1), name= "inputs")

    # 2) 다중 레이어(은닉층)
conv1 = tf.keras.layers.Conv2D(32, (3, 3), activation="relu", name= "conv2d_layer")(inputs1)
pool1 = tf.keras.layers.MaxPooling2D((2, 2), name = "maxpool_layer")(conv1)
flat1 = tf.keras.layers.Flatten(name= "flatten_layer")(pool1)

    # 3) 입력 2
flat_inputs1 = tf.keras.layers.Flatten()(inputs1)
    # 4) 플래튼 레이어와 입력 2 레이어 합치기
concat1 = tf.keras.layers.Concatenate()([flat1, flat_inputs1])
    # 5) 출력 레이어 2개 (digit_outputs : 다중 분류 출력, odd_outputs : 이진 분류 출력)
digit_outputs = tf.keras.layers.Dense(10, activation = "softmax", name="digit_dense")(concat1)
odd_outputs = tf.keras.layers.Dense(1, activation = "sigmoid", name = "odd_dense")(flat_inputs1)

    # 6) 모델 생성
model1 = tf.keras.Model(inputs = inputs1, outputs = [digit_outputs, odd_outputs])

# print(model1.summary())
"""
Model: "functional_1"
┌─────────────────────┬───────────────────┬────────────┬───────────────────┐
│ Layer (type)        │ Output Shape      │    Param # │ Connected to      │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ inputs (InputLayer) │ (None, 28, 28, 1) │          0 │ -                 │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ conv2d_layer        │ (None, 26, 26,    │        320 │ inputs[0][0]      │
│ (Conv2D)            │ 32)               │            │                   │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ maxpool_layer       │ (None, 13, 13,    │          0 │ conv2d_layer[0][… │
│ (MaxPooling2D)      │ 32)               │            │                   │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ flatten_layer       │ (None, 5408)      │          0 │ maxpool_layer[0]… │
│ (Flatten)           │                   │            │                   │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ flatten_2 (Flatten) │ (None, 784)       │          0 │ inputs[0][0]      │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ concatenate_1       │ (None, 6192)      │          0 │ flatten_layer[0]… │
│ (Concatenate)       │                   │            │ flatten_2[0][0]   │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ digit_dense (Dense) │ (None, 10)        │     61,930 │ concatenate_1[0]… │
├─────────────────────┼───────────────────┼────────────┼───────────────────┤
│ odd_dense (Dense)   │ (None, 1)         │        785 │ flatten_2[0][0]   │
└─────────────────────┴───────────────────┴────────────┴───────────────────┘
 Total params: 63,035 (246.23 KB)
 Trainable params: 63,035 (246.23 KB)
 Non-trainable params: 0 (0.00 B)
"""

# print(model1.input) # <KerasTensor shape=(None, 28, 28, 1), dtype=float32, sparse=False, name=inputs>
# print(model1.output)    # [<KerasTensor shape=(None, 10), dtype=float32, sparse=False, name=keras_tensor_12>, <KerasTensor shape=(None, 1), dtype=float32, sparse=False, name=keras_tensor_13>]

# 모델 컴파일, 다중 출력의 손실 함수는 loss ={}
model1.compile(optimizer = "adam", loss={"digit_dense" : "sparse_categorical_crossentropy", "odd_dense" : "binary_crossentropy"},
               loss_weights = {"digit_dense" : 1, "odd_dense" : 0.5},
               metrics={"digit_dense": ["accuracy"], "odd_dense": ["accuracy"]})

# 모델 훈련, 다중 출력시 훈련용과 검증용이 다중이 되므로 {"출력 레이어 name" : 출력 레이어 변수} 딕셔너리 구조를 사용
history1 = model1.fit({"inputs" : x_train_in}, {"digit_dense" : y_train, "odd_dense" : y_train_odd},
                      validation_data = ({"inputs" : x_valid_in}, {"digit_dense" : y_valid, "odd_dense" : y_valid_odd}),
                      epochs = 10)

# 모델 성능 평가
model1.evaluate({"inputs" : x_valid_in}, {"digit_dense" : y_valid, "odd_dense" : y_valid_odd})
# digit_dense_accuracy: 0.9790 - digit_dense_loss: 0.0734 - loss: 0.2057 - odd_dense_accuracy: 0.8988 - odd_dense_loss: 0.1324

# 모델 예측하기
def plot_image(data, idx):
    plt.figure(figsize = (5, 5))
    plt.imshow(data[idx])
    plt.axis("off")
    plt.show()

# plot_image(x_valid, 0)

digit_preds, odd_preds = model1.predict(x_valid_in)
# print(digit_preds[0])
"""
[7.0683325e-13 7.1075218e-10 3.4667731e-09 6.4605516e-08 2.8467294e-12
 2.6884967e-13 9.2883416e-22 9.9999988e-01 1.7655614e-10 5.4350657e-10]
"""
# print(odd_preds[0]) # [0.9996427]

digit_labels = np.argmax(digit_preds, axis = -1)
# print(digit_labels[0 : 10]) # [7 2 1 0 4 1 4 9 5 9]

odd_labels = (odd_preds > 0.5).astype(np.int32).reshape(1, -1)[0]
# print(odd_labels[0 : 10])   # [1 0 1 0 0 1 0 1 0 1]


# day31 > 1_CNN.py
# 전이학습(transfer learning)
# layer의 name 속성을 이용한 특정 레이어 추출
# (1) 기존의 Functional API 로 생성한 모델에서 특정 레이어를 추출해서 새로운 Functional API 모델 생성
    # 특정 layer와 연결된 layer 까지 추출 => conv <- pooling <- flatten
base_model_output = model1.get_layer("flatten_layer").output

base_model = tf.keras.models.Model(inputs = model1.input, outputs = base_model_output, name = "base")
base_model.summary()
"""
Model: "base"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ inputs (InputLayer)             │ (None, 28, 28, 1)      │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_layer (Conv2D)           │ (None, 26, 26, 32)     │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ maxpool_layer (MaxPooling2D)    │ (None, 13, 13, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten_layer (Flatten)         │ (None, 5408)           │             0 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 320 (1.25 KB)
 Trainable params: 320 (1.25 KB)
 Non-trainable params: 0 (0.00 B)
"""

# (2) 출력 layer를 추가하는 새로은 Sequential API로 모델 생성하기
digit_model = tf.keras.Sequential([base_model, tf.keras.layers.Dense(10, activation = "softmax")])
digit_model.summary()
"""
Model: "sequential"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ base (Functional)               │ (None, 5408)           │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_1 (Dense)                 │ (None, 10)             │        54,090 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 54,410 (212.54 KB)
 Trainable params: 54,410 (212.54 KB)
 Non-trainable params: 0 (0.00 B)
"""

# (3) 모델 컴파일
digit_model.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])

# (4) 모델 훈련
history2 = digit_model.fit(x_train_in, y_train, validation_data = (x_valid_in, y_valid), epochs = 10)

# (5)
base_model_frozen = tf.keras.models.Model(inputs = model1.input, outputs = base_model_output, name = "base_frozen")
base_model_frozen.trainable = False # 모델의 파라미터 값이 고정되어 훈련을 통해서 업데이트되지 않음 -> 훈련 X
base_model_frozen.summary()
"""
Model: "base_frozen"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ inputs (InputLayer)             │ (None, 28, 28, 1)      │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_layer (Conv2D)           │ (None, 26, 26, 32)     │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ maxpool_layer (MaxPooling2D)    │ (None, 13, 13, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten_layer (Flatten)         │ (None, 5408)           │             0 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 320 (1.25 KB)
 Trainable params: 0 (0.00 B)
 Non-trainable params: 320 (1.25 KB)
"""

# Functional API 적용으로 모델 생성
dense_output = tf.keras.layers.Dense(10, activation = "softmax")(base_model_frozen.output)
digit_model_frozen = tf.keras.models.Model(inputs = base_model_frozen.input, outputs = dense_output)
digit_model_frozen.summary()
"""
Model: "functional_3"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ inputs (InputLayer)             │ (None, 28, 28, 1)      │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_layer (Conv2D)           │ (None, 26, 26, 32)     │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ maxpool_layer (MaxPooling2D)    │ (None, 13, 13, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten_layer (Flatten)         │ (None, 5408)           │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_2 (Dense)                 │ (None, 10)             │        54,090 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 54,410 (212.54 KB)
 Trainable params: 54,090 (211.29 KB)
 Non-trainable params: 320 (1.25 KB)
"""

digit_model_frozen.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])
history3 = digit_model_frozen.fit(x_train_in, y_train, validation_data = (x_valid_in, y_valid), epochs = 10)

base_model_frozen2 = tf.keras.models.Model(inputs = model1.input, outputs = base_model_output, name = "base_frozen2")
    # 특정한 layer name 속성을 이용한 layer의 파라미터 값을 고정하고 훈련을 취소함
base_model_frozen2.get_layer("conv2d_layer").trainable = False
base_model_frozen2.summary()
"""
Model: "base_frozen2"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ inputs (InputLayer)             │ (None, 28, 28, 1)      │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_layer (Conv2D)           │ (None, 26, 26, 32)     │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ maxpool_layer (MaxPooling2D)    │ (None, 13, 13, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten_layer (Flatten)         │ (None, 5408)           │             0 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 320 (1.25 KB)
 Trainable params: 0 (0.00 B)
 Non-trainable params: 320 (1.25 KB)
"""

dense_output2 = tf.keras.layers.Dense(10, activation = "softmax")(base_model_frozen2.output)
digit_model_frozen2 = tf.keras.models.Model(inputs = base_model_frozen2.input, outputs = dense_output2)
digit_model_frozen2.summary()
"""
Model: "functional_4"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ inputs (InputLayer)             │ (None, 28, 28, 1)      │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_layer (Conv2D)           │ (None, 26, 26, 32)     │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ maxpool_layer (MaxPooling2D)    │ (None, 13, 13, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten_layer (Flatten)         │ (None, 5408)           │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_3 (Dense)                 │ (None, 10)             │        54,090 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 54,410 (212.54 KB)
 Trainable params: 54,090 (211.29 KB)
 Non-trainable params: 320 (1.25 KB)
"""

digit_model_frozen2.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])
history4 = digit_model_frozen2.fit(x_train_in, y_train, validation_data = (x_valid_in, y_valid), epochs = 10)