// ═══════════════════════════════════════════════════════════
// 图解注册表 — 知识单元可视化组件
// Diagram Registry — Visual components for KnowledgeUnit
//
// 每个图解是一个纯 React SVG 组件，200-300px 视口
// 使用 THEME 色系，可选内部动画
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { MatrixDiagram } from './MatrixDiagram';
import { LinearTransformDiagram } from './LinearTransformDiagram';
import { EigenvalueDiagram } from './EigenvalueDiagram';
import { DeterminantDiagram } from './DeterminantDiagram';
import { OrthogonalDiagram } from './OrthogonalDiagram';
import { BasisDiagram } from './BasisDiagram';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const DIAGRAM_REGISTRY: Record<string, React.ComponentType<any>> = {
  MatrixDiagram,
  LinearTransformDiagram,
  EigenvalueDiagram,
  DeterminantDiagram,
  OrthogonalDiagram,
  BasisDiagram,
};

export {
  MatrixDiagram,
  LinearTransformDiagram,
  EigenvalueDiagram,
  DeterminantDiagram,
  OrthogonalDiagram,
  BasisDiagram,
};
