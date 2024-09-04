# day15 > 3_타이타닉_상관_분석.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. seaborn 라이브러리에 내장된 "타이타닉" 데이터를 가져오기
titanic = sns.load_dataset("titanic")
print(titanic)

# 2. 내장된 데이터를 호출해서 csv 파일로 저장
titanic.to_csv("타이타닉.csv", index=True)

# 3. 결측값(누락된 값 / 공백)
print(titanic.isnull().sum())
"""
survived         0
pclass           0
sex              0
age            177
sibsp            0
parch            0
fare             0
embarked         2
class            0
who              0
adult_male       0
deck           688
embark_town      2
alive            0
alone            0
dtype: int64
"""
print("----------------------------------------------")

# 4. 결측값을 치환, fillna : n -> null(결측값)을 특정 값으로 채워주는 함수
    # 4 - 1. age 열의 결측값을 중앙값(순차적으로 정렬했을 때 가운데의 값)으로 치환
    # median() : 중앙값을 반환해주는 함수
titanic["age"] = titanic["age"].fillna(titanic["age"].median())
print(titanic.isnull().sum())   # 확인 -> age 에 결측값이 없어짐
"""
survived         0
pclass           0
sex              0
age              0
sibsp            0
parch            0
fare             0
embarked         2
class            0
who              0
adult_male       0
deck           688
embark_town      2
alive            0
alone            0
dtype: int64
"""
print("----------------------------------------------")

    # 4 - 2. embarked 열의 결측값을 최빈값(집합의 빈도가 가장 많은 값)으로 치환
print(titanic["embarked"].value_counts())
"""
embarked
S    644
C    168
Q     77
"""
titanic["embarked"] = titanic["embarked"].fillna("S")
print(titanic.isnull().sum())
"""
survived         0
pclass           0
sex              0
age              0
sibsp            0
parch            0
fare             0
embarked         0
class            0
who              0
adult_male       0
deck           688
embark_town      2
alive            0
alone            0
dtype: int64
"""
print("----------------------------------------------")

    # 4 - 3. embarked_town 열의 결측값을 최빈값으로 치환
print(titanic["embark_town"].value_counts())
"""
embark_town
Southampton    644
Cherbourg      168
Queenstown      77
"""
titanic["embark_town"] = titanic["embark_town"].fillna("Southampton")
print(titanic.isnull().sum())
"""
survived         0
pclass           0
sex              0
age              0
sibsp            0
parch            0
fare             0
embarked         0
class            0
who              0
adult_male       0
deck           688
embark_town      0
alive            0
alone            0
dtype: int64
"""
print("----------------------------------------------")

    # 4 - 4. deck 열의 결측값을 최빈값으로 치환
print(titanic["deck"].value_counts())
"""
deck
C    59
B    47
D    33
E    32
A    15
F    13
G     4
Name: count, dtype: int64
"""
titanic["deck"] = titanic["deck"].fillna("C")
print(titanic.isnull().sum())
"""
survived       0
pclass         0
sex            0
age            0
sibsp          0
parch          0
fare           0
embarked       0
class          0
who            0
adult_male     0
deck           0
embark_town    0
alive          0
alone          0
dtype: int64
"""
print("----------------------------------------------")

    # 4 - 5. 데이터의 기본 정보 탐색
print(titanic.info())
"""
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 891 entries, 0 to 890
Data columns (total 15 columns):
 #   Column       Non-Null Count  Dtype   
---  ------       --------------  -----   
 0   survived     891 non-null    int64   
 1   pclass       891 non-null    int64   
 2   sex          891 non-null    object  
 3   age          891 non-null    float64 
 4   sibsp        891 non-null    int64   
 5   parch        891 non-null    int64   
 6   fare         891 non-null    float64 
 7   embarked     891 non-null    object  
 8   class        891 non-null    category
 9   who          891 non-null    object  
 10  adult_male   891 non-null    bool    
 11  deck         891 non-null    category
 12  embark_town  891 non-null    object  
 13  alive        891 non-null    object  
 14  alone        891 non-null    bool    
dtypes: bool(2), category(2), float64(2), int64(4), object(5)
memory usage: 80.7+ KB
None
"""
print("----------------------------------------------")

    # survived(생존자 여부) 속성의 레코드 갯수
print(titanic.survived.value_counts())
"""
survived    0 : 사망자, 1 : 생존자
0    549
1    342
Name: count, dtype: int64
"""

