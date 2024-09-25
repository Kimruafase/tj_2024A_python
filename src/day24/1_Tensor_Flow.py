# day25 > 1_Tensor_Flow.py

# 텐서플로 : 텐서(다차원 데이터)를 플로(흐름)에 따라 연산하는 과정을 제공하는 라이브러리

# tensorflow 설치

# [1] 모듈 호출
import tensorflow as tf
import numpy as np

# [2] 즉시 실행모드 확인
# print(tf)                       # <module 'tensorflow' from 'C:\\Users\\tj-bu-703-17\\Desktop\\tj_2024A_python\\.venv\\Lib\\site-packages\\tensorflow\\__init__.py'>
# print(tf.executing_eagerly())   # True

# [3] tensorflow 연산

a = 1
b = 2
c = tf.math.add(a, b)
# print(type(c))              # <class 'tensorflow.python.framework.ops.EagerTensor'>
# print(tf.math.add(a, b))    # tf.Tensor(3, shape=(), dtype=int32)
# print(tf.math)              # <module 'tensorflow._api.v2.math' from 'C:\\Users\\tj-bu-703-17\\Desktop\\tj_2024A_python\\.venv\\Lib\\site-packages\\tensorflow\\_api\\v2\\math\\__init__.py'>

# [4] 결과값만 꺼내기
# print(c.numpy())            # 3

# [5] 탠서(상수 : 스칼라)        # .constant(), tf.tensor(값, shape=(배열 크기), type=타입)
    # 1. 스칼라 정의
a1 = tf.constant(1)
b1 = tf.constant(2)
# print(a1)                   # tf.Tensor(1, shape=(), dtype=int32)
# print(b1)                   # tf.Tensor(2, shape=(), dtype=int32)

    # 2. 랭크 확인              # .rank()
# print(tf.rank(a1))          # tf.Tensor(0, shape=(), dtype=int32)

    # 3. 스칼라 데이터 타입 변환, .cast(스칼라 객체, tf.타입)
a1 = tf.cast(a1, tf.float32)
b1 = tf.cast(b1, tf.float32)
# print(a1)                   # tf.Tensor(1.0, shape=(), dtype=float32)
# print(b1)                   # tf.Tensor(2.0, shape=(), dtype=float32)

    # 4. 수학적 함수 -> .math
c1 = tf.math.add(a, b)
# print(c1)                   # tf.Tensor(3, shape=(), dtype=int32)
# print(tf.rank(c1))          # tf.Tensor(3, shape=(), dtype=int32)
# print(tf.math.subtract(a, b))   # tf.Tensor(-1, shape=(), dtype=int32)
# print(tf.math.multiply(a, b))   # tf.Tensor(2, shape=(), dtype=int32)
# print(tf.math.divide(a, b))     # tf.Tensor(0.5, shape=(), dtype=float64)
# print(tf.math.mod(a, b))        # tf.Tensor(1, shape=(), dtype=int32)
# print(tf.math.floordiv(a, b))   # tf.Tensor(0, shape=(), dtype=int32)
# print(a + b)                    # 3
# print(a - b)                    # -1
# print(a * b)                    # 2
# print(a / b)                    # 0.5
# print(a % b)                    # 1
# print(a // b)                   # 0


# [6] 탠서 (1차원 배열 : 벡터)        # tf.tensor( , shape=(원소 갯수, ), dtype = 타입)
    # 벡터 선언
vec1 = tf.constant([10., 20., 30.])  # 파이썬 리스트 형식으로 선언
vec2 = tf.constant(np.array([10., 20., 30.]))
# print(vec1)                     # tf.Tensor([10 20 30], shape=(3,), dtype=int32)
# print(vec2)                     # tf.Tensor([10 20 30], shape=(3,), dtype=int32)

    # 랭크 확인
# print(tf.rank(vec1))            # tf.Tensor(1, shape=(), dtype=int32)
# print(tf.rank(vec2))            # tf.Tensor(1, shape=(), dtype=int32)

    # 벡터 연산
# print(vec1 + vec2)                  # tf.Tensor([20 40 60], shape=(3,), dtype=int32)
# print([10, 20, 30] + [10, 20, 30])  # [10, 20, 30, 10, 20, 30]
# print(vec1 - vec2)                  # tf.Tensor([0 0 0], shape=(3,), dtype=int32)
# print(vec1 * vec2)                  # tf.Tensor([100 400 900], shape=(3,), dtype=int32)
# print(vec1 / vec2)                  # tf.Tensor([1. 1. 1.], shape=(3,), dtype=float64)
# print(vec1 % vec2)                  # tf.Tensor([0 0 0], shape=(3,), dtype=int32)
# print(vec1 // vec2)                 # tf.Tensor([1 1 1], shape=(3,), dtype=int32)

    # 벡터 내 요소 총합계
