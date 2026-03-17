// ═══════════════════════════════════════════════════════════
// 素材详情页 — 预览 + 元数据 + 来源引用 + 可绑定积木
// AssetDetail — Preview + metadata + sources + compatible blocks
// ═══════════════════════════════════════════════════════════

import { MGMT } from '@/theme'
import { Card } from '@/components/ui'
import { AssetPreview } from '@/components/AssetPreview'
import { useNav } from '@/App'
import { getCategoryMeta, getSubCategoryName } from '@/lib/asset-types'
import { DEMO_ASSETS } from '@/data/demo-assets'

const SOURCE_ICONS: Record<string, string> = {
  textbook: '📕', paper: '📄', wikipedia: '🌐',
  documentation: '📋', course: '🎓', original: '✍️',
}

const SOURCE_LABELS: Record<string, string> = {
  textbook: '教科书', paper: '论文', wikipedia: 'Wikipedia',
  documentation: '文档', course: '课程', original: '原创',
}

export function AssetDetail({ assetId }: { assetId: string }) {
  const { navigate } = useNav()
  const asset = DEMO_ASSETS.find(a => a.id === assetId)

  if (!asset) {
    return (
      <div style={{ padding: MGMT.sp.xl, textAlign: 'center', color: MGMT.grayLight }}>
        <div style={{ fontSize: 48, marginBottom: 12 }}>❓</div>
        <div>素材 "{assetId}" 未找到</div>
        <button onClick={() => navigate({ page: 'assets' })}
          style={{ marginTop: MGMT.sp.md, background: MGMT.bgCard, border: `1px solid ${MGMT.border}`, borderRadius: MGMT.radius.sm, padding: '8px 16px', color: MGMT.white, cursor: 'pointer', fontFamily: MGMT.fontFamily }}>
          ← 返回素材库
        </button>
      </div>
    )
  }

  const catMeta = getCategoryMeta(asset.category)

  return (
    <div style={{ padding: MGMT.sp.xl }}>
      {/* 面包屑 */}
      <div style={{ marginBottom: MGMT.sp.lg, display: 'flex', alignItems: 'center', gap: MGMT.sp.sm }}>
        <span onClick={() => navigate({ page: 'assets' })} style={{ fontSize: MGMT.fontSize.small, color: MGMT.dimWhite, cursor: 'pointer' }}>← 素材库</span>
        <span style={{ color: MGMT.gray }}>·</span>
        <span style={{ fontSize: MGMT.fontSize.small, color: catMeta?.color }}>{catMeta?.icon} {catMeta?.name}</span>
        {asset.subCategory && catMeta && (
          <>
            <span style={{ color: MGMT.gray }}>·</span>
            <span style={{ fontSize: MGMT.fontSize.small, color: catMeta.color }}>{getSubCategoryName(asset.category, asset.subCategory)}</span>
          </>
        )}
      </div>

      {/* 标题 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: MGMT.sp.md, marginBottom: MGMT.sp.xl, flexWrap: 'wrap' }}>
        <h1 style={{ fontSize: MGMT.fontSize.h1, fontWeight: 800 }}>{asset.name}</h1>
        <span style={{ fontSize: MGMT.fontSize.small, padding: '3px 10px', borderRadius: 6, background: `${catMeta?.color}15`, color: catMeta?.color, fontWeight: 600 }}>
          {catMeta?.icon} {catMeta?.name}
        </span>
        {asset.subCategory && catMeta && (
          <span style={{ fontSize: 11, padding: '2px 8px', borderRadius: 4, background: `${catMeta.color}10`, color: catMeta.color }}>
            {getSubCategoryName(asset.category, asset.subCategory)}
          </span>
        )}
      </div>

      <div style={{ display: 'flex', gap: MGMT.sp.xl }}>
        {/* 左侧：预览 */}
        <div style={{ flex: 1 }}>
          <Card>
            <div style={{
              aspectRatio: '16/9', display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: 'linear-gradient(180deg, rgba(26,26,46,0.95), rgba(15,15,30,0.95))',
              borderRadius: MGMT.radius.lg, overflow: 'hidden',
            }}>
              <div style={{ transform: 'scale(1.3)', transformOrigin: 'center' }}>
                <AssetPreview asset={asset} />
              </div>
            </div>
          </Card>

          {/* 原始数据 */}
          <div style={{ marginTop: MGMT.sp.lg }}>
            <h3 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 600, marginBottom: MGMT.sp.sm }}>📋 原始数据</h3>
            <pre style={{
              background: MGMT.bgCard, borderRadius: MGMT.radius.md, padding: MGMT.sp.md,
              border: `1px solid ${MGMT.border}`, fontFamily: MGMT.codeFontFamily,
              fontSize: 12, color: MGMT.dimWhite, lineHeight: 1.5, whiteSpace: 'pre-wrap',
              maxHeight: 300, overflow: 'auto',
            }}>
              {JSON.stringify(asset.content.data, null, 2)}
            </pre>
          </div>
        </div>

        {/* 右侧：元数据 */}
        <div style={{ width: 340, minWidth: 340 }}>
          <Card>
            <div style={{ padding: MGMT.sp.lg }}>
              <h3 style={{ fontSize: MGMT.fontSize.h3, fontWeight: 700, marginBottom: MGMT.sp.md }}>📦 素材信息</h3>

              <InfoRow label="ID" value={asset.id} />
              <InfoRow label="分类" value={`${catMeta?.icon} ${catMeta?.name}`} />
              {asset.subCategory && catMeta && <InfoRow label="子分类" value={getSubCategoryName(asset.category, asset.subCategory)} />}
              {asset.course && <InfoRow label="课程" value={asset.course} />}
              <InfoRow label="创建" value={asset.createdAt} />

              {/* 标签 */}
              <div style={{ marginTop: MGMT.sp.md }}>
                <div style={{ fontSize: MGMT.fontSize.tiny, color: MGMT.gray, marginBottom: 6 }}>🏷️ 标签</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                  {asset.tags.map(tag => (
                    <span key={tag} style={{ fontSize: 12, padding: '2px 8px', borderRadius: 4, background: `${MGMT.white}08`, color: MGMT.dimWhite }}>
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* 来源引用 */}
              <div style={{ marginTop: MGMT.sp.lg, borderTop: `1px solid ${MGMT.border}`, paddingTop: MGMT.sp.md }}>
                <div style={{ fontSize: MGMT.fontSize.tiny, color: MGMT.gray, marginBottom: 8 }}>📚 来源引用 ({asset.sources.length})</div>
                {asset.sources.map((s, i) => (
                  <div key={i} style={{
                    padding: '8px 10px', marginBottom: 6, borderRadius: MGMT.radius.sm,
                    background: `${MGMT.white}04`, border: `1px solid ${MGMT.border}`,
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
                      <span style={{ fontSize: 14 }}>{SOURCE_ICONS[s.type] || '📎'}</span>
                      <span style={{ fontSize: 11, padding: '1px 5px', borderRadius: 3, background: `${MGMT.white}08`, color: MGMT.grayLight }}>
                        {SOURCE_LABELS[s.type] || s.type}
                      </span>
                      {s.year && <span style={{ fontSize: 11, color: MGMT.gray }}>{s.year}</span>}
                    </div>
                    <div style={{ fontSize: 12, fontWeight: 600, color: MGMT.dimWhite, fontFamily: MGMT.fontFamily }}>{s.title}</div>
                    {s.author && <div style={{ fontSize: 11, color: MGMT.gray, fontFamily: MGMT.fontFamily }}>{s.author}</div>}
                    <div style={{ display: 'flex', gap: 6, marginTop: 3, fontSize: 11, color: MGMT.grayLight }}>
                      {s.chapter && <span>📖 {s.chapter}</span>}
                      {s.page && <span>p.{s.page}</span>}
                      {s.url && <span style={{ color: MGMT.blue }}>🔗 链接</span>}
                    </div>
                  </div>
                ))}
              </div>

              {/* 可绑定积木 */}
              {asset.compatibleBlocks && asset.compatibleBlocks.length > 0 && (
                <div style={{ marginTop: MGMT.sp.lg, borderTop: `1px solid ${MGMT.border}`, paddingTop: MGMT.sp.md }}>
                  <div style={{ fontSize: MGMT.fontSize.tiny, color: MGMT.gray, marginBottom: 8 }}>🧱 可绑定积木</div>
                  {asset.compatibleBlocks.map(blockName => (
                    <div key={blockName}
                      onClick={() => navigate({ page: 'block-detail', blockName })}
                      style={{
                        padding: '8px 12px', marginBottom: 4, borderRadius: MGMT.radius.sm,
                        background: `${MGMT.white}04`, cursor: 'pointer', fontFamily: MGMT.codeFontFamily,
                        fontSize: MGMT.fontSize.small, color: MGMT.dimWhite,
                        border: `1px solid ${MGMT.border}`, transition: 'all 0.15s',
                      }}
                    >
                      🧱 {blockName}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: MGMT.fontSize.small }}>
      <span style={{ color: MGMT.gray }}>{label}</span>
      <span style={{ color: MGMT.dimWhite, fontFamily: MGMT.codeFontFamily }}>{value}</span>
    </div>
  )
}
