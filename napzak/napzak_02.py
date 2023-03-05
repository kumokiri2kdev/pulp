# 参考 : http://www.nct9.ne.jp/m_hiroi/light/pulp01.html
import pulp
from pulp import LpStatus
import pandas as pd

goods = [
    {
        'name': 'a',
        'price': 6,
        'weight': 4
    },
    {
        'name': 'b',
        'price': 4,
        'weight': 3
    },
    {
        'name': 'c',
        'price': 1,
        'weight': 1
    }
]

# データの読み出し
df = pd.DataFrame(goods)

# モデルの定義（最大化)
prob = pulp.LpProblem('napzak', sense=pulp.LpMaximize)

# 変数の生成
vars = [pulp.LpVariable(name, cat='Integer', lowBound=0) for name in df['name']]

# 目的関数の設定
prob += pulp.lpDot(df['price'], vars)

#制約条件
prob += pulp.lpDot(df['weight'], vars) <= 10

status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
print("Status", LpStatus[status])

for val in vars:
    print('{} : {}'.format(val, val.value()))

print("Maximum Price", prob.objective.value())
