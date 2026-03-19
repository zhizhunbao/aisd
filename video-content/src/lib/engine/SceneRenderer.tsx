// ═══════════════════════════════════════════════════════════
// 场景渲染器 — 根据场景数据自动选积木
// SceneRenderer — Auto-selects blocks from registry based on scene data
// ═══════════════════════════════════════════════════════════

import React from 'react';
import { BLOCK_REGISTRY } from '@blocks/index';
import { SplitLayout } from '../layouts/SplitLayout';
import { BlackboardLayout } from '@lego/layouts/BlackboardLayout';
import type { SceneData } from '@lego/types';

/** 渲染积木列表（共享逻辑） */
const renderVisuals = (visuals: SceneData['visuals']) =>
  visuals.map((v, i) => {
    const BlockComponent = BLOCK_REGISTRY[v.block];

    if (!BlockComponent) {
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
          ⚠️ Block &quot;{v.block}&quot; not found in registry
        </div>
      );
    }

    return <BlockComponent key={i} {...v.data} />;
  });

export const SceneRenderer: React.FC<{ scene: SceneData }> = ({ scene }) => {
  switch (scene.layout) {
    // ══════ 黑板快闪布局 ══════
    case 'blackboard':
      return (
        <BlackboardLayout
          act={scene.act}
          title={scene.title}
          titleColor={scene.titleColor}
          progress={scene.progress}
          pinnedItems={scene.pinnedItems}
        >
          {renderVisuals(scene.visuals)}
        </BlackboardLayout>
      );

    // ══════ 默认：左右分栏布局 ══════
    case 'landscape':
    case 'portrait':
    default:
      return (
        <SplitLayout
          act={scene.act}
          title={scene.title}
          titleColor={scene.titleColor}
          points={scene.points}
          conclusion={scene.conclusion}
        >
          {renderVisuals(scene.visuals)}
        </SplitLayout>
      );
  }
};
