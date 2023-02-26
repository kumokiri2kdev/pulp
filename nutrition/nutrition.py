# 参考 : http://www.nct9.ne.jp/m_hiroi/light/pulp01.html

from pulp import pulp, LpVariable, lpSum, value, LpStatus
import pandas as pd


foods = [
    {
        'food_name': 'a',
        'nutorition_x': 3,
        'nutorition_y' : 1,
        'price': 4
    },
    {
        'food_name': 'b',
        'nutorition_x': 1,
        'nutorition_y': 2,
        'price': 2
    },
    {
        'food_name': 'c',
        'nutorition_x': 2,
        'nutorition_y': 4,
        'price': 5
    }
]

limits = [
    {
        'nutorition_name': 'nutorition_x',
        'limits': 15
    },
    {
        'nutorition_name': 'nutorition_y',
        'limits': 10
    }
]

# データの読み出し
df_foods = pd.DataFrame(foods)
df_limits = pd.DataFrame(limits)

# モデルの定義（最小化(デフォルト))
prob = pulp.LpProblem('nutorition')

# 変数の生成
vars = {food : pulp.LpVariable(food, lowBound = 0) for food in df_foods['food_name']}

# 目的関数の設定
prob += lpSum(vars[i.food_name] * i.price for _, i in df_foods.iterrows())

# 制約条件の作成
for _,limit in df_limits.iterrows():
    prob += lpSum(nutorition[limit.nutorition_name] * vars[nutorition['food_name']] for _,nutorition in df_foods[['food_name',limit.nutorition_name]].iterrows()) >= limit.limits

status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
print("Status", LpStatus[status])
print("Result")
for key, val in vars.items():
    print('{} : {}'.format(key, val.value()))

print("z", prob.objective.value())
