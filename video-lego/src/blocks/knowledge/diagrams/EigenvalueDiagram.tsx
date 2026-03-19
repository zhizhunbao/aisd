// 特征值图解 — 向量拉伸方向不变
import React from 'react';

export const EigenvalueDiagram: React.FC = () => {
  return (
    <svg width={240} height={180} viewBox="0 0 240 180">
      {/* 坐标轴 */}
      <line x1={30} y1={150} x2={220} y2={150} stroke="rgba(255,255,255,0.15)" strokeWidth={1} />
      <line x1={120} y1={20} x2={120} y2={160} stroke="rgba(255,255,255,0.15)" strokeWidth={1} />

      {/* 原始向量 v（短，淡色） */}
      <line x1={120} y1={150} x2={170} y2={80} stroke="rgba(255,255,255,0.3)" strokeWidth={2} />
      <circle cx={170} cy={80} r={3} fill="rgba(255,255,255,0.3)" />
      <text x={175} y={78} fill="#888" fontSize={14} fontFamily="Inter">v</text>

      {/* 特征向量 Av = λv（长，同方向，亮色） */}
      <line x1={120} y1={150} x2={195} y2={40} stroke="#ffd700" strokeWidth={2.5} />
      <polygon points="195,40 189,50 199,48" fill="#ffd700" />
      <text x={200} y={38} fill="#ffd700" fontSize={14} fontFamily="Inter" fontWeight="bold">Av = λv</text>

      {/* 非特征向量（方向改变） */}
      <line x1={120} y1={150} x2={60} y2={100} stroke="rgba(255,255,255,0.2)" strokeWidth={1.5} strokeDasharray="4,3" />
      <line x1={120} y1={150} x2={45} y2={60} stroke="#e74c3c" strokeWidth={1.5} />
      <polygon points="45,60 52,68 48,70" fill="#e74c3c" />
      <text x={30} y={55} fill="#e74c3c" fontSize={12} fontFamily="Inter">方向变了</text>

      {/* 标注 */}
      <text x={160} y={172} fill="#ffd700" fontSize={12} fontFamily="Noto Sans SC">方向不变 ✓</text>
      <text x={30} y={172} fill="#e74c3c" fontSize={12} fontFamily="Noto Sans SC">方向变了 ✗</text>
    </svg>
  );
};
