import pulp
from itertools import product

factory_labels = [
    'F-A',
    'F-B',
    'F-C',
    'F-D'
]
warefouse_labels = [
    'W-A',
    'W-B',
    'W-C'
]


# 輸送コスト
trans_costs = [
    #[F-A,F-B,F-C,F-D]
    [10, 10, 11, 27], #W-A
    [18, 21, 12, 14], #W-B
    [15, 12, 14, 12], #W-C
]
# 在庫
stock = [35,41,42]
# 注文
order = [28,29,31,25]



# 1. モデルの作成
prob = pulp.LpProblem('test_02')

# 2. 変数の作成
warefouse_count = len(trans_costs)
factory_count = len(trans_costs[0])
warehouse_factory = list(product(range(warefouse_count), range(factory_count)))
v1 = {(i, j):pulp.LpVariable('v%d_%d'%(i,j), lowBound=0) for i,j in warehouse_factory}

# 3. 目的関数の設定
prob += pulp.lpSum(trans_costs[i][j] * v1[i, j] for i, j in warehouse_factory)

# 4. 制約条件の作成　
for i in range(warefouse_count):
    prob += pulp.lpSum(v1[i, j] for j in range(factory_count)) <= stock[i]

for j in range(factory_count):
    prob += pulp.lpSum(v1[i, j] for i in range(warefouse_count)) >= order[j]

# 5. 最適解の計算
prob.solve()
status = prob.solve()

# 6. 結果表示
print('Status : {}'.format(pulp.LpStatus[status]))
print('>> result')

for k, x in v1.items():
    print('Warehouse({}) => Factory({}) : {}'.format(k[0], k[1], x.value()))

print('total cost : {}'.format(prob.objective.value()))



