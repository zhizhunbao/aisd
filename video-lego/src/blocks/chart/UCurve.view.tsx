// ═══════════════════════════════════════════════════════════
// UCurve — 纯视觉层（零 Remotion 依赖）
// UCurve — Pure visual layer (zero Remotion deps)
//
// 动画参数通过 ChartAnimProps 注入
// 不传动画参数 → 显示完整静态图
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { THEME } from '../../lib/video-theme';
import type { UCurveData } from '../../lib/types';
import type { ChartAnimProps } from '../../lib/anim-types';

export const UCurveView: React.FC<UCurveData & ChartAnimProps> = ({
  points,
  xLabel,
  yLabel,
  zones = [],
  bestPoint,
  source,
  // 动画参数，默认值 = 完整静态显示
  axisOpacity = 1,
  visiblePointCount,
  zoneOpacity = 1,
  bestOpacity = 1,
  bestScale = 1,
}) => {
  const CHART = { x: 80, y: 40, w: 800, h: 480, padB: 70, padL: 70 };

  const xs = points.map((p) => p.x);
  const ys = points.map((p) => p.y);
  const xMin = Math.min(...xs);
  const xMax = Math.max(...xs);
  const yMin = Math.min(...ys) * 0.9;
  const yMax = Math.max(...ys) * 1.1;

  const toX = (x: number) =>
    CHART.x + CHART.padL + ((x - xMin) / (xMax - xMin)) * (CHART.w - CHART.padL);
  const toY = (y: number) =>
    CHART.y + CHART.h - CHART.padB - ((y - yMin) / (yMax - yMin)) * (CHART.h - CHART.padB - 20);

  const visiblePts = visiblePointCount !== undefined
    ? Math.min(visiblePointCount, points.length)
    : points.length;

  const pathD = points
    .slice(0, visiblePts)
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${toX(p.x)} ${toY(p.y)}`)
    .join(' ');

  return (
    <div style={{ position: 'relative', width: '100%' }}>
      {source && (
        <div
          style={{
            position: 'absolute', top: 4, right: 8,
            color: THEME.gray, fontSize: 13,
            fontFamily: THEME.fontFamily, opacity: 0.5,
          }}
        >
          📚 {source}
        </div>
      )}

      <svg
        width="100%"
        height="100%"
        viewBox={`${CHART.x} ${CHART.y} ${CHART.w + 40} ${CHART.h + 20}`}
        style={{ maxHeight: 500 }}
      >
        {/* 坐标轴 Axes */}
        <g opacity={axisOpacity}>
          <line
            x1={toX(xMin)} y1={toY(yMin)} x2={toX(xMax)} y2={toY(yMin)}
            stroke={THEME.gray} strokeWidth="2" opacity="0.5"
          />
          <line
            x1={toX(xMin)} y1={toY(yMin)} x2={toX(xMin)} y2={toY(yMax)}
            stroke={THEME.gray} strokeWidth="2" opacity="0.5"
          />
          <text
            x={toX((xMin + xMax) / 2)} y={toY(yMin) + 50}
            fill={THEME.dimWhite} fontSize="20" textAnchor="middle"
            fontFamily={THEME.fontFamily}
          >
            {xLabel}
          </text>
          <foreignObject x={toX(xMin) - 65} y={toY((yMin + yMax) / 2) - 40} width="40" height="80">
            <div
              style={{
                color: THEME.dimWhite, fontSize: 18,
                fontFamily: THEME.fontFamily,
                writingMode: 'vertical-rl' as const,
                textAlign: 'center',
              }}
            >
              {yLabel}
            </div>
          </foreignObject>
        </g>

        {/* 区域标注 Zones */}
        {zones.map((zone, zi) => (
          <g key={zi} opacity={zoneOpacity * 0.15}>
            <rect
              x={toX(zone.start)} y={toY(yMax)}
              width={toX(zone.end) - toX(zone.start)}
              height={toY(yMin) - toY(yMax)}
              fill={zone.color} rx="4"
            />
            <text
              x={toX((zone.start + zone.end) / 2)} y={toY(yMax) + 20}
              fill={zone.color} fontSize="22" fontWeight="bold" textAnchor="middle"
              fontFamily={THEME.fontFamily} opacity={zoneOpacity}
            >
              {zone.label}
            </text>
          </g>
        ))}

        {/* 曲线 Curve */}
        {visiblePts > 1 && (
          <path d={pathD} fill="none" stroke={THEME.gold} strokeWidth="3.5" strokeLinecap="round" />
        )}

        {/* 散点 Dots */}
        {points.slice(0, visiblePts).map((p, i) => (
          <circle key={i} cx={toX(p.x)} cy={toY(p.y)} r="3.5" fill={THEME.gold} opacity={0.6} />
        ))}

        {/* 最优点标记 Best point marker */}
        {bestPoint && bestOpacity > 0 && (() => {
          const bp = points.find((p) => p.x === bestPoint.x) || points[0];
          const safeBestScale = Math.max(0.01, bestScale);
          return (
            <g
              opacity={bestOpacity}
              transform={`translate(${toX(bp.x)}, ${toY(bp.y)}) scale(${safeBestScale})`}
            >
              <line
                x1="0" y1="0" x2="0" y2={toY(yMin) - toY(bp.y)}
                stroke={THEME.gold} strokeWidth="1.5" strokeDasharray="4 3" opacity="0.5"
              />
              <text x="0" y="-5" fill={THEME.gold} fontSize="28" textAnchor="middle">★</text>
              <text
                x="0" y="-35" fill={THEME.gold} fontSize="20" fontWeight="bold"
                textAnchor="middle" fontFamily={THEME.fontFamily}
              >
                {bestPoint.annotation}
              </text>
            </g>
          );
        })()}
      </svg>
    </div>
  );
};
