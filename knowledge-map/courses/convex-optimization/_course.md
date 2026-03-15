# 凸优化 Convex Optimization

> 名词总表 · 来源：Boyd & Vandenberghe《Convex Optimization》· Stanford EE364A · CMU 10-725
>
> 级别：研究生 Master · 角色：ML 工程师

---

### 数学基础 Mathematical Foundations

| 名词 | 英文 |
|------|------|
| 向量空间 | Vector Space |
| 范数 | Norm (L1 / L2 / L∞) |
| 内积 | Inner Product |
| 仿射集 | Affine Set |
| 仿射组合 | Affine Combination |
| 超平面 | Hyperplane |
| 半空间 | Halfspace |
| 正定矩阵 | Positive Definite Matrix |
| 半正定矩阵 | Positive Semidefinite Matrix |
| 特征值 | Eigenvalue |
| Hessian 矩阵 | Hessian Matrix |
| 梯度 | Gradient |
| 次梯度 | Subgradient |

---

### 凸集 Convex Sets

| 名词 | 英文 |
|------|------|
| 凸集 | Convex Set |
| 凸组合 | Convex Combination |
| 凸包 | Convex Hull |
| 锥 | Cone |
| 凸锥 | Convex Cone |
| 多面体 | Polyhedron |
| 单纯形 | Simplex |
| 椭球 | Ellipsoid |
| 半正定锥 | Positive Semidefinite Cone (S+) |
| 分离超平面定理 | Separating Hyperplane Theorem |
| 支撑超平面 | Supporting Hyperplane |
| 对偶锥 | Dual Cone |
| 广义不等式 | Generalized Inequality |

---

### 凸函数 Convex Functions

| 名词 | 英文 |
|------|------|
| 凸函数 | Convex Function |
| 严格凸函数 | Strictly Convex Function |
| 强凸函数 | Strongly Convex Function |
| 凹函数 | Concave Function |
| 上图 | Epigraph |
| Jensen 不等式 | Jensen's Inequality |
| 一阶条件 | First-Order Condition |
| 二阶条件 | Second-Order Condition |
| 保凸运算 | Operations that Preserve Convexity |
| 逐点最大 | Pointwise Maximum |
| 透视函数 | Perspective Function |
| 共轭函数 | Conjugate Function (Legendre Transform) |
| 拟凸函数 | Quasiconvex Function |
| 对数凸 | Log-Convex |

---

### 凸优化问题 Convex Optimization Problems

| 名词 | 英文 |
|------|------|
| 优化问题 | Optimization Problem |
| 目标函数 | Objective Function |
| 约束条件 | Constraints |
| 可行域 | Feasible Set |
| 最优值 | Optimal Value |
| 最优解 | Optimal Solution |
| 线性规划 | LP (Linear Programming) |
| 二次规划 | QP (Quadratic Programming) |
| 二次约束二次规划 | QCQP |
| 二阶锥规划 | SOCP (Second-Order Cone Programming) |
| 半正定规划 | SDP (Semidefinite Programming) |
| 几何规划 | GP (Geometric Programming) |
| 松弛 | Relaxation |
| 等价变换 | Equivalent Transformation |

---

### 对偶理论 Duality Theory

| 名词 | 英文 |
|------|------|
| 拉格朗日函数 | Lagrangian |
| 拉格朗日乘子 | Lagrange Multiplier |
| 对偶函数 | Dual Function |
| 对偶问题 | Dual Problem |
| 弱对偶 | Weak Duality |
| 强对偶 | Strong Duality |
| 对偶间隙 | Duality Gap |
| Slater 条件 | Slater's Condition |
| KKT 条件 | KKT (Karush-Kuhn-Tucker) Conditions |
| 互补松弛 | Complementary Slackness |
| 鞍点 | Saddle Point |
| 灵敏度分析 | Sensitivity Analysis |
| 对偶范数 | Dual Norm |

---

### 最优性条件 Optimality Conditions

| 名词 | 英文 |
|------|------|
| 一阶最优性条件 | First-Order Optimality Condition |
| 梯度为零 | Stationarity (∇f = 0) |
| 对偶可行 | Dual Feasibility |
| 原始可行 | Primal Feasibility |
| 互补松弛 | Complementary Slackness |
| 次微分 | Subdifferential |
| 次梯度最优性 | Subgradient Optimality |
| 近端算子 | Proximal Operator |

---

### 无约束优化 Unconstrained Optimization

| 名词 | 英文 |
|------|------|
| 梯度下降 | Gradient Descent |
| 最速下降 | Steepest Descent |
| 牛顿法 | Newton's Method |
| 拟牛顿法 | Quasi-Newton Method |
| BFGS | Broyden-Fletcher-Goldfarb-Shanno |
| L-BFGS | Limited-Memory BFGS |
| 线搜索 | Line Search |
| 回溯线搜索 | Backtracking Line Search |
| Armijo 条件 | Armijo Condition |
| Wolfe 条件 | Wolfe Conditions |
| 收敛速率 | Convergence Rate |
| 线性收敛 | Linear Convergence |
| 二次收敛 | Quadratic Convergence |
| 条件数 | Condition Number |
| Lipschitz 连续 | Lipschitz Continuity |

---

### 约束优化算法 Constrained Optimization Algorithms

| 名词 | 英文 |
|------|------|
| 等式约束牛顿法 | Newton's Method with Equality Constraints |
| 障碍法 | Barrier Method |
| 对数障碍函数 | Log-Barrier Function |
| 内点法 | Interior-Point Method |
| 中心路径 | Central Path |
| 增广拉格朗日法 | Augmented Lagrangian Method |
| ADMM | Alternating Direction Method of Multipliers |
| 罚函数法 | Penalty Method |
| 对偶分解 | Dual Decomposition |
| 切平面法 | Cutting Plane Method |

---

### 一阶方法 First-Order Methods

| 名词 | 英文 |
|------|------|
| 次梯度法 | Subgradient Method |
| 近端梯度法 | Proximal Gradient Method |
| ISTA | Iterative Shrinkage-Thresholding Algorithm |
| FISTA | Fast ISTA (Accelerated Proximal Gradient) |
| 加速梯度法 | Accelerated Gradient Method (Nesterov) |
| 坐标下降 | Coordinate Descent |
| Frank-Wolfe | Frank-Wolfe (Conditional Gradient) |
| 镜像下降 | Mirror Descent |
| 随机梯度下降 | SGD (Stochastic Gradient Descent) |
| 方差缩减 | Variance Reduction (SVRG / SAGA) |
| 投影梯度 | Projected Gradient |

---

### ML 中的凸优化应用 Convex Optimization in ML

| 名词 | 英文 |
|------|------|
| 正则化回归 | Regularized Regression |
| Lasso (L1) | Lasso (L1 Regularization) |
| Ridge (L2) | Ridge Regression (L2 Regularization) |
| 弹性网 | Elastic Net |
| SVM 对偶 | SVM Dual Problem |
| 核学习 | Kernel Learning |
| 矩阵补全 | Matrix Completion |
| 鲁棒优化 | Robust Optimization |
| 在线凸优化 | Online Convex Optimization |
| 压缩感知 | Compressed Sensing |
| 低秩近似 | Low-Rank Approximation |

---

### 工具 Tools

| 名词 | 英文 |
|------|------|
| CVXPY | CVXPY (Python) |
| CVX | CVX (MATLAB) |
| CVXR | CVXR (R) |
| 学科规范形式 | Disciplined Convex Programming (DCP) |
| 求解器 | Solver (SCS / MOSEK / ECOS / Gurobi) |
