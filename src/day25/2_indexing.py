import tensorflow as tf


"""
> 인덱싱
    > 원소가 저장된 순서 번호
    > 0번부터 시작하고 마지막 인덱스는 -1
> 슬라이싱
    > [시작 : 끝(미만)]
"""


# 1. 벡터
vec = tf.constant([10, 20, 30, 40, 50])
# print(vec)              # tf.Tensor([10 20 30 40 50], shape=(5,), dtype=int32)
# print(vec[0])           # tf.Tensor(10, shape=(), dtype=int32)
# print(vec[0].numpy())   # 10
# print(vec[-1])          # tf.Tensor(50, shape=(), dtype=int32)
# print(vec[0 : 3])       # tf.Tensor([10 20 30], shape=(3,), dtype=int32)

# 2. 행렬
mat = tf.constant([[10, 20, 30], [40, 50, 60]])
# print(mat[0, 2])    # [행 인덱스, 열 인덱스], tf.Tensor(30, shape=(), dtype=int32)
# print(mat[0, :])    # [행(슬라이싱), 열(슬라이싱)], [첫번째행 0, 전체 열 :], tf.Tensor([10 20 30], shape=(3,), dtype=int32)
# print(mat[:, 1])    # [전체 행 :, 두번째 열 1], tf.Tensor([20 50], shape=(2,), dtype=int32)
# print(mat[:, :])
"""
tf.Tensor(
[[10 20 30]
 [40 50 60]], shape=(2, 3), dtype=int32)
"""

# 3. 3차원 텐서
tensor = tf.constant([[[10, 20, 30], [40, 50, 60]], [[-10, -20, -30], [-40, -50, -60]]])
# print(tensor)
"""
tf.Tensor(
[[[ 10  20  30]
  [ 40  50  60]]

 [[-10 -20 -30]
  [-40 -50 -60]]], shape=(2, 2, 3), dtype=int32)
"""
# print(tensor[0, :, :])  # 축1에서 첫번째 인덱스의 축2에서 전체, 축3에서 전체 인덱스 호출
"""
tf.Tensor(
[[10 20 30]
 [40 50 60]], shape=(2, 3), dtype=int32)
"""
# print(tensor[:, : 2, : 2])  # 축1 전체, 축2 (0 ~ 1), 축3 (0 ~ 1) -> (2, 2, 2)
"""
tf.Tensor(
[[[ 10  20]
  [ 40  50]]

 [[-10 -20]
  [-40 -50]]], shape=(2, 2, 2), dtype=int32)
"""

# 연습
    # 1. 벡터
vec1 = tf.constant([10, 20, 30, 40, 50])

# 1) 첫번째 스칼라 출력
# print(vec1[0].numpy())  # 10

# 2) 뒤에서 2번째 스칼라 출력
# print(vec1[-2].numpy()) # 40

# 3) 앞에서 3개 요소 슬라이싱
# print(vec[0 : 3])   # tf.Tensor([10 20 30], shape=(3,), dtype=int32)

# 4) 뒤에서 4개 요소 슬라이싱
# print(vec[-4 : ]) # tf.Tensor([20 30 40 50], shape=(4,), dtype=int32)

    # 2. 행렬
mat1 = tf.constant([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 1) 첫번째 행, 두번째 열 요소 인덱싱
# print(mat1[0,1])    # tf.Tensor(2, shape=(), dtype=int32)

# 2) 세번째 행, 첫번째 열 요소 인덱싱
# print(mat1[2,0])    # tf.Tensor(7, shape=(), dtype=int32)

# 3) 첫번째 행 전체 슬라이싱
# print(mat1[0, :])   # tf.Tensor([1 2 3], shape=(3,), dtype=int32)

# 4) 두번째 열 전체 슬라이싱
# print(mat1[: , 1])  # tf.Tensor([2 5 8], shape=(3,), dtype=int32)

    # 3. 3차원 텐서
tensor1 = tf.constant([ [[1, 2], [3, 4]], [[5, 6], [7, 8]]])

# 1) 가장 첫번째에 있는 요소 인덱싱
# print(tensor1[0,0,0])   # tf.Tensor(1, shape=(), dtype=int32)

# 2) 가장 마지막에 있는 요소 인덱싱
# print(tensor1[-1,-1,-1])   # tf.Tensor(8, shape=(), dtype=int32)

# 3) 첫번째 행렬 슬라이싱
# print(tensor1[0,:,:])
"""
tf.Tensor(
[[1 2]
 [3 4]], shape=(2, 2), dtype=int32)
"""

# 4) 두번째 행렬의 첫번째 행 슬라이싱
# print(tensor1[1,0,:])   # tf.Tensor([5 6], shape=(2,), dtype=int32)