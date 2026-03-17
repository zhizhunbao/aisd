// ═══════════════════════════════════════════════════════════
// ConclusionBanner — 结论横幅积木（纯视觉层）
// ConclusionBanner — Conclusion highlight block (view layer)
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';

interface ConclusionBannerViewProps {
  text: string;
  icon?: string;
}

export const ConclusionBannerView: React.FC<ConclusionBannerViewProps> = ({ text, icon }) => {
  if (!text) {
    return (
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        height: '100%', color: THEME.dimWhite, fontSize: 16,
        fontFamily: THEME.fontFamily,
      }}>
        (空结论)
      </div>
    );
  }

  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: '20px 32px', width: '100%', boxSizing: 'border-box',
    }}>
      <div style={{
        background: `linear-gradient(135deg, ${THEME.gold}18, ${THEME.gold}08)`,
        border: `1px solid ${THEME.gold}40`,
        borderRadius: 12, padding: '16px 24px',
        display: 'flex', alignItems: 'center', gap: 12,
        maxWidth: 600, width: '100%',
      }}>
        <span style={{ fontSize: 28, flexShrink: 0 }}>
          {icon || '⭐'}
        </span>
        <span style={{
          fontSize: 20, fontWeight: 700,
          color: THEME.gold, fontFamily: THEME.fontFamily,
          lineHeight: 1.4,
        }}>
          {text}
        </span>
      </div>
    </div>
  );
};
