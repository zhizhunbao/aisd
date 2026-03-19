// 基底图解 — 坐标系 + 基向量
import React from 'react';

export const BasisDiagram: React.FC = () => {
  const cx = 100;
  const cy = 110;

  return (
    <svg width={220} height={170} viewBox="0 0 220 170">
      {/* 网格 */}
      {[...Array(5)].map((_, i) => (
        <g key={i}>
          <line
            x1={cx + (i - 2) * 35}
            y1={20}
            x2={cx + (i - 2) * 35}
            y2={150}
            stroke="rgba(255,255,255,0.06)"
            strokeWidth={1}
          />
          <line
            x1={20}
            y1={cy + (i - 2) * 35}
            x2={200}
            y2={cy + (i - 2) * 35}
            stroke="rgba(255,255,255,0.06)"
            strokeWidth={1}
          />
        </g>
      ))}

      {/* 基向量 e1 */}
      <line x1={cx} y1={cy} x2={cx + 70} y2={cy} stroke="#4ea8de" strokeWidth={3} />
      <polygon points={`${cx + 70},${cy} ${cx + 62},${cy - 5} ${cx + 62},${cy + 5}`} fill="#4ea8de" />
      <text x={cx + 75} y={cy + 5} fill="#4ea8de" fontSize={16} fontFamily="Inter" fontWeight="bold">e₁</text>

      {/* 基向量 e2 */}
      <line x1={cx} y1={cy} x2={cx} y2={cy - 70} stroke="#2ecc71" strokeWidth={3} />
      <polygon points={`${cx},${cy - 70} ${cx - 5},${cy - 62} ${cx + 5},${cy - 62}`} fill="#2ecc71" />
      <text x={cx + 8} y={cy - 72} fill="#2ecc71" fontSize={16} fontFamily="Inter" fontWeight="bold">e₂</text>

      {/* 示例向量 v = 2e1 + 1.5e2 */}
      <line x1={cx} y1={cy} x2={cx + 56} y2={cy - 42} stroke="#ffd700" strokeWidth={2} strokeDasharray="5,3" />
      <circle cx={cx + 56} cy={cy - 42} r={3} fill="#ffd700" />
      <text x={cx + 62} y={cy - 40} fill="#ffd700" fontSize={13} fontFamily="Inter">v</text>

      {/* 原点 */}
      <circle cx={cx} cy={cy} r={3} fill="white" />

      {/* 标注 */}
      <text x={110} y={162} textAnchor="middle" fill="#888" fontSize={12} fontFamily="Noto Sans SC">
        任何向量 = 基向量的线性组合
      </text>
    </svg>
  );
};
