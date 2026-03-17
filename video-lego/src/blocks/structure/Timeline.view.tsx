// ═══════════════════════════════════════════════════════════
// Timeline — 纯视觉层（垂直时间线）
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';
import type { TimelineData } from '../../lib/types';
import type { StaggerAnimProps } from '../../lib/anim-types';

export const TimelineView: React.FC<TimelineData & StaggerAnimProps> = ({
  events,
  containerStyle,
  getItemStyle,
}) => {
  return (
    <div
      style={{
        display: 'flex', flexDirection: 'column', gap: 0,
        width: '90%', position: 'relative',
        ...containerStyle,
      }}
    >
      {/* 竖线 */}
      <div style={{
        position: 'absolute', left: 20, top: 0, bottom: 0, width: 3,
        background: `linear-gradient(${THEME.gold}80, ${THEME.blue}80)`, borderRadius: 2,
      }} />

      {events.map((evt, ei) => {
        const itemStyle = getItemStyle?.(ei);

        return (
          <div key={ei} style={{
            display: 'flex', alignItems: 'flex-start', gap: 16,
            paddingLeft: 8, marginBottom: 20,
            ...itemStyle,
          }}>
            <div style={{
              width: 28, height: 28, borderRadius: '50%',
              backgroundColor: evt.color || THEME.gold,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 14, flexShrink: 0, marginTop: 4,
            }}>
              {evt.icon || '•'}
            </div>
            <div>
              <div style={{ color: evt.color || THEME.gold, fontSize: 22, fontWeight: 'bold', fontFamily: THEME.fontFamily }}>
                {evt.year}
              </div>
              <div style={{ color: THEME.dimWhite, fontSize: 20, fontFamily: THEME.fontFamily, marginTop: 4, lineHeight: 1.5 }}>
                {evt.text}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
