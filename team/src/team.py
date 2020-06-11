import random
import csv
import statistics

class Team():
    def __init__(self, list):
        # 数の設定
        # 一人当たりのコマ数
        self.TEAM_N = 3
        self.PEOPLE = 15
        self.TEAM_P_N = self.PEOPLE / self.TEAM_N

        if list == None:
            self.make_sample()
        else:
            self.list = list
        self.member = []

    # ランダムなデータを生成
    def make_sample(self):
        sample_list = []
        for num in range(45):
            sample_list.append(random.randint(0, 1))
        self.list = tuple(sample_list)





    # 出力 #
    # 各チームのポイント合計を表示する
    def get_point(self):
        point = []
        for t in range(self.TEAM_N):
            team = self.get_user(t)
            p = 0
            for m in team:
                p += m.total
            point.append(p)
        print(f'各チームの合計ポイント: {point}')

    # CSV形式でアサイン結果の出力をする
    def print_csv(self):
        with open('output.csv', 'a') as file:
            writer = csv.writer(file, lineterminator='\n')
            for line in self.slice():
                print(','.join(map(str, line)))
                # print((map(str, line)))
                writer.writerows((map(str, line)))

    # TSV形式でアサイン結果の出力をする
    def print_tsv(self):
        for line in self.slice():
            print("\t".join(map(str, line)))




    # タプルの操作 #
    # タプルを1ユーザ単位に分割
    def slice(self):
        sliced = []
        start = 0
        for num in range(self.PEOPLE):  # 人数 15
            sliced.append(self.list[start:(start + self.TEAM_N)])
            start = start + self.TEAM_N  # チーム数 3
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

    # 各チームの人数が5人になっているか
    def eval2(self):
        cost = 0
        for t in range(self.TEAM_N):
            t_num = len(self.get_user(t))
            if t_num > self.TEAM_P_N  or t_num < self.TEAM_P_N :
                cost += 1
                #print(cost)
        return cost

        # 各チームのスコア獲得ポイント合計は平坦か
    def eval3(self):
        cost = 0.1
        point = []
        for t in range(self.TEAM_N):
            team = self.get_user(t)
            p = 0
            for m in team:
                p += m.total #p = p + m.total
            point.append(p)
        pst = statistics.pstdev(point)
        cost = cost * pst
        #print(f'pointは{point} , pstは{pst}, costは{cost}')
        return cost

        # 各チームのスコア獲得ポイント合計は平坦か
    def eval4(self):


        return cost




