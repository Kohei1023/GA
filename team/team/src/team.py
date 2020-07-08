import random
import pandas as pd
import statistics
import collections

class Team():
    def __init__(self, list):
        # 数の設定
        # 一人当たりのコマ数
        self.TEAM_N = 7
        self.PEOPLE = 31
        self.TEAM_P_N = round(self.PEOPLE / self.TEAM_N)

        # 結果を保存するDF
        self.output = pd.DataFrame()
        self.tmp = pd.DataFrame()

        if list == None:
            self.make_sample()
        else:
            self.list = list
        self.member = []

    # ランダムなデータを生成
    def make_sample(self):
        sample_list = []
        for num in range(self.TEAM_N*self.PEOPLE):
            sample_list.append(random.randint(0, 1))
        self.list = tuple(sample_list)


    # 出力 #
    # CSV形式で結果を出力
    def csv_creator(self):
        for i in range(self.TEAM_N):
            team = self.get_user(i)
            count = int(i+1)
            for m in team:
                self.tmp['team'] = [count]
                self.tmp['name'] = [m.name]
                self.tmp['lab'] = [m.lab]
                self.tmp['request1'] = [m.request1]
                self.tmp['request2'] = [m.request2]
                self.tmp['request3'] = [m.request3]
                self.tmp['level'] = [m.level]

                self.output = pd.concat([self.output, self.tmp], axis=0)
        self.output = self.output.reset_index()

        #df = output[output['']]

        self.output = self.output.drop('index', axis=1)
        self.output.to_csv('../output/DSS2020-04_output.csv')

    # 各チームのポイント合計を表示する
    def get_point(self):
        point = []
        for t in range(self.TEAM_N):
            team = self.get_user(t)
            p = 0
            for m in team:
                p += m.level
            point.append(p)
        print(f'各チームの合計ポイント: {point}')




    # タプルの操作 #
    # タプルを1ユーザ単位に分割
    def slice(self):
        sliced = []
        start = 0
        for num in range(self.PEOPLE):  # 人数 31
            sliced.append(self.list[start:(start + self.TEAM_N)])
            start = start + self.TEAM_N  # チーム数 7
        #print(sliced)
        return tuple(sliced)

    # 指定されたチームにアサインされているユーザリストを返す
    def get_user(self, t):
        m = self.slice()
        count = 0
        team = []
        for i in m:
            if i[t] == 1:
                team.append(self.member[count])
            count += 1
        #print(f'{t}チームの人数は{len(team)}')
        return team



    # 目的関数 #
    # 1人1チームに割当されているか
    def eval1(self):
        m = self.slice()
        cost = 0
        for i in m:
            teams = sum(i)
            if teams > 1:
                cost += teams
            elif teams == 0:
                cost += 1
            else:
                pass
        return cost

    # 各チームの人数が4, 5人になっているか
    def eval2(self):
        cost = 1
        tmp = []
        for t in range(self.TEAM_N):
            t_num = len(self.get_user(t))
            tmp.append(t_num)
            if t_num > self.TEAM_P_N or t_num < self.TEAM_P_N:
                cost += abs(self.TEAM_P_N - t_num)
        pst = statistics.pstdev(tmp)
        cost *= pst
        return cost

    # labがかぶらないように
    def eval3(self):
        cost = 1
        for t in range(self.TEAM_N):
            lab_list = {'ichikawa':0, 'Independent':0, 'muto':0, 'nakai':0}
            for u in self.get_user(t):
                if u.lab == 'ichikawa':
                    lab_list['ichikawa'] += 1
                elif u.lab == 'Independent':
                    lab_list['Independent'] += 1
                elif u.lab == 'muto':
                    lab_list['muto'] += 1
                elif u.lab == 'nakai':
                    lab_list['nakai'] += 1
            pst = statistics.pstdev(lab_list.values())
            for i in lab_list:
                if lab_list[i] == 0:
                    cost += 1
                elif i == 'ichikawa' and lab_list[i] > 2:
                    cost += 10
                elif lab_list[i] > 1:
                    cost += 10
        cost *= pst
        return cost

    # 各チームのlevel合計は平坦か
    def eval4(self):
        cost = 1
        point = []
        for t in range(self.TEAM_N):
            team = self.get_user(t)
            p = 0
            for m in team:
                p += m.level
            point.append(p)
        pst = statistics.pstdev(point)
        cost *= pst
        return cost

    # リクエストに答えられているか
    def eval5(self):
        cost = 0
        for t in range(self.TEAM_N):
            team = self.get_user(t)
            tmp = []
            count = {}
            for m in team:
                tmp.append(m.request1)
            count = collections.Counter(tmp)
            print(count)
            input()


        return cost




