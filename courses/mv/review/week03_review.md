# Week 3 Review — Feature Detection and Description

> 📋 Based on instructor's revision topics:
> **SURF, SIFT, ORB detectors, Feature matching, Canny edge detection**

---

## Q1: What is SIFT? What are its main steps?

**SIFT (Scale-Invariant Feature Transform)** — invariant to **scaling** and **rotation**, partially invariant to **illumination** and **3D viewpoint** changes.

| Step | Name | Description |
|---|---|---|
| 1 | Scale-space Extrema Detection | Search for extrema in multi-scale DoG (Difference of Gaussians) images |
| 2 | Keypoint Localization | Refine by eliminating low-contrast and edge points |
| 3 | Orientation Assignment | Assign orientation based on local gradient directions → rotation invariance |
| 4 | Keypoint Descriptor | Generate **128-dim feature vector** |
| 5 | Feature Matching | Compare descriptors using Euclidean distance |

---

## Q2: SIFT vs SURF vs ORB Comparison

| Feature | SIFT | SURF | ORB |
|---|---|---|---|
| Speed | Slow | Medium | **Fast** |
| Descriptor | 128-dim float | 64-dim float | **Binary** |
| Detection | DoG | Hessian matrix | FAST |
| Scale invariant | ✅ | ✅ | ✅ |
| Rotation invariant | ✅ | ✅ | ✅ |
| Real-time | ❌ | ⚠️ | ✅ |
| Patent | Expired | Expired | **Free** |

**SURF** is faster than SIFT (integral images + box filters), with a 64-dim descriptor.
**ORB** = FAST (detection) + BRIEF (description), free and fastest.

---

## Q3: What is Feature Matching?

**Feature matching** identifies similar features across different images by computing distances between descriptors.

| Distance Metric | Use |
|---|---|
| Euclidean | SIFT/SURF (float descriptors) |
| Hamming | ORB (binary descriptors) |

| Matching Method | Description |
|---|---|
| **Brute Force** | Compare every feature pair exhaustively |
| **Brute Force KNN** | K-nearest neighbor brute force matching |
| **FLANN** | Fast Library for Approximate Nearest Neighbors |

**Applications:** Panorama stitching, motion tracking, object recognition, 3D modeling

---

## Q4: How are image gradients calculated?

| Formula | Description |
|---|---|
| ∇F = [δF/δx, δF/δy] | Gradient vector |
| θ = tan⁻¹(δF/δy ÷ δF/δx) | Gradient direction |
| ‖∇F‖ = √((δF/δx)² + (δF/δy)²) | Gradient magnitude |

**Example:** δF/δx=50, δF/δy=50 → Magnitude=70.1, Angle=45°

---

## Q5: What is HOG?

**HOG (Histogram of Oriented Gradients)** is particularly effective for **pedestrian/human detection**. It creates a unique representation of human body shape by analyzing gradient and edge orientations in local image regions.

### HOG Pipeline:

| Step | Description |
|---|---|
| **1. Preprocessing** | Resize image to fixed size |
| **2. Gradient computation** | Compute horizontal & vertical gradients |
| **3. Cell histograms** | Divide image into cells, build orientation histogram per cell |
| **4. Block normalization** | Normalize histograms across overlapping blocks for illumination invariance |
| **5. Feature vector** | Concatenate all block histograms into final descriptor |

**Key properties:**
- Captures **shape and edge structure** without precise spatial information
- Robust to **small deformations**
- Often combined with **SVM classifier** for detection
