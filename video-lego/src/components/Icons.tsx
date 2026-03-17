// ═══════════════════════════════════════════════════════════
// SVG 图标集 — lucide-react 统一封装
// Icon Library — centralized SVG icons via lucide-react
//
// 用法: import { Icons } from '@/components/Icons'
//       <Icons.Home size={18} />
// ═══════════════════════════════════════════════════════════

export {
  // ─── 导航 Navigation ───
  LayoutDashboard as IconDashboard,
  Home as IconHome,
  Package as IconPackage,
  Blocks as IconBlocks,
  Clapperboard as IconVideo,
  Film as IconFilm,

  // ─── 操作 Actions ───
  Plus as IconPlus,
  Trash2 as IconTrash,
  Copy as IconCopy,
  RefreshCw as IconReplace,
  ArrowUp as IconArrowUp,
  ArrowDown as IconArrowDown,
  ChevronDown as IconChevronDown,
  ChevronRight as IconChevronRight,
  X as IconX,
  Check as IconCheck,
  Upload as IconUpload,
  Download as IconDownload,
  GripVertical as IconGrip,
  ArrowLeft as IconArrowLeft,
  MoreVertical as IconMore,
  Search as IconSearch,

  // ─── 面板 Panels ───
  ClipboardList as IconProperties,
  Grid3X3 as IconPalette,
  Settings as IconSettings,
  Eye as IconPreview,
  MapPin as IconPin,

  // ─── 布局 Layouts ───
  Square as IconFullscreen,
  Columns2 as IconSplit,
  Columns3 as IconThreeColumn,

  // ─── 积木分类 Block Categories ───
  FunctionSquare as IconFormula,
  Scale as IconCompare,
  BarChart3 as IconChart,
  GitFork as IconRelation,
  Image as IconDisplay,
  Play as IconProcess,

  // ─── 状态 Status ───
  CircleCheck as IconReady,
  Circle as IconPending,
  Star as IconStar,
  AlertCircle as IconAlert,
  Info as IconInfo,
} from 'lucide-react'

// 重新导出 LucideProps 类型方便使用
export type { LucideProps as IconProps } from 'lucide-react'
