# day28 > 1_CNN.py

import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# 손글씨 데이터 로드
mnist = tf.keras.datasets.mnist
(x_train, y_train),(x_valid, y_valid) = mnist.load_data()

# 손글씨 데이터 행렬 데이터 확인
# print(x_train.shape, y_train.shape) # (60000, 28, 28) (60000,)
# print(x_valid.shape, y_valid.shape) # (10000, 28, 28) (10000,)

# 첫번째 숫자 데이터 시각화
def plot_image(data, idx):
    plt.figure(figsize=(5, 5))
    plt.imshow(data[idx], cmap="gray")
    plt.axis("off")
    plt.show()

# plot_image(x_train, 0)

# 최소 최대값 확인
# print(x_train.min(), x_train.max()) # 0 255
# print(x_valid.min(), x_valid.max()) # 0 255

# 정규화
x_train = x_train / 255.0
x_valid = x_valid / 255.0

# print(x_train.min(), x_train.max()) # 0.0 1.0
# print(x_valid.min(), x_valid.max()) # 0.0 1.0

# print(x_train.shape, x_valid.shape) # (60000, 28, 28) (10000, 28, 28)

x_train_in = x_train[..., tf.newaxis]
x_valid_in = x_valid[..., tf.newaxis]

# print(x_train_in.shape, x_valid_in.shape)   # (60000, 28, 28, 1) (10000, 28, 28, 1)

# 모델 생성
                             # 32, (3, 3) : 32개의 필터를 가지는 3 x 3 크기의 합성곱 레이어 추가
                             # relu : Relu 활성화 함수 사용
                             # input_shape = (28, 28, 1) : 독립 변수의 차원 모양(3차원), (가로, 세로, 채널)
model = tf.keras.Sequential([tf.keras.layers.Conv2D(32, (3, 3), activation = "relu", input_shape=(28, 28, 1), name = "conv"),

                             # 풀링 레이어
                                # 2 x 2 크기의 최대 풀링 레이어추가, 특성 맵 크기를 줄인다.
                             tf.keras.layers.MaxPooling2D((2, 2), name="pool"),

                             # 플래튼 레이어
                             tf.keras.layers.Flatten(),

                             # 출력 레이어
                                # 종속변수가 분류할 데이터가 0 ~ 9 이므로 10개, 다중 분류에서는 주로 softmax 활성화 함수를 사용한다.
                             tf.keras.layers.Dense(10, activation = "softmax")
                             ])

# 모델 컴파일, 옵티마이저, 손실함수, 평가지표 설정
    # 옵티마이저 : adam 옵티마이저로 설정
    # 손실함수 : 분류 모델의 오차 계산법인 엔트로피 설정
    # 평가지표 : 분류 모델의 정확도 계산법인 accuracy 설정
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics= ["accuracy"])

# 모델 훈련
    # 훈련용 데이터와 훈련용 정답
    # validation_data = 테스트용 데이터와 테스트용 정답
    # epochs : 전체 데이터셋에 대한 반복횟수
history = model.fit(x_train_in, y_train, validation_data =(x_valid_in, y_valid), epochs=10)
"""
Epoch 1/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.8882 - loss: 0.3945 - val_accuracy: 0.9716 - val_loss: 0.0921
Epoch 2/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9753 - loss: 0.0851 - val_accuracy: 0.9774 - val_loss: 0.0681
Epoch 3/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9822 - loss: 0.0613 - val_accuracy: 0.9783 - val_loss: 0.0669
Epoch 4/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9854 - loss: 0.0502 - val_accuracy: 0.9817 - val_loss: 0.0543
Epoch 5/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9868 - loss: 0.0437 - val_accuracy: 0.9795 - val_loss: 0.0637
Epoch 6/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9892 - loss: 0.0383 - val_accuracy: 0.9800 - val_loss: 0.0613
Epoch 7/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9912 - loss: 0.0276 - val_accuracy: 0.9841 - val_loss: 0.0525
Epoch 8/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9930 - loss: 0.0249 - val_accuracy: 0.9824 - val_loss: 0.0589
Epoch 9/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9937 - loss: 0.0206 - val_accuracy: 0.9837 - val_loss: 0.0550
Epoch 10/10
1875/1875 ━━━━━━━━━━━━━━━━━━━━ 6s 3ms/step - accuracy: 0.9951 - loss: 0.0171 - val_accuracy: 0.9841 - val_loss: 0.0565
"""

# 훈련된 모델의 손실, 정확도 확인하기
    # 테스트용 독립변수와 테스트용 종속변수(정답)를 평가하기
model.evaluate(x_valid_in, y_valid) # 313/313 ━━━━━━━━━━━━━━━━━━━━ 0s 1ms/step - accuracy: 0.9807 - loss: 0.0681

