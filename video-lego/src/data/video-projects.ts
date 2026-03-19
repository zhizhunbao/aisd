// ═══════════════════════════════════════════════════════════
// 视频项目数据 — 单一数据源（Dashboard + VideoList 共用）
// Video Projects Data — Single Source of Truth
// ═══════════════════════════════════════════════════════════

export interface VideoPhase {
  name: string;
  status: 'completed' | 'in_progress' | 'pending' | 'skipped';
}

export interface VideoProject {
  course: string;
  topic: string;
  title: string;
  currentPhase: number;
  totalPhases: number;
  sceneCount: number;
  durationSec: number;
  phases: VideoPhase[];
}

export const VIDEO_PROJECTS: VideoProject[] = [
  {
    course: 'machine-learning',
    topic: 'knn',
    title: 'KNN — 从抄作业到 AI 基础设施',
    currentPhase: 7,
    totalPhases: 9,
    sceneCount: 20,
    durationSec: 395.3,
    phases: [
      { name: '初始化', status: 'completed' },
      { name: '内容提取', status: 'completed' },
      { name: '脚本写作', status: 'completed' },
      { name: '分镜设计', status: 'completed' },
      { name: '素材制作', status: 'completed' },
      { name: '语音合成', status: 'completed' },
      { name: '字幕生成', status: 'completed' },
      { name: '组装渲染', status: 'in_progress' },
      { name: '质量审查', status: 'pending' },
    ],
  },
];
