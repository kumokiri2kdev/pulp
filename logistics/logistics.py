import numpy as np
import pandas as pd

from itertools import product
from pulp import LpVariable, lpSum, value
from ortoolpy import model_min, addvars, addvals

df_tc = pd.read_csv('trans_cost.csv', index_col='工場')
df_demand = pd.read_csv('demand.csv')
df_supply = pd.read_csv('supply.csv')

nw = len(df_tc.index)
nf = len(df_tc.columns)
pr = list(product(range(nw), range(nf)))

# モデルの定義（最小化)
m1 = model_min()
# 変数の作成
v1 = {(i, j):LpVariable('v%d_%d'%(i,j), lowBound=0) for i,j in pr}

# 目的関数の作成
m1 += lpSum(df_tc.iloc[i][j] * v1[i, j] for i, j in pr)

# 制約条件の作成
## 各倉庫からの供給量が上回らない事
for i in range(nw):
    m1 += lpSum(v1[i, j] for j in range(nf)) <= df_supply.iloc[0][i]
## 各工場の需要を満たす事
for j in range(nf):
    m1 += lpSum(v1[i, j] for i in range(nw)) >= df_demand.iloc[0][j]

# 問題解決
m1.solve()
## これにより、変数 v1 に数値が入力される

df_tr_sol = df_tc.copy()
total_cost = 0
for k, x in v1.items():
    i, j = k[0], k[1]
    df_tr_sol.iloc[i][j] = value(x)
    total_cost += df_tc.iloc[i][j] * value(x)
    
print(df_tr_sol)
print("Total Cost : {}".format(total_cost))