# 손실과 정확도 시각화
def plot_loss_acc(history, epoch):
    # 훈련 손실(오차)값, 테스트 손실(오차)값
    loss, val_loss = history.history["loss"], history.history["val_loss"]
    # 훈련 정확도, 테스트 정확도
    acc, val_acc = history.history["accuracy"], history.history["val_accuracy"]

    # 서브플롯 차트 구성
    fig, axes = plt.subplots(1, 2, figsize = (12, 4))

    # x축 훈련수, y축은 훈련 오차값
    axes[0].plot(range(1, epoch + 1), loss, label = "Training")

    # x축 훈련수, y축 테스트 오차값
    axes[0].plot(range(1, epoch + 1), val_loss, label = "Validation")

    axes[0].legend(loc = "best")
    axes[0].set_title("Loss")

    # x축 훈련수, y축 훈련 정확도
    axes[1].plot(range(1, epoch + 1), acc, label="Training")

    # x축 훈련수, y축 테스트 정확도
    axes[1].plot(range(1, epoch + 1), val_acc, label="Validation")

    axes[1].legend(loc="best")
    axes[1].set_title("Accuracy")

    plt.show()

# plot_loss_acc(history, 10)

# 훈련된 모델로 예측하기
print(y_valid[0])   # 종속 변수, 10000개 중에 첫번째 손글씨의 정답, 숫자
print(tf.argmax(model.predict(x_valid_in)[0]))  # 독립변수, 테스트용 데이터로 예측하기, 이미지된 손글씨
# tf.Tensor(7, shape=(), dtype=int64)
# argmax() : 배열 내 가장 큰 값을 가진 요소의 인덱스 반환

# print(model.summary())
"""
Model: "sequential"
┌─────────────────────────────────┬────────────────────────┬───────────────┐
│ Layer (type)                    │ Output Shape           │       Param # │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv (Conv2D)                   │ (None, 26, 26, 32)     │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ pool (MaxPooling2D)             │ (None, 13, 13, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten (Flatten)               │ (None, 5408)           │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense (Dense)                   │ (None, 10)             │        54,090 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 163,232 (637.63 KB)
 Trainable params: 54,410 (212.54 KB)
 Non-trainable params: 0 (0.00 B)
 Optimizer params: 108,822 (425.09 KB)
"""

# print("\n==========================================================\n")

# print(model.inputs)
# [<KerasTensor shape=(None, 28, 28, 1), dtype=float32, sparse=False, name=keras_tensor>]

# print("\n==========================================================\n")

# print(model.outputs)
# [<KerasTensor shape=(None, 10), dtype=float32, sparse=False, name=keras_tensor_4>]

# print("\n==========================================================\n")

# print(model.layers)
# [<Conv2D name=conv, built=True>, <MaxPooling2D name=pool, built=True>, <Flatten name=flatten, built=True>, <Dense name=dense, built=True>]

# print("\n==========================================================\n")

# print(model.layers[0])
# <Conv2D name=conv, built=True>

# print("\n==========================================================\n")

# print(model.layers[0].input)
# <KerasTensor shape=(None, 28, 28, 1), dtype=float32, sparse=False, name=keras_tensor>

# print("\n==========================================================\n")

# print(model.layers[0].output)
# <KerasTensor shape=(None, 26, 26, 32), dtype=float32, sparse=False, name=keras_tensor_1>

# print("\n==========================================================\n")

# print(model.layers[0].weights)
# [<KerasVariable shape=(3, 3, 1, 32), dtype=float32, path=sequential/conv/kernel>, <KerasVariable shape=(32,), dtype=float32, path=sequential/conv/bias>]

# print("\n==========================================================\n")

# print(model.layers[0].kernel)
# <KerasVariable shape=(3, 3, 1, 32), dtype=float32, path=sequential/conv/kernel>

# print("\n==========================================================\n")

# print(model.layers[0].bias)
# <KerasVariable shape=(32,), dtype=float32, path=sequential/conv/bias>

# print("\n==========================================================\n")

# print(model.get_layer("conv"))
# <Conv2D name=conv, built=True>

# print("\n==========================================================\n")

activator = tf.keras.Model(inputs = model.inputs, outputs = [layer.output for layer in model.layers[:2]])

activations = activator.predict(x_train_in[0][tf.newaxis, ...])

# print(len(activations)) # 2

# print("\n==========================================================\n")

conv_activation = activations[0]

# print(conv_activation.shape) # (1, 26, 26, 32)

# print("\n==========================================================\n")

fig, axes = plt.subplots(4, 8)
fig.set_size_inches(10, 5)

for i in range(32):
    axes[i // 8, i % 8].matshow(conv_activation[0, :, :, i], cmap="viridis")
    axes[i // 8, i % 8].set_title("kernel %s"%str(i), fontsize=10)
    plt.setp(axes[i // 8, i % 8].get_xticklabels(), visible = False)
    plt.setp(axes[i // 8, i % 8].get_yticklabels(), visible = False)

plt.tight_layout()
plt.show()

# print("\n==========================================================\n")

pooling_activation = activations[1]
# print(pooling_activation.shape) # (1, 13, 13, 32)

# print("\n==========================================================\n")

fig, axes = plt.subplots(4, 8)
fig.set_size_inches(10, 5)

for i in range(32):
    axes[i // 8, i % 8].matshow(pooling_activation[0, :, :, i], cmap="viridis")
    axes[i // 8, i % 8].set_title("kernel %s" % str(i), fontsize=10)
    plt.setp(axes[i // 8, i % 8].get_xticklabels(), visible=False)
    plt.setp(axes[i // 8, i % 8].get_yticklabels(), visible=False)

plt.tight_layout()
plt.show()