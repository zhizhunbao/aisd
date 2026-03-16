"""
3b1b 风格可复用组件 — Community Manim 移植版
=============================================
源自 3b1b/videos/_2024/transformers/helpers.py
移植到 community manim (pip install manim)

用法:
    from manim_templates import *
    
    class MyScene(Scene):
        def construct(self):
            nn = NeuralNetwork([4, 8, 4])
            self.play(FadeIn(nn))
"""
from manim import *
import numpy as np
import random
import itertools as it


# ============================================================
# 颜色工具
# ============================================================

def value_to_color(
    value,
    low_positive_color="#1e3a5f",   # 深蓝
    high_positive_color="#5b9bd5",  # 亮蓝
    low_negative_color="#5f1e1e",   # 深红
    high_negative_color="#eb5757",  # 亮红
    min_value=0.0,
    max_value=10.0,
):
    """数值 → 颜色映射（蓝正红负）"""
    alpha = np.clip(abs(value) / max(abs(max_value), 1e-9), 0, 1)
    if value >= 0:
        return interpolate_color(
            ManimColor(low_positive_color),
            ManimColor(high_positive_color),
            alpha,
        )
    else:
        return interpolate_color(
            ManimColor(low_negative_color),
            ManimColor(high_negative_color),
            alpha,
        )


# ============================================================
# NeuralNetwork — 自动绘制神经网络图
# ============================================================

