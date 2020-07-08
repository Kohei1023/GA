# -*- coding: utf-8 -*-
import pandas as pd
import random

from deap import base
from deap import creator
from deap import tools
from deap import cma

#from scoop import futures

from member import Member
from team import Team


from tqdm import tqdm
import time
start = time.time()


# menberのインスタンス生成
df = pd.read_csv('../input/DSS2020-04.csv')
#print(df)

m_list = []
for index, row in df.iterrows():
    tmp = Member(row)
    m_list.append(tmp)

'''
for i in m_list:
    print(i.name)
'''


## 遺伝子(設計変数)のセットを表す個体を定義
## creator.create()関数は、あるクラスにメンバ変数を追加して子クラスを新たに作成する関数
# 適応度の定義 #
# base.Fitnessクラスを継承して、weights=(-10.0,)というメンバ変数を追加した
# メンバ変数：ざっくりいうとクラスの中にある変数
# 適応度を表すFitnessMaxというクラスをcreatorモジュール内に作成しています。
# weight：evalShift関数の条件（目的関数）5つに重み付けしている
creator.create("FitnessPeopleCount", base.Fitness, weights=(-10.0, -10.0, -10.0, -10.0, -10.0))
# 個体の定義 #
# listクラスを継承して、fitness=creator.FitnessMaxというメンバ変数を追加したIndividualクラスを作成
# 遺伝子を保存する個体listに、適応度fitnessというメンバ変数を追加してIndividualとしている
creator.create("Individual", list, fitness=creator.FitnessPeopleCount)

# 下記のコードを簡略化するための文
toolbox = base.Toolbox()
#toolbox.register("map", futures.map)

# 遺伝子を作成する関数 #
# base.Toolbox.register()関数を使うと、引数のデフォルト値が無い関数に、デフォルト値を設定できる
# 第2引数で指定する関数に、第3引数以降で指定するデフォルト値を設定して、
# 第1引数で指定する名前でbase.Toolbox内に新しく関数を作成
# ランダムに整数を生成する関数random.randint()のデフォルト引数に0と1を指定してattr_boolという名前の関数を作成
# デフォルト引数に設定した0と1ですが、ランダムに生成する整数の範囲(minとmax値)を表しており、
# 0か1をランダムで返す引数なしで実行できる関数attr_boolが出来上がります。
toolbox.register("attr_bool", random.randint, 0, 1)
# 個体を作成する関数 #
# よくわからない関数tools.initRepeatをindividualによみかえている
# tools.initRepeatは、3個の引数container、func、nを持っており、n回funcを実行して、
# その値をcontainerに格納して返す関数です。
# container=creator.Individual, func = toolbox.attr_bool, n=210 となる
# つまり、210回toolbox.attr_boolを実行し、その値をcreator.Individualに格納して返す関数individualを作成している
# 引数なしで個体を生成できるindividual関数ができたわけです。
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 217) # 染色体を217個性性
# 世代を作成する関数 #
# 個体をtoolbox.individualで作成してlistに格納し、世代を生成するpopulation関数を作っています。
# 世代内の個体数あたるnは、後でmain関数内で指定するので、デフォルト値は設定してないでおきます。
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# 上記３つのコードで
# attr_boolで遺伝子を生成し、individualで個体を生成、populationで世代を生成するというわけ




# シフトの評価関数(目的関数)　 ## ここの関数を変えていく
def evalShift(individual):
    t = Team(individual)
    t.member = m_list

    # 目的関数
    eval1 = t.eval1()
    eval2 = t.eval2()
    eval3 = t.eval3()
    eval4 = t.eval4()
    eval5 = t.eval5()

    return (eval1, eval2, eval3, eval4, eval5)


