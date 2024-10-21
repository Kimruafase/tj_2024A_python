# day35 > 2_NLP.py

# 텐서플로 토크나이저
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

sentences = [
    "영실이는 나를 정말 정말 좋아해",
    "영실이는 영화를 좋아해"
]   # 문장들

# 토크나이저 객체 생성
tokenizer = Tokenizer()

# .fit_on_texts(문장 list)
tokenizer.fit_on_texts(sentences)

# 결과 출력
    # 단어 사전 {단어 : 인덱스}, 빈도수 순, 중복 단어 제외
# print(tokenizer.word_index) # {'영실이는': 1, '정말': 2, '좋아해': 3, '나를': 4, '영화를': 5}

# 벡터로 변환
    # 1 : 영실이는, 2 : 정말, 3 : 좋아해, 4 : 나를, 5 : 영화를
# print(tokenizer.texts_to_sequences(sentences))  # [[1, 4, 2, 2, 3], [1, 5, 3]]

# 새로운 단어
new_sentences = ["영실이는 경록이와 나를 좋아해"]    # "경록이와"는 전에 없던 문자이다.
    # 1 : 영실이는, 4 : 나를, 3 : 좋아해 -> "경록이와"는 전에 없던 문자이기 떄문에 인코딩에서 제외
# print(tokenizer.texts_to_sequences(new_sentences))  # [[1, 4, 3]]

# 새로운 단어 처리 방법
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index

new_word_encoding = tokenizer.texts_to_sequences(new_sentences)

# print(word_index)   # {'<OOV>': 1, '영실이는': 2, '정말': 3, '좋아해': 4, '나를': 5, '영화를': 6}
# print(tokenizer.texts_to_sequences(sentences))  # [[2, 5, 3, 3, 4], [2, 6, 4]]
# print(new_word_encoding)    # [[2, 1, 5, 4]]

# 단어 사전의 최대 개수 설정, 최대 개수 외의 단어들은 <OOV>로 인코딩
    # 사전 목록의 단어수는 최대 3개이며 나머지는 <OOV>이다.
    # num_words = n, n - 1개를 최대 개수로 정함
tokenizer = Tokenizer(num_words = 4, oov_token="<OOV>")
tokenizer.fit_on_texts(sentences)   # 사전 학습
# print(tokenizer.word_index) # {'<OOV>': 1, '영실이는': 2, '정말': 3, '좋아해': 4, '나를': 5, '영화를': 6}
# print(tokenizer.texts_to_sequences(sentences))  # [[2, 1, 3, 3, 1], [2, 1, 1]]
# print(tokenizer.texts_to_sequences(new_sentences))  # [[2, 1, 1, 1]], 2 : 영실이는, 1 : 경록이와, 1 : 나를, 1 : 좋아해

# 문장 길이 맞추기, 패딩, pad_sentences(인코딩한 단어들) : 문장의 길이를 맞춘다. 앞 쪽에 0을 채움
word_encoding = tokenizer.texts_to_sequences(sentences)
# print(word_encoding)    # [[2, 1, 3, 3, 1], [2, 1, 1]]

# print(pad_sequences(word_encoding)) # 두번째 문장의 앞에 [0 0] 추가됨, 첫번째 문장과 길이 맞춘 것
"""
[[2 1 3 3 1]
 [0 0 2 1 1]]
"""

    # padding = "post" : 뒤쪽에 0으로 채움, 생략 시 앞에 0으로 채움
# print(pad_sequences(word_encoding, padding="post"))
"""
[[2 1 3 3 1]
 [2 1 1 0 0]]
"""
    # maxlen = n : 최대 n개만 출력
# print(pad_sequences(word_encoding, padding="post", maxlen=4))
"""
[[1 3 3 1]
 [2 1 1 0]]
"""

    # truncation = "post" : 뒤쪽부터 자름, 생략 시 앞쪽부터 자름
# print(pad_sequences(word_encoding, padding="post", maxlen=4, truncating="post"))
"""
[[2 1 3 3]
 [2 1 1 0]]
"""