# print(tf.reduce_sum(vec1))          # tf.Tensor(60, shape=(), dtype=int32)
# print(tf.reduce_sum(vec2))          # tf.Tensor(60, shape=(), dtype=int32)

    # 거듭제곱
# print(vec1**2)                      # tf.Tensor([100 400 900], shape=(3,), dtype=int32)
# print(vec2**2)                      # tf.Tensor([100 400 900], shape=(3,), dtype=int32)

    # 제곱근
# print(vec1**0.5)                    # tf.Tensor([3.1622777 4.472136  5.477226 ], shape=(3,), dtype=float32)

    # 브로드캐스팅 연산
# print(vec1 + 1)                     # tf.Tensor([11. 21. 31.], shape=(3,), dtype=float32)

# [7] 탠서 객체 (2차원 리스트 : 행렬)      # tf.tensor([[10 20] [30 40]], shape=(행 갯수, 열 갯수), dtype=타입)
    # 행렬 선언
mat1 = tf.constant([[10, 20], [30, 40]])    # 전체를 감싼 대괄호 내 원소 갯수 : 행 갯수, 벡터 갯수 / 내부 대괄호 내 원소 갯수 : 열 갯수, 스칼라 갯수
# print(mat1)
"""
tf.Tensor(
[[10 20]
 [30 40]], shape=(2, 2), dtype=int32)
"""

    # 랭크 확인
# print(tf.rank(mat1))                # tf.Tensor(2, shape=(), dtype=int32)
mat2 = tf.stack([[1, 1], [-2, 1]])
# print(mat2)
"""
tf.Tensor(
[[ 1  0]
 [-2  1]], shape=(2, 2), dtype=int32)
"""
# print(tf.rank(mat2))                # tf.Tensor(2, shape=(), dtype=int32)

    # 행렬 연산
# print(mat1 * mat2)
"""
tf.Tensor(
[[ 10   0]
 [-60  40]], shape=(2, 2), dtype=int32)
"""
# print(mat1 + mat2)
"""
tf.Tensor(
[[11 20]
 [28 41]], shape=(2, 2), dtype=int32)
"""
# print(mat1 - mat2)
"""
tf.Tensor(
[[ 9 20]
 [32 39]], shape=(2, 2), dtype=int32)
"""
# print(mat1 / mat2)
"""
tf.Tensor(
[[ 10.  inf]
 [-15.  40.]], shape=(2, 2), dtype=float64)
"""
# print(mat1 % mat2)    # 오류
# print(tf.math.mod(mat1, mat2))
"""
tf.Tensor(
[[0 0]
 [0 0]], shape=(2, 2), dtype=int32)
"""
# print(mat1 // mat2)
"""
tf.Tensor(
[[ 10  20]
 [-15  40]], shape=(2, 2), dtype=int32)
"""
# print(tf.math.multiply(mat1, 3))
"""
tf.Tensor(
[[ 30  60]
 [ 90 120]], shape=(2, 2), dtype=int32)
"""

    # 행렬곱 연산
"""
A = [[a1, a2], 
    [a3, a4]] 
B = [[b1, b2], 
    [b3, b4]]
AB = [[(a1*b1 + a2*b3), (a1*b2 + a2*b4)], 
      [(a3*b1 + a4*b3), (a3*b2 + a4*b4)] 
"""
# print(tf.matmul(mat1, mat2))
"""
tf.Tensor(
[[-30  20]
 [-50  40]], shape=(2, 2), dtype=int32)
"""

"""
> 인공지능 (AI)
    > 빅데이터 : 많은 자료들               
    > 머신러닝 : 자료들의 학습 모델         (scikit-learn)
    > 딥러닝   : 복잡한 자료들의 학습 모델   (TensorFlow)
    
        > 텐서플로 자료구조
            > 스칼라           벡터          매트릭스            탠서
            rank - 0       rank - 1       rank - 2         rank - 3
              상수            리스트       2차원 리스트       3차원 리스트
            차수 - 0        차수 - 1        차수 - 2          차수 - 3
            방향 없음        방향 : x      방향 : x, y      방향 : x, y, z
"""