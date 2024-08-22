# day07 > 1_클래스.py
from idlelib.autocomplete import FORCE
from os import remove


# 클래스란? 객체를 실체화하기 위한 설계도, 타입 생성
    # 인스턴스란? 객체를 실체화된 메모리
    # 객체란? 추상적 개념, 물리적 개념으로 고유성질(변수)과 행위(함수)를 정의한 것

# [1] 클래스 구조 만들기

# [1-1] 간단한 클래스

class Fourcal :
    pass # 아무것도 수행하지 않는 문법으로, 임시로 코드를 작성할 때 주로 사용됨.

# [1-2] 객체 생성, 클래스명()
a = Fourcal()
print(type(a))  # <class '__main__.Fourcal'> , type() -> 타입 반환해주는 함수

# [2] 클래스 내 메소드(함수) 만들기
# [2-1] 클래스 내 메소드 선언
    # 함수 코드는 객체들이 공유해서 사용하기 때문에 self로 구별해야한다. (자신 객체라는 것을 표현하기 위해서)
class Fourcal :

    # 생성자
    def __init__(self,first,second):
        self.first = first
        self.second = second

    def setdata(self,first, second):    # 함수 / 메소드 정의 , 매개변수란 함수 호출 시 전달되는 인자값을 저장하는 함수
        self.first = first              # self : 자신 객체, self.first : 객체 변수가 생성된다. -> 4
        self.second = second            # 함수를 호출한 객체(self) 내 second 변수를 선언하고 매개변수(2)를 저장한다.

    def add(self):
        return self.first + self.second   # self : 해당 함수를 호출힌 객체 자신 self.변수(멤버변수 / 필드)

    def mul(self):
        return self.first * self.second   # return 은 함수 종료 시 호출했던 곳으로 반환되는 값

    def sub(self):
        return self.first - self.second

    def div(self):
        return self.first / self.second

# [2-2] 객체 생성
# a = Fourcal()
#
# # [2-3] 객체 내 메소드 실행
# a.setdata(4,2)
# print(a.add())  # 6
# print(a.mul())  # 8
# print(a.sub())  # 2
# print(a.div())  # 2.0
#
# # [2-3] 객체 생성, a 에 저장된 객체와 b에 저장된 객체는 다르다. 타입은 같지만
# b = Fourcal()
# b.setdata(3,7)
# print(b.first)
# print(b.second)
# print(b.add())  # 10
# print(b.mul())  # 21
# print(b.sub())  # -4
# print(b.div())  # 0.42857142857142855
#
#
# # [2-4] 객체 내 필드값 호출
# print(a.first)      # 4
# print(a.second)     # 2

# [2-5] 객체 생성 시 생성자 매개변수 이용
c = Fourcal(2,4)
print(c.first)
print(c.second)

# [3] 상속
    # 상속 : 상위 클래스로부터 물려받아 클래스 연장하기
# [3-1] 하위 클래스 정의, class 클래스명(상위 클래스명) :
class MoreFourCal(Fourcal) :
    def pow(self):
        return self.first ** self.second

    # 오버라이딩
    def div(self):  # 메소드 선언부를 동일하게 작성해야 한다.
        if self.second == 0 :
            return 0
        else :
            return self.first / self.second

a = MoreFourCal(4,2)
print(type(a))      # <class '__main__.MoreFourCal'>
print(a.add())      # 6, 상위 클래스의 메소드 호출

print(a.pow())      # 16, 본인 클래스의 메소드 호출
print(a.div())      # 2.0, 상위 클래스에서 오버라이딩한 본인 클래스의 메소드 호출

# [4] 클래스 변수
    # 객체 변수   : 객체변수명.변수명, 객체마다의 사용되는 변수, 멤버변수 라고도 한다.
    # 클래스 변수 : 클래스명.변수명, 모든 객체가 공유해서 사용하는 변수
        # 객체변수와 클래스변수의 이름이 같아도 식별이 가능하다.
class Family :
    lastname = "김"  # 클래스변수

print(Family.lastname)      # 김

a = Family()
print(a.lastname)           # 김

b = Family()
print(b.lastname)           # 김

Family.lastname = "박"
print(f"{a.lastname}, {b.lastname}")    # 박, 박