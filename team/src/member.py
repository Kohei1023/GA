# 個人属性
class Member(object):
    def __init__(self, df):
        self.name = df['name']
        self.total = df['total']

