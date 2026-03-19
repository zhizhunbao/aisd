// ═══════════════════════════════════════════════════════════
// 视频乐高积木系统 — 核心类型定义
// Video Lego Block System — Core Type Definitions
// ═══════════════════════════════════════════════════════════

// ══════ 积木数据接口 Block Data Interfaces ══════

/** 公式推导步骤 Formula derivation step */
export interface FormulaStep {
  latex: string;
  annotation?: string;
  highlight?: boolean;
}

/** 公式块数据 */
export interface FormulaBlockData {
  latex: string;
  label?: string;
  color?: string;
}

/** 公式对比数据 */
export interface FormulaComparisonData {
  left: { latex: string; label: string; color?: string };
  right: { latex: string; label: string; color?: string };
}

/** 公式推导数据 */
export interface FormulaDerivationData {
  steps: FormulaStep[];
  /** 教科书来源标注 Textbook source */
  source?: string;
}

/** 对比列数据 Comparison column */
export interface CompareColumnData {
  label: string;
  value: string;
  icon?: string;
  color: string;
  subItems?: string[];
}

/** 对比图数据 */
export interface ComparisonSplitData {
  left: CompareColumnData;
  right: CompareColumnData;
}

/** 时间线事件 */
export interface TimelineEventData {
  year: string;
  text: string;
  color?: string;
  icon?: string;
}

/** 时间线数据 */
export interface TimelineData {
  events: TimelineEventData[];
  /** 'vertical' | 'horizontal' (default: vertical) */
  direction?: 'vertical' | 'horizontal';
}

/** 进度条数据 */
export interface ProgressBarData {
  label: string;
  value: number; // 0-100
  color: string;
  displayValue?: string;
}

/** 统计卡片数据 */
export interface StatCardData {
  label: string;
  value: string;
  icon?: string;
  color: string;
  description?: string;
}

/** 代码块数据 */
export interface CodeBlockData {
  code: string;
  language?: string;
  label?: string;
  color?: string;
}

/** 图片展示数据 */
export interface ImageDisplayData {
  src: string;
  caption?: string;
  maxHeight?: number;
}

/** U曲线/J曲线数据 */
export interface UCurveData {
  points: { x: number; y: number }[];
  xLabel: string;
  yLabel: string;
  /** 教科书来源 */
  source?: string;
  zones?: { start: number; end: number; color: string; label: string }[];
  bestPoint?: { x: number; annotation: string };
}

/** 2D 散点图数据 */
export interface ScatterPlot2DData {
  points: { x: number; y: number; label: string; color?: string }[];
  xLabel?: string;
  yLabel?: string;
  source?: string;
  /** 查询点（高亮显示 + 动画） */
  queryPoint?: { x: number; y: number; k?: number };
}

/** 柱状图数据 */
export interface BarChartData {
  bars: { label: string; value: number; color: string }[];
  yLabel?: string;
  source?: string;
}

/** 热力图数据 */
export interface HeatMapData {
  matrix: number[][];
  xLabels: string[];
  yLabels: string[];
  colorScale?: { low: string; high: string };
  source?: string;
}

/** 树节点 */
export interface TreeNodeData {
  label: string;
  color?: string;
  children?: TreeNodeData[];
}

/** 树图数据 */
export interface TreeDiagramData {
  root: TreeNodeData;
  source?: string;
}

/** 流程图步骤 */
export interface FlowStepData {
  label: string;
  icon?: string;
  color?: string;
  description?: string;
}

/** 流程图数据 */
export interface FlowDiagramData {
  steps: FlowStepData[];
  direction?: 'horizontal' | 'vertical';
  source?: string;
}

/** 神经网络层 */
export interface NetworkLayerData {
  type: 'input' | 'dense' | 'conv' | 'pool' | 'output' | 'custom';
  units: number;
  label?: string;
  color?: string;
}

/** 神经网络图数据 */
export interface NetworkDiagramData {
  layers: NetworkLayerData[];
  source?: string;
}

/** 矩阵动画数据 */
export interface MatrixAnimationData {
  left: number[][];
  right: number[][];
  result: number[][];
  operation: 'multiply' | 'add' | 'convolve';
  source?: string;
}

/** 梯度下降数据 */
export interface GradientDescentData {
  /** 损失函数（用字符串表达式或预计算点） */
  surfacePoints?: { x: number; y: number; z: number }[];
  path: { x: number; y: number }[];
  learningRate: number;
  source?: string;
}

/** 卷积动画数据 */
export interface ConvolutionAnimationData {
  input: number[][];
  kernel: number[][];
  stride?: number;
  padding?: number;
  source?: string;
}

/** 数据变换动画数据 */
export interface DataTransformData {
  before: { x: number; y: number; label?: string }[];
  after: { x: number; y: number; label?: string }[];
  transformLabel: string;
  source?: string;
}

