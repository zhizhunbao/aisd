// ═══════════════════════════════════════════════════════════
// CodeBlock — 纯视觉层
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';
import type { CodeBlockData } from '../../lib/types';
import type { AnimProps } from '../../lib/anim-types';

export const CodeBlockView: React.FC<CodeBlockData & AnimProps> = ({
  code,
  label,
  color,
  containerStyle,
}) => {
  return (
    <div style={{
      backgroundColor: '#0d1117',
      borderRadius: 16, padding: '24px 20px',
      borderLeft: `4px solid ${color || THEME.blue}`,
      width: '90%',
      ...containerStyle,
    }}>
      {label && (
        <div style={{ color: color || THEME.blue, fontSize: 18, fontFamily: THEME.fontFamily, marginBottom: 14, fontWeight: 'bold' }}>
          {label}
        </div>
      )}
      <pre style={{ color: THEME.white, fontSize: THEME.fontSize.code, fontFamily: THEME.codeFontFamily, margin: 0, whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
        {code}
      </pre>
    </div>
  );
};
