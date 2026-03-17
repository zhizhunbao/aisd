// ═══════════════════════════════════════════════════════════
// Video Lego 管理系统 — 入口
// Management System — Entry point
// ═══════════════════════════════════════════════════════════

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { App } from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
