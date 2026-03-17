// ═══════════════════════════════════════════════════════════
// 场景渲染器 — 根据场景数据自动选积木
// SceneRenderer — Auto-selects blocks from registry based on scene data
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { BLOCK_REGISTRY } from '@blocks/index';
import { SplitLayout } from '../layouts/SplitLayout';
import type { SceneData } from '@lego/types';

export const SceneRenderer: React.FC<{ scene: SceneData }> = ({ scene }) => {
  // 根据 layout 选布局（目前只有 split，后续扩展）
  switch (scene.layout) {
    case 'split':
    default:
      return (
        <SplitLayout
          act={scene.act}
          title={scene.title}
          titleColor={scene.titleColor}
          points={scene.points}
          conclusion={scene.conclusion}
        >
          {scene.visuals.map((v, i) => {
            const BlockComponent = BLOCK_REGISTRY[v.block];

            if (!BlockComponent) {
              // 找不到积木 → 显示占位提示
              return (
                <div
                  key={i}
                  style={{
                    color: '#e74c3c',
                    fontSize: 20,
                    fontFamily: 'monospace',
                    padding: 20,
                    border: '1px dashed #e74c3c',
                    borderRadius: 8,
                  }}
                >
                  ⚠️ Block "{v.block}" not found in registry
                </div>
              );
            }

            return <BlockComponent key={i} {...v.data} />;
          })}
        </SplitLayout>
      );

    // TODO: 后续扩展
    // case 'fullscreen':
    //   return <FullScreenLayout ...>;
    // case 'three-column':
    //   return <ThreeColumnLayout ...>;
  }
};
