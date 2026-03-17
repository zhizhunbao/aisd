// ═══════════════════════════════════════════════════════════
// FormulaBlock — 纯视觉层（零 Remotion 依赖）
// FormulaBlock — Pure visual layer (zero Remotion deps)
// ═══════════════════════════════════════════════════════════

import React from 'react';
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';
import { THEME } from '../../lib/video-theme';
import type { FormulaBlockData } from '../../lib/types';
import type { AnimProps } from '../../lib/anim-types';

export const FormulaBlockView: React.FC<FormulaBlockData & AnimProps> = ({
  latex,
  label,
  color,
  containerStyle,
}) => {
  const c = color || THEME.gold;

  return (
    <div
      style={{
        backgroundColor: THEME.bgLight,
        borderRadius: 20,
        padding: '32px 24px',
        border: `1px solid ${c}25`,
        width: '90%',
        ...containerStyle,
      }}
    >
      <div style={{ fontSize: 44, textAlign: 'center' }}>
        <BlockMath math={`\\color{${c}}{${latex}}`} />
      </div>
      {label && (
        <div
          style={{
            color: THEME.dimWhite,
            fontSize: 20,
            textAlign: 'center',
            marginTop: 12,
            fontFamily: THEME.fontFamily,
          }}
        >
          {label}
        </div>
      )}
    </div>
  );
};
