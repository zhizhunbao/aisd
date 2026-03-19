// 矩阵图解 — 网格数组可视化
import React from 'react';

export const MatrixDiagram: React.FC = () => {
  const cells = [
    ['a₁₁', 'a₁₂', 'a₁₃'],
    ['a₂₁', 'a₂₂', 'a₂₃'],
  ];
  const cellSize = 52;
  const gap = 4;
  const cols = 3;
  const rows = 2;
  const w = cols * (cellSize + gap) + 30;
  const h = rows * (cellSize + gap) + 30;

  return (
    <svg width={260} height={180} viewBox={`0 0 ${w} ${h}`}>
      {/* 左括号 */}
      <path
        d={`M 12 8 Q 4 8, 4 ${h / 2} Q 4 ${h - 8}, 12 ${h - 8}`}
        fill="none"
        stroke="#4ea8de"
        strokeWidth={3}
        strokeLinecap="round"
      />
      {/* 右括号 */}
      <path
        d={`M ${w - 12} 8 Q ${w - 4} 8, ${w - 4} ${h / 2} Q ${w - 4} ${h - 8}, ${w - 12} ${h - 8}`}
        fill="none"
        stroke="#4ea8de"
        strokeWidth={3}
        strokeLinecap="round"
      />
      {/* 单元格 */}
      {cells.map((row, r) =>
        row.map((val, c) => {
          const x = 20 + c * (cellSize + gap);
          const y = 15 + r * (cellSize + gap);
          return (
            <g key={`${r}-${c}`}>
              <rect
                x={x}
                y={y}
                width={cellSize}
                height={cellSize}
                rx={6}
                fill="rgba(78, 168, 222, 0.12)"
                stroke="rgba(78, 168, 222, 0.3)"
                strokeWidth={1}
              />
              <text
                x={x + cellSize / 2}
                y={y + cellSize / 2 + 5}
                textAnchor="middle"
                fill="#4ea8de"
                fontSize={16}
                fontFamily="Inter, sans-serif"
              >
                {val}
              </text>
            </g>
          );
        })
      )}
    </svg>
  );
};