# 차트를 통해 시각적으로 탐색
    # 1) 남자 승객과 여자 승객의 생존율 비교 0 : 사망, 1 : 생존
    # plot을 1행 2열로 구성하고 사이즈를 (10, 5)로 구성하겠다는 의미, ax = ax[0] -> 첫번째 자리, ax[1] -> 두번째 자리
f , ax = plt.subplots(1, 2, figsize = (10, 5))
    # 원형 차트 구성, autopct : 원형 차트 내 각 조각 백분율 표시, explode[0, b] : 두 번째 조각을 (b x 100)% 정도 떨어뜨리기
    # shadow : 차트에 그림자 생기게 하기
titanic["survived"][titanic["sex"] == "male"].value_counts().plot.pie(explode=[0, 0.1], autopct ="%1.1f%%", ax = ax[0], shadow = True)
titanic["survived"][titanic["sex"] == "female"].value_counts().plot.pie(explode=[0, 0.1], autopct ="%1.1f%%", ax = ax[1], shadow = True)

ax[0].set_title("Survived (Male)")
ax[1].set_title("Survived (Female)")

plt.show()

    # 2) 객실 등급별 생존자 수, x축 : 등급(속성명), hue : 생존자 여부(속성별 갯수) -> 등급별 생존자 여부 갯수, data = DataFrame
sns.countplot(x = "pclass", hue = "survived", data = titanic)

plt.title("Pclass vs Survived")
    # 생존자는 1등급에서 가장 많고 사망자는 3등급에서 가장 많다.
plt.show()

    # 3) 동행 여부 속성에 따른 생존자 수
sns.countplot(x = "alone", hue = "survived", data= titanic)
    # 혼자일 때가 사망자 비율이 더 크다.
plt.show()


# 상관 분석 : 연속형 데이터만 가능, 예측치가 없다.(회귀 분석과 다른 점)
    # 연속형 데이터만 가능하므로 연속형 데이터 열만 추출 -> .select_dtypes(include=[타입1, 타입2, 타입3])
titanic2 = titanic.select_dtypes(include=[int, float, bool])
titanic_corr = titanic2.corr(method = "pearson")
print(titanic_corr)
"""
            survived    pclass       age  ...      fare  adult_male     alone
survived    1.000000 -0.338481 -0.064910  ...  0.257307   -0.557080 -0.203367
pclass     -0.338481  1.000000 -0.339898  ... -0.549500    0.094035  0.135207
age        -0.064910 -0.339898  1.000000  ...  0.096688    0.247704  0.171647
sibsp      -0.035322  0.083081 -0.233296  ...  0.159651   -0.253586 -0.584471
parch       0.081629  0.018443 -0.172482  ...  0.216225   -0.349943 -0.583398
fare        0.257307 -0.549500  0.096688  ...  1.000000   -0.182024 -0.271832
adult_male -0.557080  0.094035  0.247704  ... -0.182024    1.000000  0.404744
alone      -0.203367  0.135207  0.171647  ... -0.271832    0.404744  1.000000

[8 rows x 8 columns]
> 상관 계수 : 0 ~ 1 정도와 방향을 하나의 수치로 요약 -> 0에 가까우면 관계 X, 1에 가까울수록 관계가 강하다
    > 양의 상관 관계는 한 변수가 증가하면 다른 변수도 증가한다.
    > 음의 상관 관계는 한 변수가 증가하면 다른 변수는 감소한다.
> 분석 : 남자 성인은 생존 여부와 음의 상관 관계, 객실 등급은 생존 여부와 음의 상관 관계, 혼자 탑승한 경우 생존 여부와 음의 상관 관계 
    > 남자가 증가하면 생존 여부가 감소한다, 객실 등급이 증가하면 생존 여부가 감소한다, 
"""

# 상관 계수를 csv로 저장
titanic_corr.to_csv("타이타닉_상관_계수표.csv", index =True)

# 특정한 변수 사이의 상관 계수 추출
    # survived : 종속 변수(생존율), adult_male : 독립 변수(어른 남성)
print(titanic["survived"].corr(titanic["adult_male"]))  # -0.5570800422053259

    # survived : 종속 변수(생존율), fare : 독립 변수(객실 비용)
print(titanic["survived"].corr(titanic["fare"]))        # 0.2573065223849622