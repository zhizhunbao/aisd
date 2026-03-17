// ═══════════════════════════════════════════════════════════
// FormulaDerivation — 纯视觉层（零 Remotion 依赖）
// FormulaDerivation — Pure visual layer (zero Remotion deps)
// ═══════════════════════════════════════════════════════════

import React from 'react';
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';
import { THEME } from '../../lib/video-theme';
import type { FormulaDerivationData } from '../../lib/types';
import type { StaggerAnimProps } from '../../lib/anim-types';

export const FormulaDerivationView: React.FC<FormulaDerivationData & StaggerAnimProps> = ({
  steps,
  source,
  containerStyle,
  getItemStyle,
}) => {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: 12,
        width: '92%',
        ...containerStyle,
      }}
    >
      {/* 来源标注 Source citation */}
      {source && (
        <div
          style={{
            color: THEME.gray,
            fontSize: 14,
            fontFamily: THEME.fontFamily,
            textAlign: 'right',
            opacity: 0.6,
            marginBottom: 4,
          }}
        >
          📚 {source}
        </div>
      )}

      {steps.map((step, i) => {
        const isHighlighted = step.highlight;
        const formulaColor = isHighlighted ? THEME.gold : THEME.white;
        const bgColor = isHighlighted ? `${THEME.gold}10` : THEME.bgLight;
        const borderColor = isHighlighted ? `${THEME.gold}50` : `${THEME.gray}20`;
        const itemStyle = getItemStyle?.(i);

        return (
          <div
            key={i}
            style={{
              backgroundColor: bgColor,
              borderRadius: 14,
              padding: '20px 24px',
              border: `1px solid ${borderColor}`,
              borderLeft: isHighlighted ? `4px solid ${THEME.gold}` : `4px solid transparent`,
              ...itemStyle,
            }}
          >
            {/* 步骤编号 */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
              <span
                style={{
                  color: isHighlighted ? THEME.gold : THEME.gray,
                  fontSize: 14,
                  fontFamily: THEME.fontFamily,
                  opacity: 0.7,
                }}
              >
                Step {i + 1}
              </span>
              {step.annotation && (
                <span
                  style={{
                    color: isHighlighted ? THEME.gold : THEME.dimWhite,
                    fontSize: 16,
                    fontFamily: THEME.fontFamily,
                  }}
                >
                  {step.annotation}
                </span>
              )}
            </div>

            {/* 公式 */}
            <div style={{ fontSize: 36, textAlign: 'center' }}>
              <BlockMath math={`\\color{${formulaColor}}{${step.latex}}`} />
            </div>
          </div>
        );
      })}
    </div>
  );
};
