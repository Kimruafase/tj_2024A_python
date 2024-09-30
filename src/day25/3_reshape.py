# day25 > 3_reshape.py

import tensorflow as tf

# 1. 벡터 정의
vector = tf.constant(range(0,24))
# print(vector)   # tf.Tensor([ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23], shape=(24,), dtype=int32)

# 2. 벡터 -> 행렬 변환
mat = tf.reshape(vector, [3,8])
# print(mat)
"""
tf.Tensor(
[[ 0  1  2  3  4  5  6  7]
 [ 8  9 10 11 12 13 14 15]
 [16 17 18 19 20 21 22 23]], shape=(3, 8), dtype=int32)
"""

# mat2 = tf.reshape(vector, [6,4])

mat2 = tf.reshape(vector, [-1,4])   # -1은 어떤 값이 되어도 관계가 없다는 뜻이다.
# print(mat2)
"""
tf.Tensor(
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]
 [12 13 14 15]
 [16 17 18 19]
 [20 21 22 23]], shape=(6, 4), dtype=int32)
"""
# 3. 행렬 -> 벡터
vector1 = tf.reshape(mat2, [-1])    # 요소의 갯수를 모르기 때문에 -1
# print(vector1)  # tf.Tensor([ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23], shape=(24,), dtype=int32)

# 4. 벡터 -> 3차원 텐서
tensor = tf.reshape(vector1, [-1, 3, 4])
# print(tensor)
"""
tf.Tensor(
[[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]], shape=(2, 3, 4), dtype=int32)
"""

# 5. 3차원 텐서 -> 3차원 텐서 변환 (2, 3, 4) -> (3, 2, 4)
tensor1 = tf.reshape(tensor, [3, 2, 4])
# print(tensor1)
"""
tf.Tensor(
[[[ 0  1  2  3]
  [ 4  5  6  7]]

 [[ 8  9 10 11]
  [12 13 14 15]]

 [[16 17 18 19]
  [20 21 22 23]]], shape=(3, 2, 4), dtype=int32)
"""

# 6. 3차원 텐서 -> 4차원 텐서 변환 (3, 2, 4) -> (3, 2, 2, 2)
tensor2 = tf.reshape(tensor1, [3, 2, 2, 2])
# print(tensor2)
"""
tf.Tensor(
[[[[ 0  1]
   [ 2  3]]

  [[ 4  5]
   [ 6  7]]]


 [[[ 8  9]
   [10 11]]

  [[12 13]
   [14 15]]]


 [[[16 17]
   [18 19]]

  [[20 21]
   [22 23]]]], shape=(3, 2, 2, 2), dtype=int32)
"""