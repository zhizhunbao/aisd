// ═══════════════════════════════════════════════════════════
// ComparisonSplit — 纯视觉层（A vs B 对比）
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';
import type { ComparisonSplitData } from '../../lib/types';
import type { StaggerAnimProps } from '../../lib/anim-types';

export const ComparisonSplitView: React.FC<ComparisonSplitData & StaggerAnimProps> = ({
  left,
  right,
  containerStyle,
  getItemStyle,
}) => {
  return (
    <div style={{ display: 'flex', gap: 16, width: '95%', ...containerStyle }}>
      {[left, right].map((col, ci) => {
        const itemStyle = getItemStyle?.(ci);

        return (
          <div
            key={ci}
            style={{
              flex: 1,
              backgroundColor: THEME.bgLight,
              borderRadius: 16,
              padding: '24px 20px',
              borderTop: `4px solid ${col.color}`,
              textAlign: 'center',
              ...itemStyle,
            }}
          >
            <div style={{ fontSize: 40, marginBottom: 10 }}>{col.icon || ''}</div>
            <div style={{ color: col.color, fontSize: 32, fontWeight: 'bold', fontFamily: THEME.fontFamily, marginBottom: 6 }}>
              {col.value}
            </div>
            <div style={{ color: THEME.dimWhite, fontSize: 20, fontFamily: THEME.fontFamily, marginBottom: 12 }}>
              {col.label}
            </div>
            {col.subItems?.map((item, si) => (
              <div key={si} style={{ color: THEME.dimWhite, fontSize: 18, fontFamily: THEME.fontFamily, marginBottom: 6, opacity: 0.8, textAlign: 'left', paddingLeft: 12 }}>
                • {item}
              </div>
            ))}
          </div>
        );
      })}
    </div>
  );
};
