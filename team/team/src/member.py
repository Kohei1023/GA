# 個人属性
class Member(object):
    def __init__(self, df):
        self.name = df['name']
        self.lab = df['lab']
        self.request1 = df['request1']
        self.request2 = df['request2']
        self.request3 = df['request3']
        self.level = df['level']