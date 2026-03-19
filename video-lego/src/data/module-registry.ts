// ═══════════════════════════════════════════════════════════
// 模块注册表 — 数据驱动的模块 + 侧栏 + 布局配置
// Module Registry — data-driven module + sidebar + layout config
//
// SidebarNode 递归树，支持任意层级。
// 每个叶子节点可指定 layout (L1~L5) 来决定内容区布局。
// ═══════════════════════════════════════════════════════════

// ─── 布局类型 ───

export type LayoutType = 'L1' | 'L2' | 'L3' | 'L4' | 'L5'

export const LAYOUT_META: Record<LayoutType, { name: string; nameEn: string; desc: string }> = {
  L1: { name: '列表+详情',     nameEn: 'List-Detail',       desc: '左列表纵向滚动，右详情预览' },
  L2: { name: '编辑器+预览',   nameEn: 'Editor-Preview',    desc: '左编辑器，右实时预览' },
  L3: { name: '画布+属性',     nameEn: 'Canvas-Properties', desc: '居中画布所见即所得，右属性面板' },
  L4: { name: '卡片网格',      nameEn: 'Card-Grid',         desc: '多列卡片网格，右选中详情' },
  L5: { name: '横向时间线',    nameEn: 'Timeline',          desc: '上部内容+下部横向轨道，右属性' },
}

// ─── 侧栏节点（递归树） ───

export interface SidebarNode {
  id: string
  label: string
  children?: SidebarNode[]
  /** 内容区布局模板 */
  layout?: LayoutType
  /** 布局配置 */
  layoutConfig?: {
    centerLabel?: string
    rightLabel?: string
    description?: string
  }
}

// ─── 模块定义 ───

export interface ModuleDef {
  id: string
  page: string
  label: string
  labelEn: string
  subtitle: string
  icon: string
  color: string
  layer: 'content' | 'presentation' | 'assembly' | 'quality' | 'utility'
  sidebar: SidebarNode[]
}

// ─── 层级定义 ───

export interface LayerDef {
  id: string
  label: string
  labelEn: string
  emoji: string
}

export const LAYERS: LayerDef[] = [
  { id: 'utility',       label: '辅助',   labelEn: 'Utility',      emoji: '⚡' },
  { id: 'content',       label: '内容层', labelEn: 'Content',      emoji: '📝' },
  { id: 'presentation',  label: '表现层', labelEn: 'Presentation', emoji: '🎨' },
  { id: 'assembly',      label: '组装层', labelEn: 'Assembly',     emoji: '🎬' },
  { id: 'quality',       label: '质量层', labelEn: 'Quality',      emoji: '🔍' },
]

// ═══════════════════════════════════════════════════════════
// 默认模块注册表（含 layout 配置）
// ═══════════════════════════════════════════════════════════

