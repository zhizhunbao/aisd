# Machine Vision Concepts Reference

## Image Fundamentals

**Digital Image:** 2D array of pixels with intensity values

- Grayscale: Single channel (0-255)
- RGB: Three channels (Red, Green, Blue)
- Resolution: Width × Height pixels
- Bit depth: Bits per pixel (8-bit, 16-bit)

**Coordinate System:** Origin (0,0) at top-left, x-axis right, y-axis down

## Image Preprocessing

### Filtering

**Smoothing (Low-pass):**

- Gaussian: Weighted average, reduces noise
- Median: Replaces with median, removes salt-pepper noise
- Bilateral: Edge-preserving smoothing

**Sharpening (High-pass):**

- Laplacian: Detects rapid intensity changes
- Unsharp masking: Original + (Original - Blurred)

### Morphological Operations

**Basic Operations:**

- Erosion: Shrinks objects, removes noise
- Dilation: Expands objects, fills holes
- Opening: Erosion then dilation (removes small objects)
- Closing: Dilation then erosion (fills small holes)

**Structuring Element:** Kernel shape (rectangle, ellipse, cross)

## Edge Detection

**Gradient-based:**

- Sobel: Approximates gradient with 3×3 kernels
- Prewitt: Similar to Sobel, different weights
- Scharr: More accurate gradient estimation

**Canny Edge Detector:**

1. Gaussian smoothing
2. Gradient calculation
3. Non-maximum suppression
4. Double thresholding
5. Edge tracking by hysteresis

## Feature Extraction

### Corner Detection

**Harris Corner:**

```
R = det(M) - k(trace(M))²
M = Σ [Ix² IxIy]
      [IxIy Iy²]
```

**Shi-Tomasi:** Uses minimum eigenvalue instead

### Blob Detection

**LoG (Laplacian of Gaussian):** Detects regions of rapid intensity change

**DoG (Difference of Gaussians):** Approximates LoG, faster computation

### Feature Descriptors

**SIFT (Scale-Invariant Feature Transform):**

- Scale-space extrema detection
- Keypoint localization
- Orientation assignment
- Descriptor generation (128-dim)
- Patent restrictions (now expired)

**ORB (Oriented FAST and Rotated BRIEF):**

- **FAST**: Features from Accelerated Segment Test (快速角点检测)
  - Finds "interesting points" (corners, edge intersections)
  - Very fast corner detection
- **BRIEF**: Binary Robust Independent Elementary Features (二进制描述符)
  - 256-bit binary string describing texture around each feature
  - Much faster than SIFT/SURF floating-point descriptors
- **Oriented + Rotated**: Rotation invariance (旋转不变性)
  - Can recognize same feature even after image rotation

**ORB Advantages:**
- Fast (比 SIFT、SURF 快很多)
- Free and open source (无专利限制)
- Robust to rotation and moderate lighting changes
- Good for real-time applications

**What is a Descriptor?**
- A "fingerprint" of a feature point (特征点的"身份证")
- Sequence of numbers describing texture around that point
- Example: `10110010 01101001 11010010 ...` (256 bits for ORB)
- Allows matching same point across different images

### Feature Matching

**BFMatcher (Brute-Force Matcher / 暴力匹配器):**
- Compares each feature in image1 with ALL features in image2
- Example: 500 points × 500 points = 250,000 comparisons
- Best for accuracy, slower for large feature sets

**FLANN Matcher (Fast Library for Approximate Nearest Neighbors):**
- Uses KD-tree or hierarchical clustering
- Much faster for large datasets (>1000 features)
- Approximate matching (may miss some matches)

**Distance Metrics:**
- `cv2.NORM_HAMMING`: For binary descriptors (ORB, BRIEF)
  - Hamming distance = count of different bits
  - Example: `10110010` vs `10010110` → 3 bits differ → distance=3
- `cv2.NORM_L2`: For floating-point descriptors (SIFT, SURF)

**crossCheck Parameter:**
- `crossCheck=True`: Bidirectional verification (双向验证)
- Only keeps match if A's best match is B AND B's best match is A
- Reduces false matches ("mutual selection" / "双向选择")

**Match Object Properties:**
- `queryIdx`: Index of feature in first image
- `trainIdx`: Index of matched feature in second image
- `distance`: Similarity measure (smaller = better match)

## Image Segmentation

### Thresholding

**Global:** Single threshold for entire image

```
Binary: I(x,y) > T → 255, else 0
```

**Adaptive:** Local threshold based on neighborhood

**Otsu's Method:** Automatically finds optimal threshold

### Region-based

**Watershed:** Treats image as topographic surface
**Region Growing:** Starts from seed, adds similar neighbors

### Contour-based

**Active Contours (Snakes):** Energy minimization
**GrabCut:** Interactive foreground extraction

## Object Detection

### Template Matching

Cross-correlation between template and image

```
R(x,y) = Σ [T(x',y') · I(x+x', y+y')]
```

### Cascade Classifiers

**Haar Cascades:** Fast face/object detection

- Haar-like features
- AdaBoost training
- Cascade of weak classifiers

### Modern Approaches

**HOG (Histogram of Oriented Gradients):** Pedestrian detection
**Deep Learning:** CNN-based (YOLO, SSD, Faster R-CNN)

## Camera Calibration

### Intrinsic Parameters

- Focal length (fx, fy)
- Principal point (cx, cy)
- Distortion coefficients (k1, k2, p1, p2)

### Extrinsic Parameters

- Rotation matrix (R)
- Translation vector (t)

**Calibration Process:**

1. Capture checkerboard images
2. Detect corners
3. Solve PnP problem
4. Optimize parameters

## Color Spaces

**RGB:** Red, Green, Blue (device-dependent)
**HSV:** Hue, Saturation, Value (intuitive for color selection)
**LAB:** Lightness, A (green-red), B (blue-yellow) (perceptually uniform)
**YCrCb:** Luminance + Chrominance (used in JPEG)

## Performance Metrics

**Accuracy:** (TP + TN) / Total
**Precision:** TP / (TP + FP)
**Recall:** TP / (TP + FN)
**F1-Score:** 2 × (Precision × Recall) / (Precision + Recall)
**IoU:** Intersection over Union for object detection
