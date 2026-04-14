@echo off
title NLP ROS 2 Demo
echo ==========================================
echo   NLP ROS 2 Voice Q^&A Demo
echo ==========================================
echo.

REM ── 开始录屏 ──
echo [1/2] Starting screen recording (Win+Alt+R)...
start "" psr.exe /start /output NUL /maxsc 0
echo   Tip: Press Win+Alt+R to start Xbox Game Bar recording
echo.

REM ── SSH 启动节点 ──
echo [2/2] Connecting to loaner laptop...
echo   Target: aisd@192.168.2.33
echo.
echo   === Controls ===
echo   Ctrl+B then D  = detach (nodes keep running)
echo   Ctrl+C         = stop current node
echo.
ssh -t -o StrictHostKeyChecking=no aisd@192.168.2.33 "bash ~/run_loaner.sh"

echo.
echo [Done] Disconnected. Nodes may still be running.
echo   Re-attach:  ssh -t aisd@192.168.2.33 "tmux attach -t nlp_rag"
echo   Stop all:   ssh aisd@192.168.2.33 "bash ~/stop_loaner.sh"
pause
