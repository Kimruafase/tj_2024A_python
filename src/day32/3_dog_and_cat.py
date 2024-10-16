# day32 > 3_dog_and_cat.py
import os
import zipfile
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

# 실뭄에서는 데이터셋을 웹에서 로드하는 경우가 거의 없다.
# 직접 이미지를 로드하는 경우가 더 많다.
# 강의 카톡방에 cat-and-dog.zip 다운로드받아 현재 day32 폴더에 넣기

# 1. 데이터 준비(교재와 다르게 구글드라이브가 아닌 로컬PC에서 준비)
    # 데이터 경로 위치
source_file = "cat-and-dog.zip"
extract_folder = "c:/doit/dataset"

    # (파이썬 코드로) 압축 해제
    # zipfile.ZipFile(파일명, "r") : zip파일을 읽기모드로 읽어와서 zip_obj 변수에 담기
    # 파일 객체 변수명.extractall(압축해제할 폴더 경로)
with zipfile.ZipFile(source_file, "r") as zip_obj:
    zip_obj.extractall(extract_folder)  # 지정한 경로에 압축해제하기

    # 훈련용, 검증용 데이터 저장위치 지정 # "c:/doit/dataset/archive"
train_dir = os.path.join(extract_folder, "C:/doit/dataset/archive/training_set/training_set")
valid_dir = os.path.join(extract_folder, "C:/doit/dataset/archive/test_set/test_set")
# print(train_dir)
# print(valid_dir)

# 2. 정규화
image_gen = ImageDataGenerator(rescale=(1/255.0))   # 이미지 데이터를 0 ~ 255 -> 0 ~ 1로 정규화

# 3. 이미지 제네레이터 : 한번에 많은 데이터를 갖고 왔을 때 문제가 발생할 수도 있기 때문에 이미지를 batch(묶음) 단위로 반복해서 가져오기
    # flow_from_directory() 를 이용한 지정한 폴더에서 32개씩 묶어서 이미지를 반복하여 가져오는 함수
train_gen = image_gen.flow_from_directory(train_dir,    # 훈련용 데이터 저장 위치
                                          batch_size=32,    # batch 단위
                                          target_size=(224, 224),   # 이미지 사이즈 변경
                                          classes = ["cats", "dogs"],   # 문자로된 클래스(종속)를 cats = 0, dogs = 1
                                          class_mode = "binary",    # 이진 분류 사용
                                          seed = 2020)  # 난수 시드값

valid_gen = image_gen.flow_from_directory(valid_dir,    # 검증용 데이터 저장 위치
                                          batch_size=32,    # 배치 단위
                                          target_size = (224, 224),  # 이미지 사이즈 변경
                                          classes = ["cats", "dogs"],   # 문자로된 클래스(종속)를 cats = 0, dogs = 1
                                          class_mode="binary",  # 이진 분류 사용
                                          seed = 2020)  # 난수 시드값

class_labels = ["cats", "dogs"]
batch = next(train_gen)
images = batch[0]   # 독립변수, 개 or 고양이 이미지
labels = batch[1]   # 종속변수, 이미지 정답

for i in range(32):
    ax = plt.subplot(4, 8, i+1)
    plt.imshow(images[i])
    plt.title(class_labels[int(labels[i])]) # int 형 변환

plt.show()

def build_model():

    model = tf.keras.Sequential([
        # Convolution 층
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(32, (3, 3), padding="same", activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(64, (3, 3), padding = "same", activation = "relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(128, (3, 3), padding = "same", activation= "relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),

        # Classifier 출력층
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation = "sigmoid")
    ])

    return model

model = build_model()

model.compile(optimizer=tf.optimizers.Adam(learning_rate= 0.001), loss = tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=["accuracy"])

history = model.fit(train_gen, validation_data= valid_gen, epochs = 20)


def plot_loss_acc(history, epochs):
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    acc = history.history["accuracy"]
    val_acc = history.history["val_accuracy"]

    # 차트 생성
    fig, axes = plt.subplots(1, 2)

    axes[0].plot(range(1, epochs + 1), loss)
    axes[0].plot(range(1, epochs + 1), val_loss)

    axes[1].plot(range(1, epochs + 1), acc)
    axes[1].plot(range(1, epochs + 1), val_acc)

    plt.show()

plot_loss_acc(history, 20)


