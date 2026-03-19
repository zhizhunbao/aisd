// ═══════════════════════════════════════════════════════════
// ProgressBars — 纯视觉层
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';
import type { ProgressBarData } from '../../lib/types';
import type { StaggerAnimProps } from '../../lib/anim-types';

interface ProgressBarsViewProps extends StaggerAnimProps {
  bars: ProgressBarData[];
  /** 每条进度条的当前进度值（0-100），默认用 bar.value */
  getBarProgress?: (index: number) => number;
}

export const ProgressBarsView: React.FC<ProgressBarsViewProps> = ({
  bars,
  containerStyle,
  getItemStyle,
  getBarProgress,
}) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24, width: '90%', ...containerStyle }}>
      {bars.map((bar, bi) => {
        const progress = getBarProgress?.(bi) ?? bar.value;
        const itemStyle = getItemStyle?.(bi);

        return (
          <div key={bi} style={{ ...itemStyle }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <span style={{ color: THEME.dimWhite, fontSize: 20, fontFamily: THEME.fontFamily }}>
                {bar.label}
              </span>
              <span style={{ color: bar.color, fontSize: 22, fontWeight: 'bold', fontFamily: THEME.fontFamily }}>
                {bar.displayValue || `${Math.round(progress)}%`}
              </span>
            </div>
            <div style={{ height: 24, backgroundColor: THEME.bg, borderRadius: 12, overflow: 'hidden', border: `1px solid ${THEME.gray}30` }}>
              <div style={{
                width: `${progress}%`, height: '100%',
                background: `linear-gradient(90deg, ${bar.color}cc, ${bar.color})`,
                borderRadius: 12,
              }} />
            </div>
          </div>
        );
      })}
    </div>
  );
};
