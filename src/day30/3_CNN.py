# day 30 > 3_CNN.py

# 1. 데이터셋 로드, 10가지 종류의 의류 이미지 데이터셋

import tensorflow as tf
import matplotlib.pyplot as plt
import cv2

fashion_mnist = tf.keras.datasets.fashion_mnist

(x_train, y_train), (x_valid, y_valid) = fashion_mnist.load_data()

x_train = x_train / 255.0
x_valid = x_valid / 255.0

x_train_in = x_train[..., tf.newaxis]
x_valid_in = x_valid[..., tf.newaxis]



"""
0	Img	2 (Pullover)
1	Img	1 (Trouser)
2	Img	8 (Bag)
3	Img	4 (Coat)
4	Img	1 (Trouser)
5	Img	9 (Ankle boot)
6	Img	2 (Pullover)
7	Img	2 (Pullover)
8	Img	0 (T-shirt/top)
9	Img	2 (Pullover)
"""

# Functional API 이용한 모델 생성 (다중 입력)과 예측 테스트

# 입력을 (28, 28, 3)으로 변경하여 RGB 이미지 입력으로 설정
inputs = tf.keras.layers.Input(shape=(28, 28, 1))

# CNN 레이어
conv = tf.keras.layers.Conv2D(32, (3, 3), activation="relu")(inputs)
pool = tf.keras.layers.MaxPooling2D((2, 2))(conv)
flat = tf.keras.layers.Flatten()(pool)

# 입력을 직접 펼친 후 연결
flat_inputs = tf.keras.layers.Flatten()(inputs)

# CNN의 출력과 원본 입력을 결합
concat = tf.keras.layers.Concatenate()([flat, flat_inputs])

# 최종 출력 레이어
outputs = tf.keras.layers.Dense(10, activation="softmax")(concat)

# 모델 생성
model = tf.keras.models.Model(inputs=inputs, outputs=outputs)

# 모델 구조 확인
# model.summary()

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

model.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])

history = model.fit(x_train_in, y_train, validation_data = (x_valid_in, y_valid), epochs = 10)


val_loss, val_acc = model.evaluate(x_valid_in, y_valid)
# print(val_loss, val_acc)    # 10.860957145690918 0.8812999725341797

def plot_image(data, idx):
    plt.figure(figsize=(5, 5))
    plt.imshow(data[idx])
    plt.axis("off")
    plt.show()

# plot_image(x_valid, 1)

img = cv2.imread("bag.jpg")
# print(img)
"""
[[[247 249 250]
  [247 249 250]
  [247 249 250]
  ...
  [247 249 250]
  [247 249 250]
  [247 249 250]]

 [[247 249 250]
  [247 249 250]
  [247 249 250]
  ...
  [247 249 250]
  [247 249 250]
  [247 249 250]]

 [[247 249 250]
  [247 249 250]
  [247 249 250]
  ...
  [247 249 250]
  [247 249 250]
  [247 249 250]]

 ...

 [[247 249 250]
  [247 249 250]
  [247 249 250]
  ...
  [247 249 250]
  [247 249 250]
  [247 249 250]]

 [[247 249 250]
  [247 249 250]
  [247 249 250]
  ...
  [247 249 250]
  [247 249 250]
  [247 249 250]]

 [[247 249 250]
  [247 249 250]
  [247 249 250]
  ...
  [247 249 250]
  [247 249 250]
  [247 249 250]]]
"""
# print(img.shape)    # (714, 767, 3)
img = cv2.resize(img, dsize=(28, 28))
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print(img.shape)    # (28, 28, 3)

img = img / 255.0

result = model.predict(img[tf.newaxis, ...])
# print(tf.argmax(result[0]).numpy()) # 8

img1 = cv2.imread("shoes.png")

img1 = cv2.resize(img1, dsize=(28, 28))
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img1 = img / 255.0

result1 = model.predict(img1[tf.newaxis, ...])
print(tf.argmax(result1[0]).numpy())    # 5
