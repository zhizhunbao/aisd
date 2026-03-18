import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// ═══════════════════════════════════════════════════════════
// Video Lego — Vite 配置
// 积木 + 管理系统统一项目
// ═══════════════════════════════════════════════════════════

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // 禁用浏览器缓存 — 避免改代码后看到旧内容
    headers: {
      'Cache-Control': 'no-store',
    },
  },
  resolve: {
    alias: {
      // 管理系统代码
      '@': path.resolve(__dirname, 'src'),
      // 积木组件（本项目内）
      '@blocks': path.resolve(__dirname, 'src/blocks'),
      // 积木共享库（类型 + 视频主题）
      '@lego': path.resolve(__dirname, 'src/lib'),
    },
  },
  // Vite 8 (rolldown) 对 CJS require 更严格，需显式预构建
  optimizeDeps: {
    include: ['react-katex', 'prop-types', 'react-is'],
  },
})
