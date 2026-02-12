"""
CST8508 Lab 4: Streaming Live Webcam Video with Timestamp Overlay
Author: Peng Wang
Student Number: 041107730

Accesses a live video stream from the webcam using OpenCV,
overlays the current time (24-hour format with milliseconds and timezone)
on each frame, and displays the video feed in a window.
Press 'q' to quit the video stream.
"""

# 导入OpenCV库，用于视频捕获和图像处理
# Import OpenCV library for video capture and image processing
import cv2

# 导入datetime模块，用于获取当前时间（含毫秒）
# Import datetime module for getting current time (with milliseconds)
from datetime import datetime

# 导入time模块，用于获取本地时区名称
# Import time module for getting local timezone name
import time

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# 默认摄像头索引（0 = 笔记本内置摄像头）
# Default camera index (0 = laptop built-in webcam)
CAMERA_INDEX = 0

# 时间戳字体（等宽无衬线字体，清晰易读）
# Timestamp font (monospace sans-serif, clean and readable)
FONT = cv2.FONT_HERSHEY_SIMPLEX

# 时间戳在画面上的位置（x=10像素, y=30像素, 距左上角）
# Timestamp position on the frame (x=10px, y=30px, from top-left corner)
TEXT_POSITION = (10, 30)

# 字体缩放比例（0.7 适合大多数分辨率的摄像头画面）
# Font scale (0.7 works well for most webcam resolutions)
FONT_SCALE = 0.7

# 字体颜色 BGR 格式（0, 255, 0 = 纯绿色，在深色和浅色背景上都清晰可见）
# Font color in BGR format (0, 255, 0 = pure green, visible on both dark and light backgrounds)
FONT_COLOR = (0, 255, 0)

# 字体线条粗细（2像素，确保文字清晰但不遮挡画面）
# Font line thickness (2 pixels, ensures readability without blocking the view)
FONT_THICKNESS = 2

# 视频窗口标题
# Video window title
WINDOW_TITLE = "Lab 4 - Webcam with Timestamp"

# 退出键的ASCII码（'q' = 113, 按下此键结束视频流）
# ASCII code of the quit key ('q' = 113, press this key to stop the video stream)
QUIT_KEY = ord('q')

# 等待键盘输入的毫秒数（1ms = 尽可能快地刷新画面，同时仍能检测按键）
# Milliseconds to wait for keyboard input (1ms = refresh as fast as possible while still detecting key presses)
WAIT_KEY_MS = 1

# ============================================================
# 步骤 1：初始化摄像头
# Step 1: Initialize Webcam
# ============================================================

# 创建VideoCapture对象并连接到默认摄像头
# Create VideoCapture object and connect to the default webcam
# 参数：CAMERA_INDEX=0 表示使用第一个可用的摄像头（通常是笔记本内置摄像头）
# Parameter: CAMERA_INDEX=0 means use the first available camera (usually laptop built-in webcam)
cap = cv2.VideoCapture(CAMERA_INDEX)

# 检查摄像头是否成功打开q
# Check if the webcam was opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam. Please check your camera connection.")
    exit()

# 打印提示信息
# Print instructions
print("Webcam started successfully.")
print(f"Press '{chr(QUIT_KEY)}' to quit the video stream.")

# ============================================================
# 步骤 2：视频流主循环（捕获帧 → 叠加时间戳 → 显示 → 检测退出键）
# Step 2: Video Stream Main Loop (capture frame → overlay timestamp → display → detect quit key)
# ============================================================

