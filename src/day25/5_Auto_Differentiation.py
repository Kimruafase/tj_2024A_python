# day25 > 5_Auto_Differentiation

"""
    > 함수(function)
        > 수학 : 어떤 집합의 각 원소를 다른 어떤 집합의 유일한 원소에 대응시키는 이항 관계
        > 프로그래밍 : 어떠한 코드 집합에 매개변수를 대입하고 결과 변수를 받는 구조
"""

import tensorflow as tf

# 1. 선형 관계를 갖는 데이터 샘플
    # 텐서플로의 랜덤 숫자 생성 객체 선언, 시드값은 아무거나, 시드란? 랜덤 생성할 때 사용되는 제어 정수값
g = tf.random.Generator.from_seed(2020)
    # 랜덤 숫자 생성 객체를 이용한 정규분포 난수를 10개 생성해서 벡터(리스트) X에 저장한다.
    # .normal(shape = (축1, )), .normal(shape = (축1, 축2)), .normal(shape = (축1, 축2, 축3))
X = g.normal(shape = (10,))
Y = (3 * X) - 2
# print(X.numpy())    # 독립
"""
[-0.20943771  1.2746525   1.213214   -0.17576952  1.876984  
  0.16379918 1.082245    0.6199966  -0.44402212  1.3048344 ]
"""
# print(Y.numpy())    # 종속
"""
[-2.628313    1.8239574   1.6396422  -2.5273085   3.630952   
 -1.5086024  1.2467351  -0.14001012 -3.3320663   1.9145031 ]
"""

# 3. Loss 함수 정의 # 손실 함수 : 평균 제곱 오차를 정의하는 함수
def cal_mse(X, Y, a, b):
    Y_pred =(a * X)+ b # Y값 - 종속(예측) = 계수(기울기)a * X(피처) + 상수항(Y절편)
    squared_error = (Y_pred - Y) ** 2   # 예측 Y와 실제 Y 간의 차이의 제곱 : 오차제곱
    mse = tf.reduce_mean(squared_error)
    print(mse)
    return mse

# 4. 자동 미분 과정을 기록

a = tf.Variable(0.0) # 계수, 텐서플로 변수에 0으로 초기화
b = tf.Variable(0.0) # Y절편, 텐서플로 변수에 0으로 초기화
# 목적 : a 와 b 를 미세하게 변경하면서 반복적으로 계산하여 손실을 최소화하는 값을 찾는다.

EPOCHS = 200 # 계산 횟수, 반복 횟수

for epoch in range(1, EPOCHS + 1):  # 1 ~ 200까지 200회 반복
    # 200번 반복하는 목적 : a와 b를 미세하게 변경하면서 손실이 가장 적은 값을 찾기

    # 4 - 1. mse 계산 기록, tf.GradientTape() as 변수명: with 안에 있는 계산식들을 모두 기록하는 역할
    with tf.GradientTape() as tape:
        mse = cal_mse(X, Y, a, b)   # 위에서 정의한 손실함수를 계산한다.

    # 4 - 2. 기울기 계산, tape.gradient() 를 이용하여 mse 에 대한 a와 b의 미분값(기울기)을 구한다.
    grad = tape.gradient(mse, {"a" : a, "b" : b})   # mse 에 대한 a 와 b를 딕셔너리를 통해 반환
    d_a = grad["a"]
    d_b = grad["b"]

    # 4 - 3. .assign_sub(), 텐서플로 변수에 매개변수를 원본값에서 뺀 값으로 변수값을 수정하는 함수
    a.assign_sub(d_a * 0.05)    # 현재 값의 5% 감소 # a -= d_a * 0.05
    b.assign_sub(d_b * 0.05)    # 0.05% 감소

    if epoch % 20 == 0:
        print(f"epoch : {epoch}, mse : {mse:.4f}, a : {a.numpy():.2f}, b : {b.numpy():.2f}")

