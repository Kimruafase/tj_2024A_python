# day07 > task9 > Region.py

class Region :
    def __init__(self,region,people, man, woman, home): # 생성자
        self.region = region
        self.people = int(people)
        self.man = int(man)
        self.woman = int(woman)
        self.home = int(home)

    def ratio(self, people, man) :
        return int(100*(self.man / self.people))    # 전체 인구수에 따른 남자 인구수 비율 계산