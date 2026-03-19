// ═══════════════════════════════════════════════════════════
// 积木注册表 — 所有乐高积木的统一入口
// Block Registry — Central registry of all Lego blocks
//
// Motion 版本（默认）→ Remotion 视频渲染
// View 版本 → 管理 UI 静态/自定义动画预览
// ═══════════════════════════════════════════════════════════

import type { BlockName } from '../lib/types';

// ──── Motion 版本（Remotion 动画）────
import { FormulaBlock } from './formula/FormulaBlock';
import { FormulaDerivation } from './formula/FormulaDerivation';
import { UCurve } from './chart/UCurve';
import { ComparisonSplit } from './structure/ComparisonSplit';
import { Timeline } from './structure/Timeline';
import { ProgressBars } from './data/ProgressBars';
import { StatCards } from './data/StatCards';
import { CodeBlock } from './data/CodeBlock';
import { ImageDisplay } from './data/ImageDisplay';
import { KnowledgeUnit } from './knowledge/KnowledgeUnit';

// ──── View 版本（纯视觉，零 Remotion 依赖）────
import { FormulaBlockView } from './formula/FormulaBlock';
import { FormulaDerivationView } from './formula/FormulaDerivation';
import { UCurveView } from './chart/UCurve';
import { ComparisonSplitView } from './structure/ComparisonSplit';
import { TimelineView } from './structure/Timeline';
import { ProgressBarsView } from './data/ProgressBars';
import { StatCardsView } from './data/StatCards';
import { CodeBlockView } from './data/CodeBlock';
import { ImageDisplayView } from './data/ImageDisplay';
import { KnowledgeUnitView } from './knowledge/KnowledgeUnit';

// ══════ Motion 注册表（Remotion 用）══════

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const BLOCK_REGISTRY: Record<string, React.ComponentType<any>> = {
  FormulaBlock,
  FormulaDerivation,
  UCurve,
  ComparisonSplit,
  Timeline,
  ProgressBars,
  StatCards,
  CodeBlock,
  ImageDisplay,
  KnowledgeUnit,
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function getBlock(name: BlockName): React.ComponentType<any> {
  const block = BLOCK_REGISTRY[name];
  if (!block) {
    console.warn(`[BlockRegistry] Block "${name}" not found. Available: ${Object.keys(BLOCK_REGISTRY).join(', ')}`);
  }
  return block;
}

// ══════ 导出 ══════

// Motion（默认，Remotion 用）
export {
  FormulaBlock,
  FormulaDerivation,
  UCurve,
  ComparisonSplit,
  Timeline,
  ProgressBars,
  StatCards,
  CodeBlock,
  ImageDisplay,
  KnowledgeUnit,
};

// View（纯视觉，管理 UI 用）
export {
  FormulaBlockView,
  FormulaDerivationView,
  UCurveView,
  ComparisonSplitView,
  TimelineView,
  ProgressBarsView,
  StatCardsView,
  CodeBlockView,
  ImageDisplayView,
  KnowledgeUnitView,
};