class NeuralNetwork(VGroup):
    """
    自动生成多层神经网络可视化。
    
    用法:
        nn = NeuralNetwork([4, 8, 4])          # 3层网络
        nn = NeuralNetwork([3, 6, 6, 2])       # 4层网络
        nn.set_height(4).move_to(ORIGIN)
    """
    def __init__(
        self,
        layer_sizes=[6, 12, 6],
        neuron_radius=0.1,
        v_buff_ratio=1.0,
        h_buff_ratio=7.0,
        max_stroke_width=2.0,
        stroke_decay=2.0,
        neuron_color=WHITE,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.max_stroke_width = max_stroke_width
        self.stroke_decay = stroke_decay

        # 创建各层神经元
        layers = VGroup()
        for n in layer_sizes:
            layer = VGroup(*[
                Dot(radius=neuron_radius).set_stroke(neuron_color, 1)
                for _ in range(n)
            ])
            layer.arrange(DOWN, buff=neuron_radius * 2 * v_buff_ratio)
            layers.add(layer)

        layers.arrange(RIGHT, buff=neuron_radius * 2 * h_buff_ratio)

        # 创建连线
        lines = VGroup()
        for l1, l2 in zip(layers, layers[1:]):
            layer_lines = VGroup(*[
                Line(
                    n1.get_center(), n2.get_center(),
                    buff=neuron_radius,
                )
                for n1, n2 in it.product(l1, l2)
            ])
            lines.add(layer_lines)

        self.add(layers, lines)
        self.layers = layers
        self.lines = lines

        self.randomize_colors()

    def randomize_colors(self):
        """随机着色连线和神经元"""
        for group in self.lines:
            for line in group:
                line.set_stroke(
                    value_to_color(random.uniform(-10, 10)),
                    self.max_stroke_width * random.random() ** self.stroke_decay,
                )
        for layer in self.layers:
            for dot in layer:
                dot.set_fill(WHITE, random.random())
        return self


# ============================================================
# WeightMatrix — 带颜色映射的权重矩阵
# ============================================================

class WeightMatrix(VGroup):
    """
    可视化权重矩阵，数值映射到颜色。
    
    用法:
        mat = WeightMatrix(shape=(4, 6))
        mat = WeightMatrix(values=np.random.randn(4, 6))
    """
    def __init__(
        self,
        values=None,
        shape=(4, 6),
        value_range=(-5.0, 5.0),
        cell_size=0.4,
        font_size=18,
        show_values=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if values is None:
            values = np.random.uniform(*value_range, size=shape)
        else:
            shape = values.shape

        rows, cols = shape
        self.values = values
        self.entries = VGroup()
        self.cells = VGroup()

        for r in range(rows):
            for c in range(cols):
                val = values[r, c]
                color = value_to_color(val, max_value=max(abs(value_range[0]), abs(value_range[1])))
                
                cell = Square(side_length=cell_size)
                cell.set_fill(color, opacity=0.8)
                cell.set_stroke(WHITE, 0.5, opacity=0.3)
                cell.move_to([c * cell_size, -r * cell_size, 0])
                self.cells.add(cell)

                if show_values:
                    label = Text(f"{val:.1f}", font_size=font_size, color=WHITE)
                    label.move_to(cell)
                    self.entries.add(label)

        self.add(self.cells)
        if show_values:
            self.add(self.entries)

        # 添加方括号
        left_bracket = Text("[", font_size=font_size * 3, color=WHITE)
        right_bracket = Text("]", font_size=font_size * 3, color=WHITE)
        left_bracket.next_to(self.cells, LEFT, buff=0.1)
        right_bracket.next_to(self.cells, RIGHT, buff=0.1)
        left_bracket.stretch_to_fit_height(self.cells.get_height() * 1.1)
        right_bracket.stretch_to_fit_height(self.cells.get_height() * 1.1)
        self.brackets = VGroup(left_bracket, right_bracket)
        self.add(self.brackets)

        self.center()


# ============================================================
# NumericVector — 数值向量可视化（竖排）
# ============================================================

class NumericVector(VGroup):
    """
    可视化一个竖排数值向量。
    
    用法:
        vec = NumericVector(length=8)
        vec = NumericVector(values=np.array([1.2, -0.5, 3.1]))
    """
    def __init__(
        self,
        values=None,
        length=7,
        value_range=(-5.0, 5.0),
        cell_width=0.5,
        cell_height=0.35,
        font_size=16,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if values is None:
            values = np.random.uniform(*value_range, size=length)

        self.values = values
        self.entries = VGroup()
        self.cells = VGroup()

        for i, val in enumerate(values):
            color = value_to_color(val, max_value=max(abs(value_range[0]), abs(value_range[1])))
            cell = Rectangle(width=cell_width, height=cell_height)
            cell.set_fill(color, opacity=0.7)
            cell.set_stroke(WHITE, 0.5, opacity=0.3)
            cell.move_to([0, -i * cell_height, 0])
            self.cells.add(cell)

            label = Text(f"{val:+.1f}", font_size=font_size, color=WHITE)
            label.move_to(cell)
            self.entries.add(label)

        self.add(self.cells, self.entries)

        # 方括号
        lb = Text("[", font_size=font_size * 3, color=WHITE)
        rb = Text("]", font_size=font_size * 3, color=WHITE)
        lb.next_to(self.cells, LEFT, buff=0.05)
        rb.next_to(self.cells, RIGHT, buff=0.05)
        lb.stretch_to_fit_height(self.cells.get_height() * 1.1)
        rb.stretch_to_fit_height(self.cells.get_height() * 1.1)
        self.brackets = VGroup(lb, rb)
        self.add(self.brackets)
        self.center()


# ============================================================
# Timeline — 横向时间线
# ============================================================

class Timeline(VGroup):
    """
    横向时间线可视化。
    
    用法:
        tl = Timeline([
            ("1951", "Fix & Hodges", BLUE),
            ("1967", "Cover-Hart", GREEN),
            ("2017", "FAISS", RED),
        ])
    """
    def __init__(
        self,
        events,
        width=12.0,
        dot_radius=0.12,
        year_font_size=22,
        label_font_size=16,
        line_color="#828997",
        **kwargs,
    ):
        super().__init__(**kwargs)
        n = len(events)
        line = Line(LEFT * width / 2, RIGHT * width / 2, color=line_color, stroke_width=2)
        self.add(line)

        self.dots = VGroup()
        self.labels = VGroup()
        for i, event in enumerate(events):
            year_text, label_text, color = event[:3]
            x = -width / 2 + (i / max(n - 1, 1)) * width

            dot = Dot([x, 0, 0], radius=dot_radius, color=color)
            tick = Line([x, -0.2, 0], [x, 0.2, 0], color=color, stroke_width=2)
            year = Text(str(year_text), font_size=year_font_size, color=color, weight=BOLD)
            year.next_to(dot, DOWN, buff=0.25)
            label = Text(str(label_text), font_size=label_font_size, color=line_color)
            label.next_to(year, DOWN, buff=0.1)

            group = VGroup(dot, tick, year, label)
            self.dots.add(dot)
            self.labels.add(group)
            self.add(group)


# ============================================================
# DataFlowArrow — 数据流箭头（带标签）
# ============================================================

class DataFlowArrow(VGroup):
    """带标签的数据流箭头"""
    def __init__(self, start, end, label_text="", color=WHITE, font_size=20, **kwargs):
        super().__init__(**kwargs)
        arrow = Arrow(start, end, color=color, stroke_width=2)
        self.arrow = arrow
        self.add(arrow)

        if label_text:
            label = Text(label_text, font_size=font_size, color=color)
            label.next_to(arrow, UP, buff=0.1)
            self.label = label
            self.add(label)


# ============================================================
# ComparisonBars — 对比柱状图
# ============================================================

class ComparisonBars(VGroup):
    """
    对比柱状图。
    
    用法:
        bars = ComparisonBars([
            ("Bayes", 100, GREEN),
            ("KNN", 50, BLUE),
        ])
    """
    def __init__(
        self,
        data,
        max_height=4.0,
        bar_width=1.5,
        bar_spacing=2.0,
        font_size=24,
        **kwargs,
    ):
        super().__init__(**kwargs)
        max_val = max(v for _, v, _ in data)
        self.bars = VGroup()
        self.labels = VGroup()

        for i, (name, value, color) in enumerate(data):
            h = (value / max_val) * max_height
            bar = Rectangle(width=bar_width, height=h, fill_color=color,
                             fill_opacity=0.85, stroke_color=color, stroke_width=1)
            bar.shift(RIGHT * i * bar_spacing)

            val_label = Text(str(value), font_size=font_size, color=WHITE, weight=BOLD)
            val_label.next_to(bar, UP, buff=0.2)

            name_label = Text(name, font_size=int(font_size * 0.7), color="#828997")
            name_label.next_to(bar, DOWN, buff=0.3)

            group = VGroup(bar, val_label, name_label)
            self.bars.add(bar)
            self.labels.add(group)
            self.add(group)

        # 底部对齐
        for g in self.labels:
            g[0].align_to(DOWN * 1.5, DOWN)
        self.center()


# ============================================================
# ScatterPlot — 二分类散点图
# ============================================================

class ScatterPlot(VGroup):
    """
    二分类散点图。
    
    用法:
        sp = ScatterPlot(n_points=30, seed=42)
    """
    def __init__(
        self,
        n_points=25,
        seed=42,
        class_a_color="#5b9bd5",
        class_b_color="#eb5757",
        dot_radius=0.1,
        x_range=(-5, 5),
        y_range=(-3, 3),
        **kwargs,
    ):
        super().__init__(**kwargs)
        np.random.seed(seed)

        self.class_a = VGroup()
        self.class_b = VGroup()

        for _ in range(n_points):
            x = np.random.uniform(*x_range)
            y = np.random.uniform(*y_range)
            is_a = (x + y + np.random.normal(0, 1.5)) > 0
            dot = Dot([x, y, 0], radius=dot_radius,
                       color=class_a_color if is_a else class_b_color,
                       fill_opacity=0.85)
            if is_a:
                self.class_a.add(dot)
            else:
                self.class_b.add(dot)

        self.all_dots = VGroup(*self.class_a, *self.class_b)
        self.add(self.all_dots)

    def get_k_nearest(self, query_point, k=3):
        """返回距查询点最近的 k 个点"""
        dists = []
        for d in self.all_dots:
            dist = np.linalg.norm(d.get_center()[:2] - np.array(query_point[:2]))
            dists.append((dist, d))
        dists.sort(key=lambda x: x[0])
        return [d for _, d in dists[:k]]


# ============================================================
# BruteForceGrid — 暴力搜索扫描动画
# ============================================================

class BruteForceGrid(VGroup):
    """
    暴力搜索网格：逐格扫描 + 高亮 + 复杂度标注。
    
    用法:
        grid = BruteForceGrid(rows=4, cols=8)
        # 在 Scene 中: grid.animate_scan(self, speed=0.15)
    """
    def __init__(self, rows=4, cols=8, cell_size=0.5, fill_color="#252540",
                 grid_color="#2d2d44", scan_color="#eb5757", **kwargs):
        super().__init__(**kwargs)
        self.scan_color = scan_color
        self.cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(side_length=cell_size, fill_color=fill_color, fill_opacity=0.5,
                             stroke_color=grid_color, stroke_width=0.5)
                sq.move_to([c * (cell_size + 0.05) - cols * cell_size / 2.5,
                            r * (cell_size + 0.05) - rows * cell_size / 3, 0])
                self.cells.add(sq)
        self.add(self.cells)

    def animate_scan(self, scene, n_cells=None, speed_start=0.2, speed_end=0.05):
        """在 Scene 中播放扫描动画"""
        n = n_cells or len(self.cells)
        scanner = self.cells[0].copy().set_stroke(self.scan_color, 3).set_fill(opacity=0)
        scene.add(scanner)
        for i in range(min(n, len(self.cells))):
            rt = speed_start + (speed_end - speed_start) * i / max(n - 1, 1)
            scene.play(scanner.animate.move_to(self.cells[i]),
                       self.cells[i].animate.set_fill(self.scan_color, 0.12), run_time=rt)
        scene.remove(scanner)

    def get_complexity_label(self, tex=r"O(n \cdot d)", color="#eb5757", font_size=56):
        """返回复杂度 LaTeX 标签"""
        return MathTex(tex, font_size=font_size, color=color)


# ============================================================
# KDTreePartition — KD-Tree 空间切割动画
# ============================================================

class KDTreePartition(VGroup):
    """
    KD-Tree 递归空间分割可视化。
    
    用法:
        kdt = KDTreePartition(width=8, height=5)
        kdt.add_cut(scene, [-0.5, -2.5], [-0.5, 2.5], GREEN, "x")
    """
    def __init__(self, width=8, height=5, n_dots=30, seed=42,
                 dot_color="#5b9bd5", **kwargs):
        super().__init__(**kwargs)
        self.boundary = Rectangle(width=width, height=height,
                                   stroke_color="#828997", stroke_width=1)
        self.add(self.boundary)

        np.random.seed(seed)
        self.dots = VGroup(*[
            Dot([np.random.uniform(-width/2+0.3, width/2-0.3),
                 np.random.uniform(-height/2+0.3, height/2-0.3), 0],
                radius=0.06, color=dot_color, fill_opacity=0.7)
            for _ in range(n_dots)
        ])
        self.add(self.dots)
        self.cuts = VGroup()

    def add_cut(self, scene, start, end, color, axis_label="x", run_time=0.7):
        """添加一刀切割动画"""
        cut = Line(start, end, color=color, stroke_width=2.5, stroke_opacity=0.8)
        dim_lbl = MathTex(axis_label, font_size=18, color=color)
        dim_lbl.next_to(cut.get_center(), UR, 0.08)
        self.cuts.add(cut)
        self.add(cut)
        scene.play(Create(cut, run_time=run_time), FadeIn(dim_lbl, run_time=0.3))
        scene.wait(0.15)
        scene.play(FadeOut(dim_lbl, run_time=0.2))

    def highlight_region(self, scene, center, width, height, color="#6fcf97"):
        """高亮搜索区域"""
        rect = Rectangle(width=width, height=height, fill_color=color,
                          fill_opacity=0.08, stroke_color=color, stroke_width=1.5)
        rect.move_to(center)
        scene.play(FadeIn(rect), run_time=0.7)
        return rect


# ============================================================
# DimensionComparison — 维度灾难可视化
# ============================================================

class DimensionComparison(VGroup):
    """
    维度灾难对比：1D线段 vs 2D圆 vs nD膨胀。
    
    用法:
        dc = DimensionComparison()
        dc.animate_expansion(scene)  # 在 Scene 中播放
    """
    def __init__(self, spacing=3.5, **kwargs):
        super().__init__(**kwargs)
        # 1D
        line_space = Line(LEFT*1.2, RIGHT*1.2, color="#828997", stroke_width=1.5)
        line_neighbor = Line(LEFT*0.3, RIGHT*0.3, color="#6fcf97", stroke_width=6)
        self.dim1 = VGroup(line_space, line_neighbor)
        self.dim1_label = Text("1D", font_size=22, color="#6fcf97", weight=BOLD)

        # 2D
        sq2 = Square(2.0, stroke_color="#828997", stroke_width=1.5)
        c2 = Circle(radius=0.45, color="#f2994a", fill_opacity=0.15, stroke_width=2)
        self.dim2 = VGroup(sq2, c2)
        self.dim2_label = Text("2D", font_size=22, color="#f2994a", weight=BOLD)

        # nD (will expand)
        sqn = Square(2.0, stroke_color="#828997", stroke_width=1.5)
        self.dim_n_neighbor = Square(0.3, color="#eb5757", fill_opacity=0.15, stroke_width=2)
        self.dim_n_neighbor.move_to(sqn)
        self.dim_n = VGroup(sqn, self.dim_n_neighbor)
        self.dim_n_label = Text("100D", font_size=22, color="#eb5757", weight=BOLD)

        groups = VGroup(
            VGroup(self.dim1, self.dim1_label),
            VGroup(self.dim2, self.dim2_label),
            VGroup(self.dim_n, self.dim_n_label),
        )
        for g in groups:
            g[0][1].move_to(g[0][0])
            g[1].next_to(g[0], UP, 0.15)
        groups.arrange(RIGHT, buff=1.2)
        self.add(groups)
        self.groups = groups

    def animate_expansion(self, scene):
        """动画: 100D 邻域膨胀到几乎覆盖全空间"""
        target = self.dim_n[0].copy()  # outer square
        target.set_fill("#eb5757", 0.3).set_stroke("#eb5757", 2)
        scene.play(Transform(self.dim_n_neighbor, target), run_time=1.5,
                   rate_func=rate_functions.ease_out_expo)
        scene.play(Flash(self.dim_n_neighbor, color="#eb5757",
                          line_length=0.3, flash_radius=1.5), run_time=0.5)


# ============================================================
# HashBuckets — LSH 哈希桶可视化
# ============================================================

class HashBuckets(VGroup):
    """
    LSH 分桶动画模版。
    
    用法:
        hb = HashBuckets(n_buckets=4)
        hb.animate_fill(scene)
        hb.highlight_bucket(scene, index=2)
    """
    def __init__(self, n_buckets=4, bucket_width=2.0, bucket_height=2.2,
                 colors=None, **kwargs):
        super().__init__(**kwargs)
        if colors is None:
            colors = ["#5b9bd5", "#eb5757", "#6fcf97", "#f2994a",
                      "#bb6bd9", "#56ccf2", "#f2c94c", "#828997"][:n_buckets]
        self.colors = colors
        self.bucket_groups = VGroup()
        for i in range(n_buckets):
            b = RoundedRectangle(width=bucket_width, height=bucket_height,
                                  corner_radius=0.12, stroke_color=colors[i],
                                  stroke_width=1.5, fill_color="#1a1a30", fill_opacity=0.5)
            b.shift(RIGHT * (i * (bucket_width + 0.3) - (n_buckets - 1) * (bucket_width + 0.3) / 2))
            bl = MathTex(f"h={i}", font_size=20, color=colors[i]).next_to(b, UP, 0.1)
            self.bucket_groups.add(VGroup(b, bl))
        self.add(self.bucket_groups)

    def animate_fill(self, scene, dots_per_bucket=4, drop_height=2.5, speed=0.1):
        """每个桶里落入随机点"""
        np.random.seed(42)
        for bi, bg in enumerate(self.bucket_groups):
            bc = bg[0].get_center()
            for j in range(dots_per_bucket):
                dot = Dot([bc[0] + np.random.uniform(-0.5, 0.5), bc[1] + drop_height, 0],
                          radius=0.08, color=self.colors[bi], fill_opacity=0.85)
                ty = bc[1] + np.random.uniform(-0.7, 0.7)
                tx = bc[0] + np.random.uniform(-0.5, 0.5)
                scene.play(dot.animate.move_to([tx, ty, 0]),
                           run_time=speed, rate_func=rate_functions.ease_in_quad)

    def highlight_bucket(self, scene, index, color="#f2c94c"):
        """高亮一个桶"""
        hl = SurroundingRectangle(self.bucket_groups[index][0],
                                   color=color, stroke_width=2.5, buff=0.08)
        scene.play(Create(hl), run_time=0.7)
        return hl


# ============================================================
# FormulaDerivation — 逐步公式推导
# ============================================================

class FormulaDerivation(VGroup):
    """
    逐步推导公式动画：每一步依次出现。
    
    用法:
        fd = FormulaDerivation([
            (r"R^*", GREEN),
            (r"\leq", WHITE),
            (r"R_{1\text{-NN}}", WHITE),
            (r"\leq", WHITE),
            (r"2R^*", YELLOW),
        ])
        fd.animate_steps(scene)
    """
    def __init__(self, steps, font_size=56, spacing=0.25, **kwargs):
        super().__init__(**kwargs)
        self.step_mobs = VGroup()
        for tex, color in steps:
            m = MathTex(tex, font_size=font_size, color=color)
            self.step_mobs.add(m)
        self.step_mobs.arrange(RIGHT, buff=spacing)
        self.add(self.step_mobs)

    def animate_steps(self, scene, step_time=0.8, pause=0.3):
        """逐步展示每个公式部分"""
        for m in self.step_mobs:
            scene.play(Write(m), run_time=step_time)
            scene.wait(pause)

    def add_highlight_box(self, scene, color="#6fcf97", buff=0.25):
        """给整个推导加高亮框"""
        box = SurroundingRectangle(self.step_mobs, color=color,
                                    stroke_width=2, buff=buff)
        scene.play(Create(box), run_time=0.8)
        return box

    def add_brace(self, scene, mob_index, text, direction=DOWN, color="#f2c94c"):
        """给某一步加 Brace + 文字标注"""
        brace = Brace(self.step_mobs[mob_index], direction, color=color)
        label = brace.get_text(text, font_size=24, color=color)
        scene.play(GrowFromCenter(brace), FadeIn(label), run_time=0.8)
        return VGroup(brace, label)