/** 要点列表数据 */
export interface KeyPointsData {
  points: { icon?: string; text: string; color?: string; bold?: boolean }[];
}

/** 结论横幅数据 */
export interface ConclusionBannerData {
  text: string;
  icon?: string;
}

/** 知识单元数据 — 一屏黑板上的完整内容 */
export interface KnowledgeUnitData {
  /** 中文核心术语 */
  zhName: string;
  /** 英文对照 */
  enName: string;
  /** 同义词/别名列表 */
  aliases?: string[];
  /** LaTeX 核心公式 */
  formula?: string;
  /** 公式标注文字 */
  formulaLabel?: string;
  /** 2D 图解组件名（在 DIAGRAM_REGISTRY 中查找） */
  diagram?: string;
  /** 一句话白话释义 */
  explanation: string;
  /** 中文名强调色（默认 white） */
  color?: string;
}

// ══════ 积木注册表类型 Block Registry Types ══════

/** 所有积木类型映射 */
export interface BlockDataMap {
  FormulaBlock: FormulaBlockData;
  FormulaDerivation: FormulaDerivationData;
  FormulaComparison: FormulaComparisonData;
  ComparisonSplit: ComparisonSplitData;
  Timeline: TimelineData;
  ProgressBars: { bars: ProgressBarData[] };
  StatCards: { cards: StatCardData[] };
  CodeBlock: CodeBlockData;
  ImageDisplay: ImageDisplayData;
  UCurve: UCurveData;
  ScatterPlot2D: ScatterPlot2DData;
  BarChart: BarChartData;
  HeatMap: HeatMapData;
  TreeDiagram: TreeDiagramData;
  FlowDiagram: FlowDiagramData;
  NetworkDiagram: NetworkDiagramData;
  MatrixAnimation: MatrixAnimationData;
  GradientDescent: GradientDescentData;
  ConvolutionAnimation: ConvolutionAnimationData;
  DataTransform: DataTransformData;
  KeyPoints: KeyPointsData;
  ConclusionBanner: ConclusionBannerData;
  KnowledgeUnit: KnowledgeUnitData;
}

/** 积木名称 */
export type BlockName = keyof BlockDataMap;

// ══════ 场景类型 Scene Types ══════

/** 场景中的一个可视化元素（选积木 + 传数据） */
export interface SceneVisual<T extends BlockName = BlockName> {
  /** 使用哪个积木 Which block to use */
  block: T;
  /** 传给积木的数据 Data for the block */
  data: BlockDataMap[T];
}

/** 右侧要点 */
export interface KeyPoint {
  icon?: string;
  text: string;
  color?: string;
  bold?: boolean;
  variant?: 'normal' | 'highlight' | 'warning' | 'formula';
  latex?: string;
}

/** 场景布局类型 */
export type LayoutType = 'landscape' | 'portrait' | 'blackboard';

/** 一个场景的完整数据 */
export interface SceneData {
  /** 场景布局 */
  layout: LayoutType;
  /** 所属幕名 */
  act: string;
  /** 场景标题 */
  title: string;
  /** 场景子标题 */
  subtitle?: string;
  /** 标题颜色（可选） */
  titleColor?: string;
  /** 左侧可视化元素列表 */
  visuals: SceneVisual[];
  /** 右侧要点列表 */
  points: KeyPoint[];
  /** 底部结论横幅 */
  conclusion?: { text: string; icon?: string };
  /** 黑板布局专用：进度信息 */
  progress?: { current: number; total: number };
  /** 黑板布局专用：钉在左上角的已闪过的知识点 */
  pinnedItems?: Array<{ zhName: string; enName: string; color?: string }>;
}

// ══════ 视频级数据 Video-Level Data ══════

/** 字幕条目 */
export interface SubtitleEntry {
  start: number;
  end: number;
  text: string;
}

/** 时间戳条目 */
export interface TimestampEntry {
  start: number;
  end: number;
}

/** 旁白数据 */
export interface NarrationData {
  /** 音频文件路径（相对于 public/） */
  audioFile: string;
  /** 每个场景的时间戳 */
  timestamps: TimestampEntry[];
  /** 字幕文本 */
  subtitles: SubtitleEntry[];
}

/** 视频元数据 */
export interface VideoMeta {
  topic: string;
  course: string;
  title: string;
  /** 教科书来源 */
  textbookSource?: string;
  /** 素材来源（Wikipedia、教科书、论文等） */
  contentSources?: string[];
  /** 总时长（秒） */
  totalDurationSec: number;
}

/** 一个视频的完整数据 — 做视频唯一需要写的东西 */
export interface VideoData {
  meta: VideoMeta;
  narration: NarrationData;
  scenes: SceneData[];
}
