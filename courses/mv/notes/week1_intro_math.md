# Week 1: 机器视觉导论 — 数学公式速查 (Math Quick Reference)

> 📐 See also: [概念速查](week1_intro_cheatsheet.md) | [代码参考](week1_intro_code.md)
> 📄 Source: slides + demo code

---

## 📐 公式与计算

### 1. 图像矩阵表示

**灰度图像**（Grayscale Image）：

$$I \in \mathbb{R}^{H \times W}$$

| 符号      | 含义                     | 取值范围           |
| --------- | ------------------------ | ------------------ |
| $I$       | 图像矩阵                 | —                  |
| $H$       | 图像高度（行数）         | 正整数             |
| $W$       | 图像宽度（列数）         | 正整数             |
| $I(y, x)$ | 位置 $(y, x)$ 处的像素值 | $[0, 255]$ (uint8) |

**彩色图像**（RGB Color Image）：

$$I \in \mathbb{R}^{H \times W \times 3}$$

| 符号         | 含义         | 取值范围   |
| ------------ | ------------ | ---------- |
| $I(y, x, 0)$ | Red 通道值   | $[0, 255]$ |
| $I(y, x, 1)$ | Green 通道值 | $[0, 255]$ |
| $I(y, x, 2)$ | Blue 通道值  | $[0, 255]$ |

> ⚠️ 注意坐标顺序：$(y, x)$ = (行, 列)，不是 $(x, y)$

---

### 2. 图像内存大小计算

**灰度图内存：**

$$\text{Size}_{\text{gray}} = H \times W \times 1 \text{ bytes}$$

**RGB 彩色图内存：**

$$\text{Size}_{\text{RGB}} = H \times W \times 3 \text{ bytes}$$

**RGBA（带透明度）图内存：**

$$\text{Size}_{\text{RGBA}} = H \times W \times 4 \text{ bytes}$$

📝 **手算练习 1：**

> 一张 1920×1080 的 RGB 图像（无压缩）占多少 MB？
>
> 答：$1920 \times 1080 \times 3 = 6{,}220{,}800$ bytes $\approx 5.93$ MB

📝 **手算练习 2：**

> 一张 640×480 灰度图占多少 KB？
>
> 答：$640 \times 480 \times 1 = 307{,}200$ bytes $= 300$ KB

---

### 3. RGB ↔ HSV 色彩空间转换

**RGB → HSV 转换公式：**

先将 RGB 归一化到 $[0, 1]$：$R', G', B' = R/255, G/255, B/255$

$$C_{\max} = \max(R', G', B')$$
$$C_{\min} = \min(R', G', B')$$
$$\Delta = C_{\max} - C_{\min}$$

**Hue（色相）计算：**

$$
H = \begin{cases}
0° & \text{if } \Delta = 0 \\
60° \times \frac{G' - B'}{\Delta} \mod 360° & \text{if } C_{\max} = R' \\
60° \times \frac{B' - R'}{\Delta} + 120° & \text{if } C_{\max} = G' \\
60° \times \frac{R' - G'}{\Delta} + 240° & \text{if } C_{\max} = B'
\end{cases}
$$

**Saturation（饱和度）：**

$$
S = \begin{cases}
0 & \text{if } C_{\max} = 0 \\
\frac{\Delta}{C_{\max}} & \text{otherwise}
\end{cases}
$$

**Value（明度）：**

$$V = C_{\max}$$

| 符号 | 含义              | 取值范围     |
| ---- | ----------------- | ------------ |
| $H$  | 色相 — 颜色类型   | $[0°, 360°)$ |
| $S$  | 饱和度 — 鲜艳程度 | $[0, 1]$     |
| $V$  | 明度 — 亮度       | $[0, 1]$     |

📝 **手算练习 3：**

> 纯红色 RGB = (255, 0, 0)，求 HSV 值？
>
> 答：$R'=1, G'=0, B'=0$；$C_{\max}=1, C_{\min}=0, \Delta=1$
>
> - $H = 60° \times \frac{0-0}{1} = 0°$
> - $S = 1/1 = 1$
> - $V = 1$
>   → HSV = **(0°, 1, 1)** — 色相0°(红), 饱和度满, 亮度满

📝 **手算练习 4：**

> RGB = (128, 0, 255)，这是什么颜色？HSV 大约是多少？
>
> 答：$R'=0.502, G'=0, B'=1$；$C_{\max}=1, C_{\min}=0, \Delta=1$
>
> - $H = 60° \times \frac{0.502-0}{1} + 240° = 270.1°$（蓝紫色）
> - $S = 1$
> - $V = 1$
>   → 紫色/Violet

---

### 4. 压缩率计算

$$\text{Compression Ratio} = \frac{\text{Original Size}}{\text{Compressed Size}}$$

$$\text{Space Saving} = 1 - \frac{\text{Compressed Size}}{\text{Original Size}} = 1 - \frac{1}{\text{Compression Ratio}}$$

📝 **手算练习 5：**

> 原始 RAW 图像 6 MB，JPEG 压缩后 600 KB，压缩率是多少？
>
> 答：$6{,}000 / 600 = 10:1$，节省 $1 - 1/10 = 90\%$ 空间

---

## 🔢 数值速查表

| 概念          | 灰度         | RGB                   | RGBA (带透明度)       |
| ------------- | ------------ | --------------------- | --------------------- |
| 通道数        | 1            | 3                     | 4                     |
| 每像素字节    | 1            | 3                     | 4                     |
| 矩阵维度      | $H \times W$ | $H \times W \times 3$ | $H \times W \times 4$ |
| 值范围(uint8) | 0-255        | 0-255 per ch          | 0-255 per ch          |

| HSV 通道 | 含义   | 范围 (标准) | OpenCV 范围 |
| -------- | ------ | ----------- | ----------- |
| H        | 色相   | 0°-360°     | 0-179       |
| S        | 饱和度 | 0-1         | 0-255       |
| V        | 明度   | 0-1         | 0-255       |

> ⚠️ **OpenCV 特殊：** H 通道范围是 **0-179**（不是 0-360），因为 uint8 最大 255，所以 OpenCV 将色相值除以 2

---

## 🔗 相关文件

- 📖 [概念速查](week1_intro_cheatsheet.md) — 定义、要点、陷阱
- 🔧 [代码参考](week1_intro_code.md) — Python/OpenCV 实现