# 无限循环，持续捕获和显示帧画面
# Infinite loop to continuously capture and display frames
while True:
    # 从摄像头读取一帧画面
    # Read one frame from the webcam
    # ret: 布尔值，表示是否成功读取（True=成功，False=失败）
    # ret: boolean, indicates if read was successful (True=success, False=failure)
    # frame: 捕获的图像帧（numpy数组，形状为 [高, 宽, 3通道BGR]）
    # frame: captured image frame (numpy array, shape [height, width, 3 channels BGR])
    ret, frame = cap.read()

    # 如果读取失败，打印错误并退出循环
    # If read failed, print error and break out of the loop
    if not ret:
        print("Error: Failed to capture frame from webcam.")
        break

    # 获取当前本地时间（精确到微秒）
    # Get current local time (precise to microseconds)
    now = datetime.now()

    # 计算本地时区的UTC偏移量（如 "UTC-5", "UTC+8"）
    # Calculate local timezone UTC offset (e.g., "UTC-5", "UTC+8")
    # 原因：Windows中文系统下 time.tzname 返回中文（如 "东部标准时间"），
    #       OpenCV 的 putText 只支持 ASCII 字符，中文会显示为 ????
    # Reason: On Chinese Windows, time.tzname returns Chinese characters
    #       (e.g., "东部标准时间"), but OpenCV putText only supports ASCII
    # 使用 tm_isdst 判断当前是否处于夏令时（0=否，1=是），选择对应的偏移量
    # Use tm_isdst to check if DST is currently active (0=no, 1=yes), pick correct offset
    is_dst = time.localtime().tm_isdst
    utc_offset_seconds = time.altzone if is_dst else time.timezone
    utc_offset_hours = -utc_offset_seconds // 3600
    local_tz = f"UTC{utc_offset_hours:+d}"

    # 格式化时间字符串：年-月-日 时:分:秒.毫秒 时区（24小时制）
    # Format time string: YYYY-MM-DD HH:MM:SS.mmm Timezone (24-hour format)
    # %Y = 四位年份, %m = 月份(01-12), %d = 日期(01-31)
    # %Y = 4-digit year, %m = month (01-12), %d = day (01-31)
    # %H = 24小时制的小时（00-23），%M = 分钟（00-59），%S = 秒（00-59）
    # %H = 24-hour format hour (00-23), %M = minute (00-59), %S = second (00-59)
    # %f = 微秒（000000-999999），取前3位得到毫秒
    # %f = microsecond (000000-999999), take first 3 digits for milliseconds
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.") + now.strftime("%f")[:3] + f" {local_tz}"

    # 使用putText将时间戳绘制到帧画面上
    # Use putText to draw the timestamp on the frame
    # 参数：frame = 目标图像（会被直接修改），
    #       timestamp = 要绘制的文字内容，
    #       TEXT_POSITION = 文字左下角的坐标（距左上角 10px右, 30px下），
    #       FONT = 字体类型（HERSHEY_SIMPLEX = 正常大小的无衬线字体），
    #       FONT_SCALE = 字体缩放倍数（0.7 = 原始大小的70%），
    #       FONT_COLOR = 文字颜色BGR（绿色，在各种背景上都醒目），
    #       FONT_THICKNESS = 笔画粗细（2像素，清晰但不过粗）
    # Parameters: frame = target image (modified in-place),
    #       timestamp = text content to draw,
    #       TEXT_POSITION = bottom-left corner of text (10px right, 30px down from top-left),
    #       FONT = font type (HERSHEY_SIMPLEX = normal-size sans-serif font),
    #       FONT_SCALE = font scale factor (0.7 = 70% of original size),
    #       FONT_COLOR = text color in BGR (green, stands out on various backgrounds),
    #       FONT_THICKNESS = stroke thickness (2 pixels, clear but not too thick)
    cv2.putText(frame, timestamp, TEXT_POSITION, FONT, FONT_SCALE,
                FONT_COLOR, FONT_THICKNESS)

    # 在窗口中显示带有时间戳的帧画面
    # Display the frame with timestamp overlay in a window
    cv2.imshow(WINDOW_TITLE, frame)

    # 等待1毫秒检测键盘输入，按 'q' 退出
    # Wait 1ms for keyboard input, press 'q' to quit
    # waitKey 返回按下的键的ASCII码（&0xFF 确保跨平台兼容性）
    # waitKey returns ASCII code of pressed key (&0xFF ensures cross-platform compatibility)
    if cv2.waitKey(WAIT_KEY_MS) & 0xFF == QUIT_KEY:
        print("Quit key pressed. Stopping video stream...")
        break

# ============================================================
# 步骤 3：清理资源
# Step 3: Cleanup Resources
# ============================================================

# 释放摄像头硬件资源
# Release the webcam hardware resources
# 原因：不释放可能导致摄像头被锁定，其他程序无法使用
# Reason: Not releasing may lock the camera, preventing other programs from using it
cap.release()

# 关闭所有OpenCV创建的窗口
# Close all windows created by OpenCV
cv2.destroyAllWindows()

# 打印结束信息
# Print termination message
print("Webcam released and all windows closed.")
