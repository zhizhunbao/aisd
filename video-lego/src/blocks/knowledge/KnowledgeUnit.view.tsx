// ═══════════════════════════════════════════════════════════
// KnowledgeUnit — 静态视图（管理 UI 预览 / 无 Remotion 依赖）
// KnowledgeUnit — Static view (management UI / no Remotion deps)
//
// 一屏展示一个概念的 6 个维度：
// 中文名 → 英文名 → 别名 → 图解 → 公式 → 释义
// ═══════════════════════════════════════════════════════════

import React from 'react';
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';
import type { KnowledgeUnitData } from '../../lib/types';
import { DIAGRAM_REGISTRY } from './diagrams';

interface KnowledgeUnitViewProps extends KnowledgeUnitData {
  containerStyle?: React.CSSProperties;
  /** 各元素的独立 style（动画注入用） */
  zhNameStyle?: React.CSSProperties;
  enNameStyle?: React.CSSProperties;
  aliasesStyle?: React.CSSProperties;
  diagramStyle?: React.CSSProperties;
  formulaStyle?: React.CSSProperties;
  explanationStyle?: React.CSSProperties;
}

export const KnowledgeUnitView: React.FC<KnowledgeUnitViewProps> = ({
  zhName,
  enName,
  aliases,
  formula,
  formulaLabel,
  diagram,
  explanation,
  color = '#f0f0f0',
  containerStyle,
  zhNameStyle,
  enNameStyle,
  aliasesStyle,
  diagramStyle,
  formulaStyle,
  explanationStyle,
}) => {
  const DiagramComponent = diagram ? DIAGRAM_REGISTRY[diagram] : null;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 12,
        width: '100%',
        maxWidth: 1600,
        ...containerStyle,
      }}
    >
      {/* ══════ ① 中文名（主视觉）══════ */}
      <div
        style={{
          fontSize: 80,
          fontWeight: 'bold',
          color,
          fontFamily: 'Noto Sans SC, sans-serif',
          letterSpacing: 8,
          textShadow: '0 2px 20px rgba(0,0,0,0.5)',
          ...zhNameStyle,
        }}
      >
        {zhName}
      </div>

      {/* ══════ ② 英文名 ══════ */}
      <div
        style={{
          fontSize: 36,
          color: '#aaaaaa',
          fontFamily: 'Inter, sans-serif',
          fontWeight: 300,
          letterSpacing: 3,
          marginTop: -4,
          ...enNameStyle,
        }}
      >
        {enName}
      </div>

      {/* ══════ ③ 别名 ══════ */}
      {aliases && aliases.length > 0 && (
        <div
          style={{
            fontSize: 22,
            color: '#777777',
            fontFamily: 'Noto Sans SC, sans-serif',
            marginTop: 2,
            ...aliasesStyle,
          }}
        >
          也叫：{aliases.join(' / ')}
        </div>
      )}

      {/* ══════ ④ 图解 + ⑤ 公式（水平排列）══════ */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 60,
          marginTop: 20,
          width: '100%',
        }}
      >
        {/* 图解 */}
        {DiagramComponent && (
          <div
            style={{
              flexShrink: 0,
              ...diagramStyle,
            }}
          >
            <DiagramComponent />
          </div>
        )}

        {/* 公式卡片 */}
        {formula && (
          <div
            style={{
              backgroundColor: 'rgba(255, 215, 0, 0.06)',
              border: '1.5px solid rgba(255, 215, 0, 0.25)',
              borderRadius: 16,
              padding: '24px 40px',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 8,
              ...formulaStyle,
            }}
          >
            <div style={{ fontSize: 38 }}>
              <BlockMath math={`\\color{#ffd700}{${formula}}`} />
            </div>
            {formulaLabel && (
              <div
                style={{
                  color: '#999999',
                  fontSize: 18,
                  fontFamily: 'Noto Sans SC, sans-serif',
                }}
              >
                {formulaLabel}
              </div>
            )}
          </div>
        )}
      </div>

      {/* ══════ ⑥ 一句话释义 ══════ */}
      <div
        style={{
          fontSize: 28,
          color: '#e0e0e0',
          fontFamily: 'Noto Sans SC, sans-serif',
          marginTop: 20,
          textAlign: 'center',
          lineHeight: 1.6,
          maxWidth: 900,
          padding: '8px 20px',
          borderLeft: '3px solid rgba(78, 168, 222, 0.4)',
          backgroundColor: 'rgba(78, 168, 222, 0.05)',
          borderRadius: 8,
          ...explanationStyle,
        }}
      >
        {explanation}
      </div>
    </div>
  );
};
