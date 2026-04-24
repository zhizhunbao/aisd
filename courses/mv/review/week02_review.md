# Week 2 Review — Fundamentals of Image Processing

> 📋 Based on instructor's revision topics:
> **Segmentation, Global and adaptive thresholding, Contour object detection**

---

## Q1: What is Image Segmentation?

**Answer:**

Segmentation **extracts** objects from an image for further processing. The output is typically a **binary image** — an image with values of zero and one (black and white).

- **1** indicates the piece of image we wanted to use
- **0** indicates everything else
- Binary image acts as a **mask** for the area of the source image

---

## Q2: What is global vs. adaptive thresholding?

**Answer:**

| Feature | Global (Simple) Thresholding | Adaptive Thresholding |
|---|---|---|
| **Threshold value** | The **same threshold** is applied for every pixel | Calculates a threshold for **each sub-region** |
| **Mechanism** | If pixel value ≤ threshold → 0, otherwise → max value | Uses **local neighborhood** to determine threshold |
| **Best for** | Uniform lighting | **Uneven lighting** |
| **Methods** | Simple comparison | `adaptive_mean` or `adaptive_gaussian` |
| **Result** | May fail with varying illumination | Better results for images with varying illumination |

**Key insight:** Binary thresholding is **not ideal** for uneven lighting — adaptive thresholding counteracts this by using local neighborhoods.

---

## Q3: What is a contour? How does it relate to edge detection?

**Answer:**

A **contour** is a curve that joins a set of points enclosing an area having the **same color or intensity**.

| Aspect | Contours | Edge Detection |
|---|---|---|
| **Output** | Closed path | May be open edges |
| **Purpose** | Shape analysis, object detection | Finding intensity changes |
| **Relationship** | Similar to edge detection but edges must form a **closed path** |

---

## Q4: What is the contour detection pipeline?

**Answer:**

| Step | Operation |
|---|---|
| 1 | **Original color image** → Convert to grayscale |
| 2 | **Grayscale image** → Create binary image with thresholding |
| 3 | **Binary image** → Detect contours using `cv2.findContours()` |
| 4 | **Draw contours** on original image using `cv2.drawContours()` |

**Key functions:**

- `cv2.findContours()` → Returns: **Contours** (list of boundary points) and **Hierarchy** (parent-child relationship)
- `cv2.drawContours()` → Draws outlines (`thickness ≥ 0`) or fills area (`thickness < 0`)

---

## Q5: What are the steps of Canny edge detection?

**Answer:**

| Step | Name | Description |
|---|---|---|
| 1 | **Noise Reduction** | Smooth image with Gaussian filter |
| 2 | **Gradient Calculation** | Find intensity gradients using Sobel kernel (horizontal + vertical) |
| 3 | **Non-maximum Suppression** | Thin out edges by suppressing non-maximum gradient values |
| 4 | **Double Thresholding** | Classify edges into strong, weak, and non-edges |
| 5 | **Edge Tracking by Hysteresis** | Connect weak edges to strong edges; discard isolated weak edges |

---

## Q6: What are morphological operations?

**Answer:**

Morphological operations process images based on **shapes**.

| Operation | Rule | Effect | Use Case |
|---|---|---|---|
| **Erosion** | Pixel = 1 only if **all** pixels under kernel = 1 | Shrinks objects | Remove small white noise, detach connected objects |
| **Dilation** | Pixel = 1 if **at least one** pixel under kernel = 1 | Expands objects | Join broken parts |
| **Opening** | Erosion → Dilation | Removes small objects | Noise removal without losing object shape |
| **Closing** | Dilation → Erosion | Fills small holes | Close small gaps inside objects |
