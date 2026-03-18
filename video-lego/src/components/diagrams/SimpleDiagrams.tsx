// ═══════════════════════════════════════════════════════════
// 简单三栏图解工厂 — 不需要复杂 SVG 的公式
// Simple 3-column diagram factory for text-heavy formulas
// ═══════════════════════════════════════════════════════════

import React from 'react'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'
import { colStyle, dividerStyle, colLabelStyle, boardStyle, conclusionStyle } from './boardStyles'

const animCSS = `
  @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  .sf-f1 { opacity: 0; animation: fadeIn 0.3s ease-out 0.2s forwards }
  .sf-f2 { opacity: 0; animation: fadeIn 0.3s ease-out 0.5s forwards }
  .sf-f3 { opacity: 0; animation: fadeIn 0.3s ease-out 0.8s forwards }
  .sf-f4 { opacity: 0; animation: fadeIn 0.3s ease-out 1.1s forwards }
`

export interface SimpleDef {
  name: string
  latex: string
  color: string
  explain: string[]
  known: string[]
  steps: string[]
  conclusion: string
}

export function makeSimpleDiagram(def: SimpleDef): React.FC<{ compact?: boolean }> {
  const Component: React.FC<{ compact?: boolean }> = ({ compact }) => {
    if (compact) return (
      <div style={{ textAlign: 'center', padding: '6px' }}>
        <div style={{ fontSize: 14, color: def.color }}><BlockMath math={def.latex} /></div>
        <div style={{ color: '#888', fontSize: 9 }}>{def.explain[0]}</div>
      </div>
    )
    return (
      <div style={{ padding: '8px 0' }}>
        <div style={{ padding: '4px 8px', display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(255,255,255,0.02)', borderRadius: '8px 8px 0 0', border: '1px solid rgba(255,255,255,0.06)', borderBottom: 'none' }}>
          <span style={{ fontSize: 14, color: '#fff', fontWeight: 700, whiteSpace: 'nowrap' }}>{def.name}</span>
          <div style={{ flex: 1, fontSize: 18, color: def.color, textAlign: 'center' }}><BlockMath math={def.latex} /></div>
        </div>
        <div style={{ ...boardStyle, borderRadius: '0 0 8px 8px' }}>
          <div style={{ ...colStyle(1), minWidth: 150 }}>
            <div style={colLabelStyle}>解释</div>
            <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
              {def.explain.map((e, i) => <div key={i} style={{ color: i === 0 ? '#ccc' : '#aaa', fontSize: i === 0 ? 12 : 11, marginTop: i > 0 ? 2 : 0 }}>{e}</div>)}
            </div>
          </div>
          <div style={dividerStyle} />
          <div style={{ ...colStyle(1), minWidth: 140 }}>
            <div style={colLabelStyle}>已知</div>
            <div style={{ fontSize: 12, color: '#ccc', lineHeight: 1.8 }}>
              {def.known.map((k, i) => <div key={i} style={{ fontSize: 11, color: i === def.known.length-1 ? '#FFD700' : '#aaa' }}>{k}</div>)}
            </div>
          </div>
          <div style={dividerStyle} />
          <div style={{ ...colStyle(1.3), minWidth: 240 }}>
            <div style={colLabelStyle}>解题过程</div>
            <style>{animCSS}</style>
            <div style={{ fontSize: 11, color: '#aaa', lineHeight: 1.7 }}>
              {def.steps.map((s, i) => <div key={i} className={`sf-f${Math.min(i+1,3)}`}>{s}</div>)}
              <div className="sf-f4" style={conclusionStyle}>
                <span style={{ color: '#FFD700', fontWeight: 700 }}>∴</span> {def.conclusion}
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
  Component.displayName = def.name.replace(/\s/g, '') + 'Diagram'
  return Component
}

// ─── 偏导数 ───
export const PartialDiagram = makeSimpleDiagram({
  name: '偏导数', color: '#3498db',
  latex: String.raw`\frac{\partial f}{\partial x_i}`,
  explain: ['固定其他变量，对一个变量求导', '• 多变量函数的变化率', '• 梯度向量的每个分量', '• 反向传播的基本运算'],
  known: ['f(x,y) = x²y + 3y', '求 ∂f/∂x 和 ∂f/∂y'],
  steps: ['① ∂f/∂x: 把y当常数', '   = 2xy', '② ∂f/∂y: 把x当常数', '   = x² + 3'],
  conclusion: '每个方向一个导数',
})

// ─── 梯度 ───
export const GradientDiagram = makeSimpleDiagram({
  name: '梯度', color: '#2ecc71',
  latex: String.raw`\nabla f = \left[\frac{\partial f}{\partial x_1}, \ldots, \frac{\partial f}{\partial x_n}\right]`,
  explain: ['所有偏导数组成的向量', '• 指向函数上升最快方向', '• 梯度下降取反方向', '• 长度 = 变化剧烈程度'],
  known: ['f(x,y) = x² + y²', '在点 (1,2) 求梯度'],
  steps: ['① ∂f/∂x = 2x = 2', '② ∂f/∂y = 2y = 4', '③ ∇f = [2, 4]'],
  conclusion: '|∇f| = √(4+16) ≈ 4.47',
})

// ─── L2 范数 ───
export const L2NormDiagram = makeSimpleDiagram({
  name: 'L2范数', color: '#4ea8de',
  latex: String.raw`\|\vec{x}\|_2 = \sqrt{\sum_{i=1}^{n} x_i^2}`,
  explain: ['向量的长度/模', '• 欧氏空间的距离', '• L2正则化的核心', '• 权重衰减 = 限制范数'],
  known: ['x⃗ = [3, 4]', '求 ‖x⃗‖₂ = ?'],
  steps: ['① 3² = 9', '② 4² = 16', '③ √(9 + 16) = √25'],
  conclusion: '‖x⃗‖₂ = 5',
})

// ─── 特征值 ───
export const EigenvalueDiagram = makeSimpleDiagram({
  name: '特征值', color: '#9b59b6',
  latex: String.raw`A\vec{v} = \lambda\vec{v}`,
  explain: ['矩阵作用不改变方向的特殊向量', '• v⃗ = 特征向量 (方向不变)', '• λ = 特征值 (缩放倍数)', '• PCA: 找最大特征值对应的方向'],
  known: ['A = [[2,1],[1,2]]', '求 λ 和 v⃗'],
  steps: ['① det(A-λI) = 0', '② (2-λ)²-1 = 0', '③ λ₁=3, λ₂=1'],
  conclusion: 'v₁=[1,1], v₂=[1,-1]',
})

// ─── 条件概率 ───
export const ConditionalDiagram = makeSimpleDiagram({
  name: '条件概率', color: '#1abc9c',
  latex: String.raw`P(A|B) = \frac{P(A \cap B)}{P(B)}`,
  explain: ['已知B发生，A发生的概率', '• 缩小样本空间到B', '• 贝叶斯定理的基础', '• 分类器本质就是条件概率'],
  known: ['掷骰子: A={偶数}, B={>3}', 'P(A∩B)=P({4,6})=2/6', 'P(B)=P({4,5,6})=3/6'],
  steps: ['① P(A∩B) = 2/6', '② P(B) = 3/6', '③ P(A|B) = (2/6)/(3/6)'],
  conclusion: 'P(偶数|>3) = 2/3',
})

// ─── 期望 ───
export const ExpectationDiagram = makeSimpleDiagram({
  name: '期望', color: '#e67e22',
  latex: String.raw`E[X] = \sum_{i} x_i \cdot P(x_i)`,
  explain: ['加权平均值', '• 每个值×出现概率之和', '• 损失函数的理论基础', '• RL: 回报的期望'],
  known: ['骰子 X: 1~6', 'P(每面) = 1/6', '求 E[X] = ?'],
  steps: ['① 1×1/6 + 2×1/6 + 3×1/6', '② + 4×1/6 + 5×1/6 + 6×1/6', '③ = 21/6'],
  conclusion: 'E[X] = 3.5',
})

// ─── 方差 ───
export const VarianceDiagram = makeSimpleDiagram({
  name: '方差', color: '#3498db',
  latex: String.raw`\text{Var}(X) = \frac{1}{n}\sum(x_i - \bar{x})^2`,
  explain: ['数据偏离均值的程度', '• σ² = 方差，σ = 标准差', '• BatchNorm 用方差归一化', '• 方差大 = 数据分散'],
  known: ['X = [2, 4, 6]', 'x̄ = 4', '求 Var(X)'],
  steps: ['① (2-4)² = 4', '② (4-4)² = 0', '③ (6-4)² = 4', '④ Var = (4+0+4)/3'],
  conclusion: 'Var(X) = 8/3 ≈ 2.67',
})

// ─── MAE ───
export const MAEDiagram = makeSimpleDiagram({
  name: 'MAE', color: '#27ae60',
  latex: String.raw`\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|`,
  explain: ['预测偏差的绝对值平均', '• 不像MSE对大误差敏感', '• 对异常值更鲁棒', '• 单位与原数据一致'],
  known: ['y = [3, 5, 7]', 'ŷ = [2.5, 5.5, 6]', '求 MAE'],
  steps: ['① |3-2.5| = 0.5', '② |5-5.5| = 0.5', '③ |7-6| = 1.0', '④ MAE = (0.5+0.5+1)/3'],
  conclusion: 'MAE = 2/3 ≈ 0.67',
})

// ─── 闵可夫斯基 ───
export const MinkowskiDiagram = makeSimpleDiagram({
  name: '闵可夫斯基距离', color: '#1abc9c',
  latex: String.raw`d(x,y) = \left(\sum|x_i - y_i|^p\right)^{1/p}`,
  explain: ['L1/L2 的通用形式', '• p=1 → 曼哈顿距离', '• p=2 → 欧氏距离', '• p→∞ → 切比雪夫距离'],
  known: ['x=[1,2], y=[4,6]', 'p=2 时求 d(x,y)'],
  steps: ['① |1-4|² = 9', '② |2-6|² = 16', '③ (9+16)^(1/2) = √25'],
  conclusion: 'd = 5 (即欧氏距离)',
})

// ─── 动量法 ───
export const MomentumDiagram = makeSimpleDiagram({
  name: '动量法', color: '#3498db',
  latex: String.raw`v_t = \gamma v_{t-1} + \eta \nabla L`,
  explain: ['带惯性的梯度下降', '• γ ≈ 0.9 (动量系数)', '• 像小球滚下山坡', '• 加速收敛，减少震荡'],
  known: ['γ=0.9, η=0.1', '∇L = 2, v₀ = 0', '求前3步的 v'],
  steps: ['① v₁ = 0.9×0 + 0.1×2 = 0.2', '② v₂ = 0.9×0.2 + 0.1×2 = 0.38', '③ v₃ = 0.9×0.38 + 0.1×2 = 0.542'],
  conclusion: '速度逐步积累，加速收敛',
})

// ─── 学习率衰减 ───
export const LearningRateDiagram = makeSimpleDiagram({
  name: '学习率衰减', color: '#f39c12',
  latex: String.raw`\eta_t = \eta_0 \cdot \frac{1}{1 + \alpha t}`,
  explain: ['逐渐减小步长', '• 初期大步快收敛', '• 后期小步精调', '• 防止在最优解附近震荡'],
  known: ['η₀ = 0.1, α = 0.01', '求 t=100 时的 η'],
  steps: ['① 1 + 0.01×100 = 2', '② η₁₀₀ = 0.1 × 1/2 = 0.05', '③ 步长减半'],
  conclusion: '学习率从0.1降到0.05',
})

// ─── 信息熵 ───
export const EntropyDiagram = makeSimpleDiagram({
  name: '信息熵', color: '#e74c3c',
  latex: String.raw`H(X) = -\sum p(x_i) \log p(x_i)`,
  explain: ['不确定性的度量', '• 均匀分布 → 熵最大', '• 确定事件 → 熵=0', '• 决策树:选熵下降最大的特征'],
  known: ['硬币: P(正)=0.5, P(反)=0.5', '求 H(X)'],
  steps: ['① -0.5×log₂(0.5) = 0.5', '② -0.5×log₂(0.5) = 0.5', '③ H = 0.5 + 0.5'],
  conclusion: 'H = 1 bit (最大不确定性)',
})

// ─── KL散度 ───
export const KLDiagram = makeSimpleDiagram({
  name: 'KL散度', color: '#8e44ad',
  latex: String.raw`D_{KL}(P\|Q) = \sum P(x) \log\frac{P(x)}{Q(x)}`,
  explain: ['两个分布的差异(有方向)', '• P=真实, Q=预测', '• D_KL ≥ 0, P=Q时=0', '• VAE的正则化项'],
  known: ['P=[0.7, 0.3]', 'Q=[0.5, 0.5]', '求 D_KL(P‖Q)'],
  steps: ['① 0.7×log(0.7/0.5) = 0.236', '② 0.3×log(0.3/0.5) = -0.153', '③ D_KL = 0.236 + (-0.153)'],
  conclusion: 'D_KL ≈ 0.082 nats',
})