## 目的関数、また交差・突然変異・選択を求める関数を読みかえている
###### 目的関数 #####
toolbox.register("evaluate", evalShift)
# 交叉関数(二点交叉) #
# デフォルト。
# 二つの個体ind1, ind2を引数として、固体内の遺伝子を2点交叉で入れ替えて返す関数です。
toolbox.register("mate", tools.cxTwoPoint)
# 突然変異関数 #
# デフォルト。
# 一つの個体individualと遺伝子突然変異率indpbを引数にして、固体内の遺伝子を突然変異させて返していますね。
# 遺伝子が0と1のビット値なので、ビット値を入れ替えることで突然変異を表しています。
# indpb=0.05というデフォルト値を与えています。遺伝子突然変異率は5%で決め打ちという事です。
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
# 選択関数(トーナメント選択、tournsizeはトーナメントのサイズ) #
# デフォルト。
# トーナメント選択を実施する関数です。引数はindividuals, k, tournsize, fit_attr="fitness"の4つですね。
# individualsは、個体individualの後ろにsがついており複数形になっています。
#紛らわしいですが、複数ある個体は世代を表すので、この引数には世代(population)を入れてやります。
# kは、世代individuals中の個体の数です。tournsizeはトーナメントサイズです。tournsize=3で決め打ちしています。
# fit_attr="fitness"は、固体のメンバ変数になっている適応度の変数名を指定しています。
# fit_attrはfitness_attribute(適応度_属性)の略だと思います。
# デフォルト値がfitnessになってますね。8行目の個体定義時に、fitnessという名前以外で適応度を登録した場合、
#ここで変えないとエラーになるわけですね。 253行あたりで書き換えているから変更が必要
# Pythonではメンバ変数の事を属性(attribute)とも呼ぶらしいです。
toolbox.register("select", tools.selTournament, tournsize=3)




#random.seed(64)

# 初期集団を生成する
# n=300で世代内の個体数を指定
# toolbox.populationを実行するだけで、遺伝子、固体、世代を一気に作れる
pop = toolbox.population(n=300)
# 交叉率、個体突然変異率、ループを回す世代数を指定
CXPB, MUTPB, NGEN = 0.6, 0.4, 100

print("--進化開始--")

# 初期集団の個体を評価する
# 初期世代の個体の適応度を計算し、メンバ変数fitnessに登録しています。
# 個体内の適応度にはfitness.valuesでアクセスします。
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):  # zipは複数変数の同時ループ
    # 適合性をセットする
    ind.fitness.values = fit

#print("  %i の個体を評価" % len(pop))

# プログラムの進捗確認
bar1 = tqdm(total = NGEN)

 # 進化計算開始
for g in range(NGEN):
    #if g % 100 == 0:
        #print("-- %i 世代 --" % g)

    # 選択 #
    # 364行目で選択した個体をoffspringに格納してから、
    # 366行目でクローンを作ってまたoffspringに入れてますね。
    # 次世代の個体群を選択
    offspring = toolbox.select(pop, len(pop))
    # 個体群のクローンを生成
    # コメントアウトすると、最適化がすすまなくなってしまう
    offspring = list(map(toolbox.clone, offspring))

    # 選択した個体群に交差と突然変異を適応する

    # 交叉
    # 偶数番目と奇数番目の個体を取り出して交叉
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            # 交叉された個体の適合度を削除する
            # 交叉で遺伝子を取り換えた後は、適応度を再計算する必要があるためdelで削除
            del child1.fitness.values
            del child2.fitness.values

    # 突然変異
    for mutant in offspring:
        if random.random() < MUTPB:
            # toolbox.mutate関数に突っ込んで、固体内の遺伝子を突然変異させる
            toolbox.mutate(mutant)
            # 突然変異が発生した個体の適応度を再計算する必要があるためdelで削除
            del mutant.fitness.values

    # 適合度が計算されていない個体を集めて適合度を計算
    # 交叉と突然変異でdelした適応度を再計算
    # if not ind.fitness.validを選んで適応度を再計算させる
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # 一連のステップが完了したので、これ以降の記述は次世代offspringを現世代popにコピー
    # pop[:] = offspring　してまたループするという流れになってます。
    # 次世代群をoffspringにする
    pop[:] = offspring

    # 進捗確認
    bar1.update(1)

best_ind = tools.selBest(pop, 1)[0]
#print("最も優れていた個体: %s, %s" % (best_ind, best_ind.fitness.values))

# チーム編成表示
t = Team(best_ind)
t.member = m_list
t.csv_creator()
t.get_point()

bar1.close()
process_time = time.time() - start
print(f'実行時間:{process_time/60}')
