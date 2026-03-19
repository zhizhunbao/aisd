// 行列式图解 — 面积缩放可视化
import React from 'react';

export const DeterminantDiagram: React.FC = () => {
  return (
    <svg width={260} height={170} viewBox="0 0 260 170">
      {/* 原始单位正方形 */}
      <rect x={20} y={40} width={80} height={80} fill="rgba(78,168,222,0.15)" stroke="#4ea8de" strokeWidth={1.5} rx={2} />
      <text x={60} y={85} textAnchor="middle" fill="#4ea8de" fontSize={14} fontFamily="Inter">面积=1</text>

      {/* 箭头 */}
      <path d="M 110 80 L 130 80" stroke="#ffd700" strokeWidth={2} markerEnd="url(#detArrow)" />
      <defs>
        <marker id="detArrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
          <path d="M 0 0 L 8 4 L 0 8 Z" fill="#ffd700" />
        </marker>
      </defs>

      {/* 变换后平行四边形 */}
      <polygon
        points="140,100 200,100 220,35 160,35"
        fill="rgba(255,215,0,0.12)"
        stroke="#ffd700"
        strokeWidth={1.5}
      />
      <text x={180} y={75} textAnchor="middle" fill="#ffd700" fontSize={14} fontFamily="Inter" fontWeight="bold">
        面积=|det(A)|
      </text>

      {/* 底部标注 */}
      <text x={60} y={145} textAnchor="middle" fill="#888" fontSize={12} fontFamily="Noto Sans SC">变换前</text>
      <text x={180} y={145} textAnchor="middle" fill="#ffd700" fontSize={12} fontFamily="Noto Sans SC">变换后</text>
      <text x={130} y={160} textAnchor="middle" fill="#999" fontSize={11} fontFamily="Noto Sans SC">
        行列式 = 面积缩放因子
      </text>
    </svg>
  );
};
