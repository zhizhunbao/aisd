// 正交图解 — 90° 向量 + 内积为零
import React from 'react';

export const OrthogonalDiagram: React.FC = () => {
  const cx = 120;
  const cy = 100;

  return (
    <svg width={240} height={170} viewBox="0 0 240 170">
      {/* 坐标轴（淡色） */}
      <line x1={20} y1={cy} x2={220} y2={cy} stroke="rgba(255,255,255,0.1)" strokeWidth={1} />
      <line x1={cx} y1={15} x2={cx} y2={155} stroke="rgba(255,255,255,0.1)" strokeWidth={1} />

      {/* 向量 u（水平） */}
      <line x1={cx} y1={cy} x2={200} y2={cy} stroke="#4ea8de" strokeWidth={2.5} />
      <polygon points="200,100 192,95 192,105" fill="#4ea8de" />
      <text x={205} y={105} fill="#4ea8de" fontSize={16} fontFamily="Inter" fontWeight="bold">u</text>

      {/* 向量 v（垂直） */}
      <line x1={cx} y1={cy} x2={cx} y2={30} stroke="#2ecc71" strokeWidth={2.5} />
      <polygon points="120,30 115,38 125,38" fill="#2ecc71" />
      <text x={128} y={30} fill="#2ecc71" fontSize={16} fontFamily="Inter" fontWeight="bold">v</text>

      {/* 直角标记 */}
      <polyline
        points={`${cx + 12},${cy} ${cx + 12},${cy - 12} ${cx},${cy - 12}`}
        fill="none"
        stroke="#ffd700"
        strokeWidth={1.5}
      />

      {/* 标注 */}
      <text x={cx} y={158} textAnchor="middle" fill="#ffd700" fontSize={13} fontFamily="Inter">
        u · v = 0
      </text>
    </svg>
  );
};
