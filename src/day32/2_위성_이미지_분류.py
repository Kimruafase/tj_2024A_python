# day32 > 2_위성_이미지_분류.py
from distutils.command.build_ext import build_ext

# 1. 데이터수집
# 2. 데이터 전처리 / 데이터 분할
# 3. 모델 설계, 구축
# 4. 모델 컴파일
# 5. 모델 학습 -> 최적의 하이퍼 파라미터 찾기 -> 모델 튜닝(반복)
# 6. 모델 평가 및 예측

import tensorflow as tf
import numpy as np
import json
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
import chardet
from tensorflow.keras.applications import ResNet50V2

DATA_DTR = "c:/doit/dataset/"

(train_ds, valid_ds), info = tfds.load("eurosat/rgb",  # 데이터셋 이름
                                       split=["train[:80%]", "train[80%:]"],  # 80%의 데이터를 훈련용, 20%는 검증용
                                       shuffle_files=True,  # 파일을 무작위로 섞어 데이터를 로드 허용
                                       as_supervised=True,  # 이미지와 레이블로 구성된 튜플로 가져오기 허용
                                       with_info=True,  # 데이터셋의 메타정보(데이터셋 설명) 가져오기 허용
                                       data_dir=DATA_DTR)  # 현재 python 폴더에 하위 폴더로 "dataset" 폴더 안에 데이터셋을 다운로드

# print(train_ds)
# <_PrefetchDataset element_spec=(TensorSpec(shape=(64, 64, 3), dtype=tf.uint8, name=None), TensorSpec(shape=(), dtype=tf.int64, name=None))>
# print(valid_ds)
# <_PrefetchDataset element_spec=(TensorSpec(shape=(64, 64, 3), dtype=tf.uint8, name=None), TensorSpec(shape=(), dtype=tf.int64, name=None))>

# print(info)
'''
tfds.core.DatasetInfo(
    name='eurosat',
    full_name='eurosat/rgb/2.0.0',
    description="""
    EuroSAT dataset is based on Sentinel-2 satellite images covering 13 spectral
    bands and consisting of 10 classes with 27000 labeled and
    geo-referenced samples.

    Two datasets are offered:
    - rgb: Contains only the optical R, G, B frequency bands encoded as JPEG image.
    - all: Contains all 13 bands in the original value range (float32).

    URL: https://github.com/phelber/eurosat
    """,
    config_description="""
    Sentinel-2 RGB channels
    """,
    homepage='https://github.com/phelber/eurosat',
    data_dir='dataset/eurosat\\rgb\\2.0.0',
    file_format=tfrecord,
    download_size=89.91 MiB,
    dataset_size=89.50 MiB,
    features=FeaturesDict({
        'filename': Text(shape=(), dtype=string),
        'image': Image(shape=(64, 64, 3), dtype=uint8),
        'label': ClassLabel(shape=(), dtype=int64, num_classes=10),
    }),
    supervised_keys=('image', 'label'),
    disable_shuffling=False,
    splits={
        'train': <SplitInfo num_examples=27000, num_shards=1>,
    },
    citation="""@misc{helber2017eurosat,
        title={EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification},
        author={Patrick Helber and Benjamin Bischke and Andreas Dengel and Damian Borth},
        year={2017},
        eprint={1709.00029},
        archivePrefix={arXiv},
        primaryClass={cs.CV}
    }""",
)
'''

# show_samples() : 샘플의 이미지와 분류 label 출력해주는 함수

# 데이터 확인
# tfds.show_examples(train_ds, info)

# as_dataframe() 사용하여 샘플 출력
# tfds.as_dataframe(valid_ds.take(10), info)

# 목표 클래스의 갯수
NUM_CLASSES = info.features["label"].num_classes
# print(NUM_CLASSES)  # 10

# 숫자 label을 활용해 문자열 메타 데이터로 변환
# print(info.features["label"].int2str(6))    # PermanentCrop

# 데이터 전처리 파이프 라인 정의
# 배치란 한번에 처리하는 데이터의 묶음 단위를 의미한다.
# 데이터를 배치로 나눠서 처리하면 메모리 사용을 최적화할 수 있다.
# 모델이 전체를 한번에 처리하지 않고 데이터를 묶음(배치) 단위로 처리한다 -> 배치 처리
BATCH_SIZE = 64
# 버퍼란 임시 저장공간을 의미한다.
# 셔플할 때 버퍼에 데이터를 1000개 가져와서 임시로 저장하는 공간
# 셔플 : 일반적으로 정형화된 데이터들을 순서대로 넣으면 모델의 특정 패턴에 치우칠 수 있기 때문에 섞어줌
BUFFER_SIZE = 1000


def preprocess_data(image, label):
    image = tf.cast(image, tf.float32) / 255  # 0 ~ 1 정규화, float32 변환
    return image, label  # 튜플 구조로 return


# Java map 함수
# newArray = [3, 2, 1].map((value) -> {return value + 10;})
# newArray(13, 12, 11)

# num_parallel_calls = tf.data.AUTOTUNE : 병렬 처리(병렬 매핑)
train_data = train_ds.map(preprocess_data, num_parallel_calls=tf.data.AUTOTUNE)
valid_data = valid_ds.map(preprocess_data, num_parallel_calls=tf.data.AUTOTUNE)

# train_data 를 BUFFER_SIZE 만큼 shuffle 함, valid_data 는 shuffle 하지 않음 둘 다 autotune 적용함
train_data = train_data.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
# cache() : 캐시란 기록이며 여기에선 검증데이터셋 메모리를 캐시한다.
# 한번 호출한 검증 데이터를 메모리에 기록하여 다음에 호출 시 빠르게 접근할 수 있도록 한다.
# prefetch() : 데이터 전처리와 훈련을 병렬로 수행하여 학습 속도를 향상시킬 수 있다.
valid_data = valid_data.batch(BATCH_SIZE).cache().prefetch(tf.data.AUTOTUNE)


