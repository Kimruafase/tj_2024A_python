# day33 > 1_객체_탐지.py

import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow_hub as tfhub

# 1. 샘플 이미지
img_path = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Gangnam_Seoul_January_2009.jpg/1280px-Gangnam_Seoul_January_2009.jpg"

    # 1) 지정한 경로의 이미지를 파일 객체로 가져오기
img = tf.keras.utils.get_file(fname="gangnam", origin=img_path)
# print(img)  # C:\Users\tj-bu-703-17\.keras\datasets\gangnam

    # 2) 파일 객체를 String 으로 변환
img = tf.io.read_file(img)
# print(img)

    # 3) 문자(string)를 숫자(uint8) 텐서로 변환
img = tf.image.decode_jpeg(img, channels=3)
# print(img)
"""
tf.Tensor(
[[[  5   5   5]
  [  3   3   3]
  [  1   1   1]
  ...
  [ 91  98 114]
  [ 76  93 103]
  [ 76  99 105]]

 [[  4   4   4]
  [  3   3   3]
  [  2   2   2]
  ...
  [ 90  97 113]
  [ 76  94 104]
  [ 78 103 108]]

 [[  4   4   4]
  [  3   3   3]
  [  2   2   2]
  ...
  [ 90 102 116]
  [ 71  91 100]
  [ 74 102 106]]

 ...

 [[  4   4   4]
  [  3   3   3]
  [  2   2   0]
  ...
  [ 39  34  38]
  [ 40  36  37]
  [ 40  36  37]]

 [[  1   2   4]
  [  0   1   0]
  [  0   2   0]
  ...
  [ 38  32  36]
  [ 36  30  32]
  [ 36  30  32]]

 [[  0   1   2]
  [  0   1   0]
  [  0   1   0]
  ...
  [ 38  29  34]
  [ 33  24  27]
  [ 35  26  29]]], shape=(700, 1280, 3), dtype=uint8)
"""

    # 4) 0 ~ 1 범위로 정규화
img = tf.image.convert_image_dtype(img, tf.float32)
# print(img)
"""
tf.Tensor(
[[[0.01960784 0.01960784 0.01960784]
  [0.01176471 0.01176471 0.01176471]
  [0.00392157 0.00392157 0.00392157]
  ...
  [0.35686275 0.38431376 0.44705886]
  [0.29803923 0.3647059  0.4039216 ]
  [0.29803923 0.38823533 0.41176474]]

 [[0.01568628 0.01568628 0.01568628]
  [0.01176471 0.01176471 0.01176471]
  [0.00784314 0.00784314 0.00784314]
  ...
  [0.3529412  0.3803922  0.4431373 ]
  [0.29803923 0.36862746 0.40784317]
  [0.30588236 0.4039216  0.42352945]]

 [[0.01568628 0.01568628 0.01568628]
  [0.01176471 0.01176471 0.01176471]
  [0.00784314 0.00784314 0.00784314]
  ...
  [0.3529412  0.40000004 0.454902  ]
  [0.2784314  0.35686275 0.3921569 ]
  [0.2901961  0.40000004 0.4156863 ]]

 ...

 [[0.01568628 0.01568628 0.01568628]
  [0.01176471 0.01176471 0.01176471]
  [0.00784314 0.00784314 0.        ]
  ...
  [0.15294118 0.13333334 0.14901961]
  [0.15686275 0.14117648 0.14509805]
  [0.15686275 0.14117648 0.14509805]]

 [[0.00392157 0.00784314 0.01568628]
  [0.         0.00392157 0.        ]
  [0.         0.00784314 0.        ]
  ...
  [0.14901961 0.1254902  0.14117648]
  [0.14117648 0.11764707 0.1254902 ]
  [0.14117648 0.11764707 0.1254902 ]]

 [[0.         0.00392157 0.00784314]
  [0.         0.00392157 0.        ]
  [0.         0.00392157 0.        ]
  ...
  [0.14901961 0.1137255  0.13333334]
  [0.12941177 0.09411766 0.10588236]
  [0.13725491 0.10196079 0.1137255 ]]], shape=(700, 1280, 3), dtype=float32)
"""

    # 5) 시각화
