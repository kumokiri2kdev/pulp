import pulp

# 1. モデルの作成
prob = pulp.LpProblem('test_01')

# 2. 変数の作成
x = pulp.LpVariable('x', lowBound = 0)
y = pulp.LpVariable('y', lowBound = 0)

# 3. 目的関数の設定
prob += x + y + 1

# 4. 制約条件の作成　
prob += 3 * x + 5 * y <= 15
prob += 2 * x + y >= 4
prob += x - y == 1

print(prob)

# 5. 最適解の計算
status = prob.solve()
print('Status : {}'.format(pulp.LpStatus[status]))

# 6. 結果表示
print('>> result')
print('x : {}'.format(x.value()))
print('y : {}'.format(y.value()))
print('z : {}'.format(prob.objective.value()))