export const DEFAULT_MODULES: ModuleDef[] = [

  // ── M0 素材管理器 ──
  {
    id: 'M0', page: 'asset-manager',
    label: '素材管理器', labelEn: 'Asset Manager',
    subtitle: '跨模块素材浏览',
    icon: 'package', color: '#6c7a89',
    layer: 'utility',
    sidebar: [
      { id: 'cat-asset', label: '素材分类', children: [
        { id: 'M0.1', label: '旁白文稿', layout: 'L1', layoutConfig: { centerLabel: '旁白素材列表', rightLabel: '旁白预览' } },
        { id: 'M0.2', label: '视觉画面', layout: 'L1', layoutConfig: { centerLabel: '视觉素材列表', rightLabel: '视觉预览' } },
        { id: 'M0.3', label: '文字叠层', layout: 'L1', layoutConfig: { centerLabel: '叠层素材列表', rightLabel: 'LaTeX/代码预览' } },
        { id: 'M0.4', label: '音频音效', layout: 'L1', layoutConfig: { centerLabel: '音频素材列表', rightLabel: '波形预览' } },
        { id: 'M0.5', label: '数据素材', layout: 'L1', layoutConfig: { centerLabel: '数据素材列表', rightLabel: '数据预览' } },
        { id: 'M0.6', label: '引用来源', layout: 'L1', layoutConfig: { centerLabel: '引用列表', rightLabel: '引用详情' } },
        { id: 'M0.7', label: '转场衔接', layout: 'L1', layoutConfig: { centerLabel: '转场素材列表', rightLabel: '转场配置' } },
      ]},
    ],
  },

  // ── M1 脚本工坊 ──
  {
    id: 'M1', page: 'script-editor',
    label: '脚本工坊', labelEn: 'Script Workshop',
    subtitle: 'Snyder + McKee',
    icon: 'mic', color: '#4ea8de',
    layer: 'content',
    sidebar: [
      { id: 'cat-narrative', label: '叙事结构', children: [
        { id: 'M1.1', label: '故事结构', layout: 'L3', layoutConfig: { centerLabel: '幕结构画布', rightLabel: '幕属性', description: 'Beat Sheet 分幕编辑，拖拽排序' } },
        { id: 'M1.4', label: '冲突弧线', layout: 'L3', layoutConfig: { centerLabel: '紧张度曲线', rightLabel: '转折点属性', description: 'SVG 折线图编辑紧张度' } },
      ]},
      { id: 'cat-draft', label: '文稿编辑', children: [
        { id: 'M1.2', label: '旁白文稿', layout: 'L2', layoutConfig: { centerLabel: '旁白编辑器', rightLabel: 'TTS 预听', description: '富文本分段编辑+关键词高亮' } },
        { id: 'M1.3', label: '节奏设计', layout: 'L5', layoutConfig: { centerLabel: '节奏条', rightLabel: '段落属性', description: '语速/停顿/语气时间轴' } },
      ]},
    ],
  },

  // ── M2 视觉画面 ──
  {
    id: 'M2', page: 'visual-assets',
    label: '视觉画面', labelEn: 'Visual Assets',
    subtitle: 'Mayer + Knaflic',
    icon: 'palette', color: '#2ecc71',
    layer: 'presentation',
    sidebar: [
      { id: 'cat-dynamic', label: '动态素材', children: [
        { id: 'M2.1', label: '动画规格', layout: 'L1', layoutConfig: { centerLabel: '动画列表', rightLabel: '动画代码+预览' } },
        { id: 'M2.4', label: '屏幕录制', layout: 'L4', layoutConfig: { centerLabel: '录制视频网格', rightLabel: '视频裁剪' } },
      ]},
      { id: 'cat-static', label: '静态素材', children: [
        { id: 'M2.2', label: '图表设计', layout: 'L3', layoutConfig: { centerLabel: '图表预览', rightLabel: '图表属性', description: '类型/数据绑定/颜色' } },
        { id: 'M2.3', label: '示意图',   layout: 'L3', layoutConfig: { centerLabel: '示意图预览', rightLabel: '节点编辑' } },
        { id: 'M2.5', label: '插画/照片', layout: 'L4', layoutConfig: { centerLabel: '图片网格', rightLabel: '大图+来源' } },
      ]},
    ],
  },

  // ── M3 文字叠层 ──
  {
    id: 'M3', page: 'text-overlays',
    label: '文字叠层', labelEn: 'Text Overlays',
    subtitle: 'Mayer Redundancy',
    icon: 'type', color: '#ffd700',
    layer: 'presentation',
    sidebar: [
      { id: 'cat-struct-text', label: '结构文字', children: [
        { id: 'M3.1', label: '标题卡',   layout: 'L3', layoutConfig: { centerLabel: '标题卡预览 16:9', rightLabel: '字体/颜色/动画' } },
        { id: 'M3.2', label: '要点列表', layout: 'L2', layoutConfig: { centerLabel: 'Markdown 编辑', rightLabel: '渲染预览' } },
      ]},
      { id: 'cat-tech-text', label: '技术文字', children: [
        { id: 'M3.3', label: '公式渲染', layout: 'L2', layoutConfig: { centerLabel: 'LaTeX 编辑器', rightLabel: 'KaTeX 渲染+直觉解释' } },
        { id: 'M3.4', label: '代码块',   layout: 'L2', layoutConfig: { centerLabel: '代码编辑器', rightLabel: '语法高亮预览' } },
      ]},
      { id: 'cat-aux-text', label: '辅助文字', children: [
        { id: 'M3.5', label: '字幕',     layout: 'L5', layoutConfig: { centerLabel: '字幕+时间轴', rightLabel: '字幕属性' } },
        { id: 'M3.6', label: '标注/引用', layout: 'L3', layoutConfig: { centerLabel: '标注画布', rightLabel: '标注属性' } },
      ]},
    ],
  },

  // ── M4 数据源 ──
  {
    id: 'M4', page: 'data-sources',
    label: '数据源', labelEn: 'Data Sources',
    subtitle: 'Knaflic + Mayer',
    icon: 'database', color: '#e67e22',
    layer: 'content',
    sidebar: [
      { id: 'cat-struct-data', label: '结构数据', children: [
        { id: 'M4.1', label: '时间线数据', layout: 'L1', layoutConfig: { centerLabel: '事件列表', rightLabel: '事件编辑' } },
        { id: 'M4.2', label: '对比结构',   layout: 'L3', layoutConfig: { centerLabel: '对比卡片预览', rightLabel: '左右项属性' } },
        { id: 'M4.5', label: '参数表',     layout: 'L1', layoutConfig: { centerLabel: 'KV 表格', rightLabel: '行属性' } },
      ]},
      { id: 'cat-content-data', label: '内容数据', children: [
        { id: 'M4.3', label: '数值数据集', layout: 'L2', layoutConfig: { centerLabel: 'JSON/CSV 编辑器', rightLabel: '表格预览' } },
        { id: 'M4.4', label: '代码示例',   layout: 'L2', layoutConfig: { centerLabel: '代码编辑器', rightLabel: '语法高亮' } },
      ]},
    ],
  },

  // ── M5 音频中心 ──
  {
    id: 'M5', page: 'audio-center',
    label: '音频中心', labelEn: 'Audio Center',
    subtitle: 'Mayer Modality',
    icon: 'volume', color: '#9b59b6',
    layer: 'presentation',
    sidebar: [
      { id: 'cat-voice', label: '语音', children: [
        { id: 'M5.1', label: 'TTS 合成', layout: 'L2', layoutConfig: { centerLabel: '旁白文本输入', rightLabel: '声音选择+试听' } },
        { id: 'M5.5', label: '时间戳',   layout: 'L5', layoutConfig: { centerLabel: '波形+时间标记', rightLabel: '句级时间' } },
      ]},
      { id: 'cat-sfx', label: '音效', children: [
        { id: 'M5.2', label: 'BGM',      layout: 'L4', layoutConfig: { centerLabel: '音乐网格', rightLabel: '波形+音量' } },
        { id: 'M5.3', label: '转场音效', layout: 'L4', layoutConfig: { centerLabel: '音效网格', rightLabel: '音效属性' } },
        { id: 'M5.4', label: '提示音',   layout: 'L4', layoutConfig: { centerLabel: '提示音网格', rightLabel: '试听' } },
      ]},
    ],
  },

  // ── M6 积木编辑器 ──
  {
    id: 'M6', page: 'block-editor',
    label: '积木编辑器', labelEn: 'Block Editor',
    subtitle: '分类浏览 + 实时预览',
    icon: 'blocks', color: '#f59e0b',
    layer: 'presentation',
    sidebar: [
      { id: 'cat-block-browse', label: '积木浏览', children: [
        { id: 'M6.1', label: '图表积木',   layout: 'L3', layoutConfig: { centerLabel: '积木预览 16:9', rightLabel: 'Props 面板' } },
        { id: 'M6.2', label: '代码积木',   layout: 'L3', layoutConfig: { centerLabel: '积木预览 16:9', rightLabel: 'Props 面板' } },
        { id: 'M6.3', label: '文字积木',   layout: 'L3', layoutConfig: { centerLabel: '积木预览 16:9', rightLabel: 'Props 面板' } },
        { id: 'M6.4', label: '对比积木',   layout: 'L3', layoutConfig: { centerLabel: '积木预览 16:9', rightLabel: 'Props 面板' } },
        { id: 'M6.5', label: '时间线积木', layout: 'L3', layoutConfig: { centerLabel: '积木预览 16:9', rightLabel: 'Props 面板' } },
      ]},
      { id: 'cat-block-tool', label: '积木工具', children: [
        { id: 'M6.6', label: '新建积木',    layout: 'L2', layoutConfig: { centerLabel: '积木定义', rightLabel: '骨架代码预览' } },
        { id: 'M6.7', label: 'Props Schema', layout: 'L2', layoutConfig: { centerLabel: 'Schema 编辑', rightLabel: '表单预览' } },
      ]},
    ],
  },

  // ── M6a 动画实验室 ──
  {
    id: 'M6a', page: 'animation-lab',
    label: '动画实验室', labelEn: 'Animation Lab',
    subtitle: 'Williams 动画原理',
    icon: 'sparkles', color: '#9b59b6',
    layer: 'presentation',
    sidebar: [
      { id: 'cat-anim-type', label: '动画类型', children: [
        { id: 'M6.A', label: '入场动画', layout: 'L3', layoutConfig: { centerLabel: '动画预览', rightLabel: 'duration/delay/easing' } },
        { id: 'M6.B', label: '强调动画', layout: 'L3', layoutConfig: { centerLabel: '动画预览', rightLabel: 'scale/glow/bounce' } },
        { id: 'M6.C', label: '退场动画', layout: 'L3', layoutConfig: { centerLabel: '动画预览', rightLabel: 'direction/fade' } },
      ]},
      { id: 'cat-anim-tool', label: '动画工具', children: [
        { id: 'M6.D', label: '缓动曲线', layout: 'L3', layoutConfig: { centerLabel: '贝塞尔曲线编辑器', rightLabel: '控制点+预设' } },
        { id: 'M6.E', label: '序列组合', layout: 'L5', layoutConfig: { centerLabel: '序列时间条', rightLabel: '排列方式' } },
      ]},
    ],
  },

  // ── M7 质量审查 ──
  {
    id: 'M7', page: 'quality-review',
    label: '质量审查', labelEn: 'Quality Review',
    subtitle: 'Clark & Mayer Ch.17',
    icon: 'listChecks', color: '#1abc9c',
    layer: 'quality',
    sidebar: [
      { id: 'cat-critical', label: '严重', children: [
        { id: 'M7.1', label: '冗余检查', layout: 'L1', layoutConfig: { centerLabel: '问题列表', rightLabel: '截图对比+修复' } },
        { id: 'M7.2', label: '时间同步', layout: 'L5', layoutConfig: { centerLabel: '对齐图', rightLabel: '偏差修复' } },
      ]},
      { id: 'cat-medium', label: '中等', children: [
        { id: 'M7.3', label: '空间邻近', layout: 'L1', layoutConfig: { centerLabel: '问题列表', rightLabel: '位置标注' } },
        { id: 'M7.4', label: '相干性',   layout: 'L1', layoutConfig: { centerLabel: '无关元素列表', rightLabel: '修复建议' } },
        { id: 'M7.5', label: '分段检查', layout: 'L1', layoutConfig: { centerLabel: '段落时长列表', rightLabel: '拆分建议' } },
      ]},
      { id: 'cat-suggestion', label: '建议', children: [
        { id: 'M7.6', label: '声音质量', layout: 'L1', layoutConfig: { centerLabel: '音频段+波形', rightLabel: '修复参数' } },
        { id: 'M7.7', label: '人格化',   layout: 'L1', layoutConfig: { centerLabel: '旁白段+评分', rightLabel: '改写建议' } },
      ]},
    ],
  },

  // ── M8 来源引用 ──
  {
    id: 'M8', page: 'references',
    label: '来源引用', labelEn: 'References',
    subtitle: '学术规范',
    icon: 'bookOpen', color: '#888888',
    layer: 'content',
    sidebar: [
      { id: 'cat-index', label: '索引管理', children: [
        { id: 'M8.1', label: '教科书库', layout: 'L1', layoutConfig: { centerLabel: '书目列表', rightLabel: '章节结构' } },
        { id: 'M8.2', label: '引用管理', layout: 'L1', layoutConfig: { centerLabel: '引用绑定列表', rightLabel: '引用详情' } },
      ]},
      { id: 'cat-check-out', label: '检查输出', children: [
        { id: 'M8.3', label: '版权检查', layout: 'L1', layoutConfig: { centerLabel: '扫描结果 ✅/⚠️/❌', rightLabel: 'License 详情' } },
        { id: 'M8.4', label: '片尾字幕', layout: 'L2', layoutConfig: { centerLabel: '引用排序编辑', rightLabel: '字幕预览' } },
      ]},
    ],
  },

  // ── M9 场景编排 ──
  {
    id: 'M9', page: 'scene-composer',
    label: '场景编排', labelEn: 'Scene Composer',
    subtitle: 'Mayer Pre-training',
    icon: 'film', color: '#f59e0b',
    layer: 'assembly',
    sidebar: [
      { id: 'cat-scene-edit', label: '场景编辑', children: [
        { id: 'M9.1', label: '场景列表', layout: 'L3', layoutConfig: { centerLabel: '场景预览 16:9', rightLabel: '场景属性' } },
        { id: 'M9.2', label: '布局选择', layout: 'L3', layoutConfig: { centerLabel: '布局预览', rightLabel: '布局模板' } },
        { id: 'M9.3', label: '积木放置', layout: 'L3', layoutConfig: { centerLabel: '积木预览', rightLabel: '积木选择器' } },
      ]},
      { id: 'cat-scene-out', label: '场景输出', children: [
        { id: 'M9.4', label: '预览画布', layout: 'L3', layoutConfig: { centerLabel: '16:9 全预览', rightLabel: '场景导航' } },
        { id: 'M9.5', label: '导出 JSON', layout: 'L2', layoutConfig: { centerLabel: 'JSON 格式化', rightLabel: '复制+下载' } },
      ]},
    ],
  },

  // ── M10 时间线 ──
  {
    id: 'M10', page: 'timeline-editor',
    label: '时间线', labelEn: 'Timeline Editor',
    subtitle: 'Mayer Temporal',
    icon: 'clock', color: '#e67e22',
    layer: 'assembly',
    sidebar: [
      { id: 'cat-time-seq', label: '时序编排', children: [
        { id: 'M10.1', label: '场景时序',   layout: 'L5', layoutConfig: { centerLabel: '时间轴+拖拽', rightLabel: '时长/间隙' } },
        { id: 'M10.4', label: '总时长计算', layout: 'L1', layoutConfig: { centerLabel: '时长统计表', rightLabel: '目标+溢出' } },
      ]},
      { id: 'cat-audio-align', label: '音轨对齐', children: [
        { id: 'M10.2', label: '旁白对齐', layout: 'L5', layoutConfig: { centerLabel: '双轨道对齐', rightLabel: '偏移量' } },
        { id: 'M10.3', label: '字幕时序', layout: 'L5', layoutConfig: { centerLabel: '波形+字幕条', rightLabel: '起止时间' } },
      ]},
    ],
  },
]

// ─── 辅助函数 ───

export function findModuleByPage(page: string): ModuleDef | undefined {
  return DEFAULT_MODULES.find(m => m.page === page)
}

export function getModulesByLayer(): { layer: LayerDef; modules: ModuleDef[] }[] {
  return LAYERS.map(layer => ({
    layer,
    modules: DEFAULT_MODULES.filter(m => m.layer === layer.id),
  })).filter(g => g.modules.length > 0)
}

/** 递归查找节点 */
export function findNode(nodes: SidebarNode[], id: string): SidebarNode | null {
  for (const n of nodes) {
    if (n.id === id) return n
    if (n.children) {
      const found = findNode(n.children, id)
      if (found) return found
    }
  }
  return null
}