# plt.imshow(img)
# plt.show()

    # 6) 차원 추가
# print(img.shape)    # (700, 1280, 3)
img_input = tf.expand_dims(img, 0)  # 0번 인덱스(가장 앞에) 차원 추가
# print(img_input.shape)  # (1, 700, 1280, 3)

    # 7) 지정한 URL 이용한 모델 load 하기
model = tfhub.load("https://www.kaggle.com/models/google/faster-rcnn-inception-resnet-v2/tensorFlow1/faster-rcnn-openimages-v4-inception-resnet-v2/1?tfhub-redirect=true")
# print(model.signatures.keys())
"""
KeysView(_SignatureMap({'default': <ConcreteFunction () -> Dict[['detection_scores', TensorSpec(shape=(None, 1), dtype=tf.float32, name=None)], 
['detection_class_names', TensorSpec(shape=(None, 1), dtype=tf.string, name=None)], ['detection_class_entities', TensorSpec(shape=(None, 1), dtype=tf.string, name=None)], 
['detection_boxes', TensorSpec(shape=(None, 4), dtype=tf.float32, name=None)], ['detection_class_labels', TensorSpec(shape=(None, 1), dtype=tf.int64, name=None)]] at 0x24ABF68B290>}))
"""
obj_detector = model.signatures["default"]
# print(obj_detector)
"""
ConcreteFunction Input Parameters:
Output Type:
  Dict[['detection_scores', TensorSpec(shape=(None, 1), dtype=tf.float32, name=None)], ['detection_class_names', TensorSpec(shape=(None, 1), dtype=tf.string, name=None)], 
  ['detection_class_entities', TensorSpec(shape=(None, 1), dtype=tf.string, name=None)], ['detection_boxes', TensorSpec(shape=(None, 4), dtype=tf.float32, name=None)], 
  ['detection_class_labels', TensorSpec(shape=(None, 1), dtype=tf.int64, name=None)]]
Captures:
"""

    # 8) load 한 모델로 예측하기
result = obj_detector(img_input)
# print(result.keys())    # 경계박스 좌표, 예측한 or 검증된 클래스 (정답 / 종속) 아이디, 예측 or 검증된 확률 or 스코어
# dict_keys(['detection_scores', 'detection_class_names', 'detection_class_entities', 'detection_boxes', 'detection_class_labels'])
# print(len(result["detection_scores"]))  # 100

    # 9) 모델이 예측한 결과를 시각화
boxes = result["detection_boxes"]   # Bounding Box 좌표 예측값
labels = result["detection_class_entities"] # 분류 예측값
scores = result["detection_scores"] # 신뢰도(confidence)

    # 샘플 이미지 가로 세로 크기 설정
img_height, img_width = img.shape[0], img.shape[1]

    # 탐지할 최대 객체의 수
obj_to_detect = 10

    # 시각화
plt.figure(figsize=(15, 10))
for i in range(min(obj_to_detect, boxes.shape[0])):
    if scores[i] >= 0.2:    # 예측 신뢰도가 0.2 (20%) 이상인 것만 시각화
        # ymax : 상단 좌표, xmin : 좌측 좌표, ymin : 하단 좌표, xmax : 우측 좌표
        (ymax, xmin, ymin, xmax) = (boxes[i][0] * img_height, boxes[i][1] * img_width,
                                    boxes[i][2] * img_height, boxes[i][3] * img_width)
        plt.imshow(img)
        # 예측한 경계 상자 그리기
            # (xmin, ymin) : 좌측 하단, (xmax, ymin) : 우측 하단, (xmax, ymax) : 우측 상단, (xmin, ymax) : 좌측 상단
            # 연결 경계선을 yellow, 두께를 2로 설정
        plt.plot([xmin, xmax, xmax, xmin, xmin], [ymin, ymin, ymax, ymax, ymin], color = "yellow", linewidth = 2)

        class_name = labels[i].numpy().decode("utf-8")
        infer_score = int(scores[i].numpy() * 100)
        annotation = f"{class_name} : {infer_score}%"
        plt.text(xmin + 10, ymax + 20, annotation, color = "white", backgroundcolor = "blue", fontsize = 10)

plt.show()