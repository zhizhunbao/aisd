// ═══════════════════════════════════════════════════════════
// 积木详情页 — 预览 + 信息面板 + 评审评分
// BlockDetail — Preview + info panel + rating review
// ═══════════════════════════════════════════════════════════

import { MGMT } from '@/theme'
import { Badge, StarRating } from '@/components/ui'
import { BlockPreview } from '@/components/BlockPreview'
import { useNav } from '@/App'
import { BLOCK_CATEGORIES, type BlockMeta } from '@blocks/catalog'

export function BlockDetail({ blockName }: { blockName: string }) {
  const { navigate } = useNav()

  // 查找积木
  let block: (BlockMeta & { _cat: typeof BLOCK_CATEGORIES[number] }) | null = null
  for (const cat of BLOCK_CATEGORIES) {
    const found = cat.blocks.find((b) => b.name === blockName)
    if (found) { block = { ...found, _cat: cat }; break }
  }

  if (!block) {
    return (
      <div style={{ padding: MGMT.sp.xl, textAlign: 'center', color: MGMT.grayLight }}>
        <div style={{ fontSize: 48, marginBottom: 12 }}>❓</div>
        <div>积木 "{blockName}" 未找到</div>
        <button onClick={() => navigate({ page: 'blocks' })}
          style={{ marginTop: MGMT.sp.md, background: MGMT.bgCard, border: `1px solid ${MGMT.border}`, borderRadius: MGMT.radius.sm, padding: '8px 16px', color: MGMT.white, cursor: 'pointer', fontFamily: MGMT.fontFamily }}>
          ← 返回目录
        </button>
      </div>
    )
  }

  return (
    <div style={{ padding: MGMT.sp.xl }}>
      {/* 面包屑 */}
      <div style={{ marginBottom: MGMT.sp.lg, display: 'flex', alignItems: 'center', gap: MGMT.sp.sm }}>
        <span onClick={() => navigate({ page: 'blocks' })} style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, cursor: 'pointer' }}>← 积木目录</span>
        <span style={{ color: MGMT.gray }}>·</span>
        <span style={{ fontSize: MGMT.fontSize.small, color: block._cat.color }}>{block._cat.icon} {block._cat.name}</span>
      </div>

      {/* 标题 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.md, marginBottom: MGMT.sp.xl }}>
        <h1 style={{ fontSize: MGMT.fontSize.h1, fontWeight: 800, fontFamily: MGMT.codeFontFamily }}>{block.name}</h1>
        <Badge status={block.status} />
        {block.cmType && (
          <span style={{ fontSize: MGMT.fontSize.tiny, padding: '3px 8px', borderRadius: 4, background: `${MGMT.purple}18`, color: MGMT.purple }}>{block.cmType}</span>
        )}
      </div>

      <div style={{ display: 'flex', gap: MGMT.sp.xl }}>
        {/* 左侧：预览 + 信息 */}
        <div style={{ flex: 1 }}>
          {/* 预览区 */}
          <div style={{
            background: MGMT.bgCard, borderRadius: MGMT.radius.lg,
            border: `1px solid ${MGMT.border}`, aspectRatio: '16/9',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            marginBottom: MGMT.sp.md, overflow: 'hidden',
          }}>
            <BlockPreview blockName={block.name} />
          </div>

          {/* 描述 */}
          <div style={{ fontSize: MGMT.fontSize.body, color: MGMT.dimWhite, lineHeight: 1.6, marginBottom: MGMT.sp.lg }}>
            {block.description}
          </div>

          {/* Props 接口 */}
          <div style={{ marginBottom: MGMT.sp.lg }}>
            <h3 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 600, marginBottom: MGMT.sp.sm }}>📦 Props</h3>
            <div style={{
              background: MGMT.bgCard, borderRadius: MGMT.radius.md, padding: MGMT.sp.md,
              border: `1px solid ${MGMT.border}`, fontFamily: MGMT.codeFontFamily,
              fontSize: MGMT.fontSize.code, color: MGMT.dimWhite, lineHeight: 1.6, whiteSpace: 'pre-wrap',
            }}>
              {block.props}
            </div>
          </div>

          {/* 文件路径 */}
          <div>
            <h3 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 600, marginBottom: MGMT.sp.sm }}>📂 文件</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.sm, padding: `${MGMT.sp.xs}px 0`, fontSize: MGMT.fontSize.small }}>
              <span style={{ color: MGMT.gray }}>📄</span>
              <span style={{ fontFamily: MGMT.codeFontFamily, color: MGMT.dimWhite }}>src/blocks/{block.file}</span>
            </div>
          </div>
        </div>

        {/* 右侧：评审 */}
        <div style={{ width: 320, minWidth: 320 }}>
          <div style={{ background: MGMT.bgCard, borderRadius: MGMT.radius.lg, border: `1px solid ${MGMT.border}`, padding: MGMT.sp.lg }}>
            <h3 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 700, marginBottom: MGMT.sp.md }}>⭐ 评审</h3>
            {block.rating ? (
              <>
                <StarRating label="Mayer" value={block.rating.mayer} />
                <StarRating label="CRAP" value={block.rating.crap} />
                <StarRating label="动画" value={block.rating.animation} />
                <StarRating label="灵活性" value={block.rating.flexibility} />
                <StarRating label="代码" value={block.rating.codeQuality} />
                <div style={{ borderTop: `1px solid ${MGMT.border}`, marginTop: MGMT.sp.md, paddingTop: MGMT.sp.md, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: MGMT.fontSize.body, fontWeight: 700 }}>总分</span>
                  <span style={{ fontSize: 28, fontWeight: 800, color: block.rating.total >= 7 ? MGMT.green : MGMT.red, fontFamily: 'Inter, sans-serif' }}>{block.rating.total}/10</span>
                </div>
                {block.rating.notes && (
                  <div style={{ marginTop: MGMT.sp.md, fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, lineHeight: 1.5, fontStyle: 'italic' }}>💬 {block.rating.notes}</div>
                )}
                {block.rating.lastReviewed && (
                  <div style={{ marginTop: MGMT.sp.sm, fontSize: MGMT.fontSize.tiny, color: MGMT.gray }}>
                    🕐 评审于 {block.rating.lastReviewed}
                  </div>
                )}
              </>
            ) : (
              <div style={{ textAlign: 'center', color: MGMT.grayLight, padding: MGMT.sp.lg }}>
                <div style={{ fontSize: 32, marginBottom: MGMT.sp.sm }}>📋</div>
                <div style={{ fontSize: MGMT.fontSize.small }}>{block.status === 'todo' ? '积木尚未实现' : '尚未评审'}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
