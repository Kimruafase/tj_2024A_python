# day25 > 1_Tensor_Flow.py

"""
> [텐서플로]
    > 1. 구글이 개발한 오픈소스 딥러닝 프레임워크
    > 2. 머신러닝, 딥러닝 모델을 만들고 훈련하는데 사용된다.
    > 3. 특히 신경망을 기반으로한 모델을 구축하고 학습 시키는데 사용된다.
    > 4. 케라스라는 고수준 API를 제공하고 보다 간단한 모델을 정의하고 훈련시킬 수 있다.
    > 5. 그 외 이미지 처리, 자연어 처리, 음성 인식 등의 다양한 곳에서 활용된다.

> [텐서]
    > 1. 텐서플로에서 다루는 기본 데이터 구조
    > 2. 다차원 배열 / 리스트를 생각할 수 있고, 여러 차원으로 표현이 가능
    > 3. 텐서(데이터 구조) 플로(흐름) : 데이터를 처리하고 학습시키는 과정을 나타낸다.
    > 4. 종류
        > 1) 스칼라 -> 0차원 텐서, 상수, 랭크 0, 0차수, 방향이 없다.
            > ex_ 단일 숫자 : 5
        > 2) 벡터 -> 1차원 텐서, 1차원 리스트, 랭크 1, 1차수, X or Y 한 방향, (행 또는 열)
            > ex_ [5, 10, 15]
        > 3) 행렬 -> 2차원 텐서, 2차원 리스트, 랭크 2, 2차수, X and Y 두 방향, (행, 열)
            > 행(row)와 열(column) ex_ [[5, 10], [15, 20]]
        > 4) 고차원 텐서
            > 3차원 텐서, 3차원 리스트, 랭크 3, 3차수, X and Y, Z 세 방향, (행, 열, 높이)
            > 4차원 텐서, 4차원 리스트, 랭크 4, 4차수, X and Y and Z, W 네 방향, (축1, 축2, 축3, 축4)
"""

import tensorflow as tf

# [1] 스칼라
a = tf.constant(5)
# print(a)                    # tf.Tensor(5, shape=(), dtype=int32)
# print(tf.rank(a))           # tf.Tensor(0, shape=(), dtype=int32)
# print(a.numpy())            # 5
# print(tf.rank(a).numpy())   # 0

# [2] 벡터
a1 = tf.constant([5, 10, 15])
# print(a1)                    # tf.Tensor([ 5 10 15], shape=(3,), dtype=int32)
# print(tf.rank(a1))           # tf.Tensor(1, shape=(), dtype=int32)
# print(a1.numpy())            # [ 5 10 15]
# print(tf.rank(a1).numpy())   # 1

# [3] 행렬
a2 = tf.constant([[5, 10], [15, 20]])
# print(a2)
"""
tf.Tensor(
[[ 5 10]
[15 20]], shape=(2, 2), dtype=int32)
"""
# print(tf.rank(a2))           # tf.Tensor(2, shape=(), dtype=int32)
# print(a2.numpy())
"""
[[ 5 10]
 [15 20]]
"""
# print(tf.rank(a2).numpy())   # 2

# [4] 고차원 텐서
# 1. 3차원 텐서
    # 1) 2차원 리스트(행렬) 만들기
mat1 = [[1, 2, 3, 4], [5, 6, 7, 8]] # 2차원 리스트
mat2 = [[9, 10, 11, 12], [13, 14, 15, 16]] # 행 2, 열 4
mat3 = [[17, 18, 19, 20], [21, 22, 23, 24]] # (2, 4)

    # 2) 같은 축 방향으로 2차원 리스트 나열하기 -> 3차원 텐서
tensor1 = tf.constant([mat1, mat2, mat3])   # 3개의 리스트를 하나의 리스트로 감싼다.

    # 3) 텐서 확인, 랭크 확인
# print(tensor1)
"""
tf.Tensor(
[[[ 1  2  3  4]
  [ 5  6  7  8]]

 [[ 9 10 11 12]
  [13 14 15 16]]

 [[17 18 19 20]
  [21 22 23 24]]], shape=(3, 2, 4), dtype=int32)
"""
# print(tf.rank(tensor1))         # tf.Tensor(3, shape=(), dtype=int32)
# print(tensor1.numpy())
"""
[[[ 1  2  3  4]
  [ 5  6  7  8]]

 [[ 9 10 11 12]
  [13 14 15 16]]

 [[17 18 19 20]
  [21 22 23 24]]]
"""
# print(tf.rank(tensor1).numpy()) # 3

    # 4) 다른 방법으로 만들기
tensor2 = tf.stack([mat1, mat2, mat3])
# print(tensor2)
"""
tf.Tensor(
[[[ 1  2  3  4]
  [ 5  6  7  8]]

 [[ 9 10 11 12]
  [13 14 15 16]]

 [[17 18 19 20]
  [21 22 23 24]]], shape=(3, 2, 4), dtype=int32)
"""
# print(tf.rank(tensor2))         # tf.Tensor(3, shape=(), dtype=int32)

    # 5) 벡터로 3차원 만들기
vec1 = [1, 2, 3, 4]
vec2 = [5, 6, 7, 8]
vec3 = [9, 10, 11, 12]
vec4 = [13, 14, 15, 16]
vec5 = [17, 18, 19, 20]
vec6 = [21, 22, 23, 24]
    # [[], [], []] -> 행렬 3개 (2, 4) -> 고차원 텐서 1개 (3, 2, 4)
tensor3 = tf.constant([[vec1, vec2], [vec3, vec4], [vec5, vec6]])
# print(tensor3)
"""
tf.Tensor(
[[[ 1  2  3  4]
  [ 5  6  7  8]]

 [[ 9 10 11 12]
  [13 14 15 16]]

 [[17 18 19 20]
  [21 22 23 24]]], shape=(3, 2, 4), dtype=int32)
"""
# print(tf.rank(tensor3))         # tf.Tensor(3, shape=(), dtype=int32)

    # 6) 4차원 텐서 만들기 -> [3차원 리스트, 3차원 리스트] -> [2, 3, 2, 4]
tensor4 = tf.stack([tensor1, tensor2])
print(tensor4)
"""
tf.Tensor(
[[[[ 1  2  3  4]
   [ 5  6  7  8]]

  [[ 9 10 11 12]
   [13 14 15 16]]

  [[17 18 19 20]
   [21 22 23 24]]]


 [[[ 1  2  3  4]
   [ 5  6  7  8]]

  [[ 9 10 11 12]
   [13 14 15 16]]

  [[17 18 19 20]
   [21 22 23 24]]]], shape=(2, 3, 2, 4), dtype=int32)
"""
print(tf.rank(tensor4)) # tf.Tensor(4, shape=(), dtype=int32)

"""
# 벡터
array1 = [] # 벡터, 1차원 리스트
array2 = []
array3 = []
array4 = []

# 행렬
array5 = [array1, array2] # 행렬, 2차원 리스트
array6 = [array3, array4]

# 고차원 텐서
array7 = [array5, array6] # 고차원 텐서, 3차원 리스트

"""