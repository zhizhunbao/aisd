// 线性变换图解 — 网格变形可视化（单位正方形 → 平行四边形）
import React from 'react';

export const LinearTransformDiagram: React.FC = () => {
  // 原始网格（浅色）
  const gridLines: React.ReactNode[] = [];
  for (let i = 0; i <= 4; i++) {
    const x = 30 + i * 25;
    const y = 30 + i * 25;
    gridLines.push(
      <line key={`h${i}`} x1={30} y1={y} x2={130} y2={y} stroke="rgba(255,255,255,0.1)" strokeWidth={1} />,
      <line key={`v${i}`} x1={x} y1={30} x2={x} y2={130} stroke="rgba(255,255,255,0.1)" strokeWidth={1} />,
    );
  }

  // 变换后的平行四边形网格（亮色）
  // 变换矩阵 [[1.3, 0.4], [0.2, 1.1]] 应用到单位正方形
  const transform = (x: number, y: number): [number, number] => {
    return [150 + (1.3 * x + 0.4 * y) * 25, 30 + (0.2 * x + 1.1 * y) * 25];
  };

  const transformedLines: React.ReactNode[] = [];
  for (let i = 0; i <= 4; i++) {
    const [x1, y1] = transform(0, i);
    const [x2, y2] = transform(4, i);
    const [x3, y3] = transform(i, 0);
    const [x4, y4] = transform(i, 4);
    transformedLines.push(
      <line key={`th${i}`} x1={x1} y1={y1} x2={x2} y2={y2} stroke="rgba(78,168,222,0.3)" strokeWidth={1} />,
      <line key={`tv${i}`} x1={x3} y1={y3} x2={x4} y2={y4} stroke="rgba(78,168,222,0.3)" strokeWidth={1} />,
    );
  }

  return (
    <svg width={280} height={170} viewBox="0 0 290 170">
      {/* 原始网格 */}
      {gridLines}
      <rect x={30} y={30} width={100} height={100} fill="none" stroke="rgba(255,255,255,0.25)" strokeWidth={2} />

      {/* 箭头 */}
      <path d="M 135 80 L 148 80" stroke="#ffd700" strokeWidth={2} markerEnd="url(#arrowGold)" />
      <defs>
        <marker id="arrowGold" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
          <path d="M 0 0 L 8 4 L 0 8 Z" fill="#ffd700" />
        </marker>
      </defs>

      {/* 变换后网格 */}
      {transformedLines}
      {/* 变换后外框 */}
      {(() => {
        const [x0, y0] = transform(0, 0);
        const [x1, y1] = transform(4, 0);
        const [x2, y2] = transform(4, 4);
        const [x3, y3] = transform(0, 4);
        return (
          <polygon
            points={`${x0},${y0} ${x1},${y1} ${x2},${y2} ${x3},${y3}`}
            fill="none"
            stroke="#4ea8de"
            strokeWidth={2}
          />
        );
      })()}

      {/* 标签 */}
      <text x={80} y={155} textAnchor="middle" fill="#888" fontSize={13} fontFamily="Inter">原始</text>
      <text x={210} y={155} textAnchor="middle" fill="#4ea8de" fontSize={13} fontFamily="Inter">T(x)=Ax</text>
    </svg>
  );
};
