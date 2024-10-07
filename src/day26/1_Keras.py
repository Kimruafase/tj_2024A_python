# day26 > 1_Keras.py

import numpy as np
import matplotlib.pyplot as plt

# [1]
def make_linear(w, b, size, noise):
    x = np.random.rand(size)    # 0 ~ 1 사이의 size 만큼의 난수로 이루어진 x 배열 선언
    # print(x)
    y = (w * x) + b
    # print(y)

    # 음수 noise부터 양수 noise 사이의 난수 생성, 갯수는 y 갯수만큼, 크기는 y 크기만큼
    # 실제 y 값의 노이즈(작은 변화)를 주고 확인하는 예제
    noise = np.random.uniform(-abs(noise), abs(noise), size = y.shape)
    # print(noise)

    yy = y + noise

    # 시각화
    plt.plot(x, y, c = "r")
    plt.scatter(x, yy)
    plt.title("y = 0.3 * x + 0.5")
    plt.show()

    return x, yy

x, y = make_linear(0.3, 0.5, 100, 0.01)

# [2] w(기울기)와 b(y절편)를 학습률을 업데이트하여 손실(오차)를 최소화하는 방법을 찾는 예제
num_epoch = 1000 # 1. 학습 횟수를 최대 1000번

learning_rate = 0.005 # 2. 업데이트 크기, 학습률

# 3. 에러 기록, 손실(오차)를 기록할 리스트
errors = []

# 4.
w = np.random.uniform(low=0.0, high = 1.0)  # w(기울기)를 0 ~ 1 사이의 랜덤값으로 초기화
print(w)

b = np.random.uniform(low = 0.0, high = 1.0) # b(y절편)를 0 ~ 1 사이의 랜덤값으로 초기화
print(b)

for epoch in range(num_epoch):  # 최대 epoch 수만큼 반복문 실행

    y_hat = (w * x) + b # y 에 대한 예측값, 주어진 x에 따른 최적의 오차를 찾는 w와 b를 찾기

    # 오차 계산식, 평균 제곱 오차 계산식
        # 예측값과 실제값(노이즈된 y값) 차이를 제곱하여 평균한 값
    error = 0.5 * ((y_hat - y) ** 2).sum()

    # 만약에 오차라 0.005 미만이면 반복문 종료
    if error < 0.005:
        break

    # 기울기 미분 계산
        # 1. 기울기 업데이트
    w = w - learning_rate * ((y_hat - y) * x).sum()

        # 2. y절편 업데이트
    b = b - learning_rate * (y_hat - y).sum()

    # 손실(오차) 기록
    errors.append(error)

    if epoch % 5 == 0:
        print(f"{epoch}, w = {w:.5f}, b = {b:.5f}, error = {error:.5f}")


print(f"---------------------------------------------------------------")
print(f"{epoch}, w = {w:.1f}, b = {b:.1f}, error = {error:.5f}")

plt.plot(errors)
plt.xlabel("Epoch")
plt.ylabel("Error")
plt.show()