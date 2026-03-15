# Convex Optimization Knowledge Map

> 来源课程：Stanford EE364A (Stephen Boyd) · CMU 10-725 · Boyd & Vandenberghe 教材
> 级别：研究生 Master · 角色：ML 工程师
> 前置课程：`linear-algebra` · `calculus` · `optimization`

## 课程定位

凸优化是 ML 的数学引擎 — 几乎所有 ML 算法底层都在求解某种凸/非凸优化问题。

| 维度 | Optimization (基础) | Convex Optimization (研究生) |
|------|---------------------|------------------------------|
| 重点 | 数值方法 + 基本优化 | 凸集/凸函数理论 + 对偶 + 内点法 |
| 数学深度 | 梯度/Hessian | 对偶理论 + KKT + 收敛证明 |
| 工具 | scipy.optimize | CVXPY / MOSEK / Gurobi |

## 主题列表

| 主题 | 文件数 | 状态 | 描述 |
|------|--------|------|------|
| convex_sets | 0 | 🔲 planned | 凸集：凸包、锥、多面体、分离超平面 |
| convex_functions | 0 | 🔲 planned | 凸函数：Jensen不等式、一阶/二阶条件、保凸运算 |
| optimization_problems | 0 | 🔲 planned | LP/QP/SOCP/SDP/GP 问题分类与等价变换 |
| duality | 0 | 🔲 planned | 对偶理论：拉格朗日/对偶问题/KKT/强对偶/Slater条件 |
| unconstrained | 0 | 🔲 planned | 无约束优化：梯度下降/牛顿法/拟牛顿/线搜索/收敛率 |
| constrained | 0 | 🔲 planned | 约束优化：内点法/障碍法/ADMM/增广拉格朗日 |
| first_order_methods | 0 | 🔲 planned | 一阶方法：近端梯度/FISTA/坐标下降/镜像下降/SGD |
| ml_applications | 0 | 🔲 planned | ML应用：Lasso/Ridge/SVM对偶/矩阵补全/在线凸优化 |
