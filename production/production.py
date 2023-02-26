# 参考 : http://www.nct9.ne.jp/m_hiroi/light/pulp01.html

from pulp import pulp, LpVariable, LpMaximize, lpSum, value, LpStatus
import pandas as pd

products = [
    {
        'product_name': 'product_a',
        'material_w': 2,
        'material_x': 1,
        'material_y': 0,
        'material_z': 0,
        'profit': 5
    },
    {
        'product_name': 'product_b',
        'material_w': 0,
        'material_x': 2,
        'material_y': 1,
        'material_z': 0,
        'profit': 3
    },
    {
        'product_name': 'product_c',
        'material_w': 0,
        'material_x': 0,
        'material_y': 1,
        'material_z': 2,
        'profit': 2
    },
    {
        'product_name': 'product_d',
        'material_w': 1,
        'material_x': 0,
        'material_y': 0,
        'material_z': 2,
        'profit': 4
    }
]

limits = [
    {
        'material_name': 'material_w',
        'limit': 4
    },
    {
        'material_name': 'material_x',
        'limit': 8
    },
    {
        'material_name': 'material_y',
        'limit': 6
    },
    {
        'material_name': 'material_z',
        'limit': 10
    }
]

MINIMUM_PRODUCTION = 0

# データの読み出し
df_product = pd.DataFrame(products)
df_limits = pd.DataFrame(limits)

# モデルの定義（最大化)
prob = pulp.LpProblem('production', sense=LpMaximize)

# 変数の生成
vars = {product : pulp.LpVariable(product, lowBound = MINIMUM_PRODUCTION) for product in df_product['product_name']}

# 目的関数の設定
prob += lpSum(vars[i.product_name] * i.profit for _, i in df_product.iterrows())

# 制約条件の作成
for _,limit in df_limits.iterrows():
    prob += lpSum(material[limit.material_name] * vars[material['product_name']] for _,material in df_product[['product_name',limit.material_name]].iterrows()) <= limit.limit

status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
print("Status", LpStatus[status])

print("Result")
for key, val in vars.items():
    print('{} : {}'.format(key, val.value()))

print("g", prob.objective.value())
