# 2_딕셔너리.py

#   > key 와 value 를 한 쌍으로 가지는 자료형
#       > {key1 : value1, key2 : value2, key3 : value3}

# 1) 딕셔너리의 형테
dic = {'name' : 'pey', 'phone' : '010-9999-1234', 'birth' : '1118'}
a = {1 : 'hi'}
a = {'a' : [1,2,3]}

# 2) 딕셔너리의 쌍 추가, 삭제
    # [1] 추가, 수정
dic['addr'] = '인천시'     # 변수명['key'] = 초기값, 딕셔너리 내 존재하지 않는 key 라면 쌍 추가
print(dic)      # {'name': 'pey', 'phone': '010-9999-1234', 'birth': '1118', 'addr': '인천시'}

dic['name'] = 'kim'      # 변수명['key'] = 새로운 값, 딕셔너리 내 존재하는 key 라면 value 수정
print(dic)      # {'name': 'kim', 'phone': '010-9999-1234', 'birth': '1118', 'addr': '인천시'}

    # [2] 삭제
del dic['addr']          # del 변수명['key'], 딕셔너리 내 존재하는 key 면 쌍 삭제
print(dic)      # {'name': 'kim', 'phone': '010-9999-1234', 'birth': '1118'}

# del dic['age']  # KeyError: 'age' , 딕셔너리 내 존재하지 않는 key 이므로 예외 발생

# 3) 딕셔너리에서 key 를 이용한 value 추출
print(dic['name'])    # 변수명['key'], 딕셔너리 내 존재하는 key 면 value 반환
# print(dic.name)     # AttributeError: 'dict' object has no attribute 'name'
# print(dic['age'])   # KeyError: 'age', 딕셔너리 내 존재하지 않는 key 면 예외 발생
print(dic['phone'])   # 010-9999-1234

# 4) 딕셔너리 만들 때 주의할 점
    # [1] 중복된 key의 이름을 가질 수 없다, key 는 중복 불가능, value 는 중복 가능
a = {1 : 'a', 1 : 'b'}
print(a)        # {1: 'b'}, key는 중복이 불가능하므로 마지막 쌍이 적용된다.

    # [2] 리스트 타입으로는 key 사용이 불가능, key 가 변화하는 값인지 변하지 않는 값인 지가 달려있다.
# a = {[1,2] : 'hi'}      # TypeError: unhashable type: 'list'

# 5) 딕셔너리 관련 함수들
    # [1] .keys() : 딕셔너리 내 모든 key를 객체로 반환
print(dic.keys())           # dict_keys(['name', 'phone', 'birth'])

    # [2] list(객체) : 객체를 리스트로 변환해서 반환하는 함수
print(list(dic.keys()))     # ['name', 'phone', 'birth']

    # [3] .values() : 딕셔너리 내 모든 value 를 객체로 반환
print(dic.values())         # dict_values(['kim', '010-9999-1234', '1118'])
print(list(dic.values()))   # ['kim', '010-9999-1234', '1118']

    # [4] .items() : 딕셔너리 내 모든 쌍을 튜플로 묶은 객체로 반환하는 함수
print(dic.items())          # dict_items([('name', 'kim'), ('phone', '010-9999-1234'), ('birth', '1118')])
print(list(dic.items()))    # [('name', 'kim'), ('phone', '010-9999-1234'), ('birth', '1118')]

    # [5] .get('key') : 딕셔너리 내 key 에 해당하는 value 반환하는 함수
print(dic.get('name'))      # kim, 만일 딕셔너리 내 존재하는 key 면 value 반환
print(dic.get('age'))       # None, 만일 딕셔너리 내 존재하는 key 가 아니면 None 반환, dic['age'] 보다 조금 더 안전한 방법이다.

    # [6] key in 딕셔너리 변수명 : 딕셔너리 내 key 가 존재하는지 여부 반환 함수
print('name' in dic)        # True, 존재하면 true
print('age' in dic)         # False, 존재하지 않으면 false

    # [7] .clear() : 딕셔너리 내 모든 쌍 삭제
dic.clear()
print(dic)                  # {}