def build_model():
    # Sequential API를 사용하여 샘플 모델 생성
    model = tf.keras.Sequential([
        # Convolution 층
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(32, (3, 3), padding="same", activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(64, (3, 3), padding="same", activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),

        # Classifier 출력층
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CLASSES, activation="softmax")
    ])

    return model


model = build_model()

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

history = model.fit(train_data, validation_data = valid_data, epochs = 50)

# 손실 함수, 정확도 그래프 그리기
# plot_loss_acc(history, 50)

# 샘플 이미지
image_batch, label_batch = next(iter(train_data.take(1)))

image = image_batch[0]
label = label_batch[0].numpy()

plt.imshow(image)
plt.title(info.features["label"].int2str(label))


# 데이터 증강 전후를 비교하는 시각화 함수를 정의
def plot_augmentation(original, augmented):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].imshow(original)
    axes[0].set_title("Original")

    axes[1].imshow(augmented)
    axes[1].set_title("Augmented")

    plt.show()


# 좌우 뒤집기
lr_flip = tf.image.flip_left_right(image)
plot_augmentation(image, lr_flip)

# 상하 뒤집기
ud_flip = tf.image.flip_up_down(image)
plot_augmentation(image, ud_flip)

# 회전 (90도)
rotate90 = tf.image.rot90(image)
plot_augmentation(image, rotate90)

# transpose (행렬의 도치, 행과 열의 위치를 바꿈)
transpose = tf.image.transpose(image)
plot_augmentation(image, transpose)

# 이미지 자르기 1
crop1 = tf.image.central_crop(image, central_fraction=0.6)
plot_augmentation(image, crop1)

# 이미지 자르기 2
img = tf.image.resize_with_crop_or_pad(image, 64 + 20, 64 + 20)  # 사이즈 키우기
crop2 = tf.image.random_crop(img, size=[64, 64, 3])
plot_augmentation(image, crop2)

# 이미지 밝기
brightness = tf.image.adjust_brightness(image, delta=0.3)
plot_augmentation(image, brightness)

# 이미지 채도
saturation = tf.image.adjust_saturation(image, saturation_factor=0.5)
plot_augmentation(image, saturation)


# 이미지 대비
contrast = tf.image.adjust_contrast(image, contrast_factor=2)
plot_augmentation(image, contrast)

# 이미지 증강 전처리
def data_augmentation(image, label):
    image = tf.image.random_flip_left_right(image)  # 좌우 반전
    image = tf.image.random_flip_up_down(image)  # 상하 반전
    image = tf.image.random_brightness(image, max_delta=0.3)  # 밝기 변화
    image = tf.image.random_crop(image, size=[64, 64, 3])  # 크기 자르기

    image = tf.cast(image, tf.float32) / 255  # 0 ~ 1 정규화

    return image, label  # 튜플 구조로 return


train_aug = train_ds.map(data_augmentation, num_parallel_calls=tf.data.AUTOTUNE)
valid_aug = valid_ds.map(data_augmentation, num_parallel_calls=tf.data.AUTOTUNE)

train_aug = train_aug.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
valid_aug = valid_aug.batch(BATCH_SIZE).cache().prefetch(tf.data.AUTOTUNE)

# print(train_aug)
# <_PrefetchDataset element_spec=(TensorSpec(shape=(None, 64, 64, 3), dtype=tf.float32, name=None), TensorSpec(shape=(None,), dtype=tf.int64, name=None))>
# print(valid_aug)
# <_PrefetchDataset element_spec=(TensorSpec(shape=(None, 64, 64, 3), dtype=tf.float32, name=None), TensorSpec(shape=(None,), dtype=tf.int64, name=None))>

# 모델 생성
aug_model = build_model()

# 모델 컴파일
aug_model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# 모델 훈련
aug_history = aug_model.fit(train_aug, validation_data=valid_aug, epochs=50)

# 손실 함수, 정학도 그래프 그리기
# plot_loss_acc(aug_history, 50)

# pre_trained 모델을 사전 학습된 가중치와 함께 가져오기
pre_trained_base = ResNet50V2(include_top= False, weights= "imagenet", input_shape=[64, 64, 3])

# 사전 학습된 가중치를 업데이트되지 않도록 설정
pre_trained_base.trainable = False

# Top 층에 Classifier 추가
def build_trainsfer_classifier():
    model = tf.keras.Sequential([
        # pre_trained Base
        pre_trained_base,

        # Classifier 출력층
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CLASSES, activation="softmax")
    ])

    return model

# 모델 구조
tc_model = build_trainsfer_classifier()
tc_model.summary()
"""
Model: "sequential_2"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 resnet50v2 (Functional)     (None, 2, 2, 2048)        23564800  
                                                                 
 flatten_2 (Flatten)         (None, 8192)              0         
                                                                 
 dense_6 (Dense)             (None, 128)               1048704   
                                                                 
 dropout_4 (Dropout)         (None, 128)               0         
                                                                 
 dense_7 (Dense)             (None, 64)                8256      
                                                                 
 dropout_5 (Dropout)         (None, 64)                0         
                                                                 
 dense_8 (Dense)             (None, 10)                650       
                                                                 
=================================================================
Total params: 24,622,410
Trainable params: 1,057,610
Non-trainable params: 23,564,800
_________________________________________________________________
"""

# 모델 컴파일
tc_model.compile(optimizer="adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])

# 모델 훈련
tc_history = tc_model.fit(train_aug, validation_data=valid_aug, epochs= 50)

# 손실함수, 정확도 그리기
# plot_loss_acc(tc_history, 50)