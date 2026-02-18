# CST8508 Machine Vision — Quiz Answers with All Options and Explanations

---

## Question 1

**What is Machine Vision primarily used for?**

### Options

- Gaming development
- 3D animation
- ✅ Imaging-based automatic inspection and analysis
- Web design

### Explanation

Machine Vision is mainly used for automatic inspection and analysis using images. It allows machines to detect defects, recognize objects, and make automated decisions in industrial and real-world applications.

---

## Question 2

**What are morphological operations in image processing typically used for?**

### Options

- ✅ Processing images based on shapes
- Enhancing image resolution
- Color corrections
- Image compression

### Explanation

Morphological operations (erosion, dilation, opening, closing) operate on object shapes and structures in binary or grayscale images to remove noise or improve object boundaries.

---

## Question 3

**Which stage in machine vision workflow deals with analysis and manipulation of images?**

### Options

- Neural Networks
- Interpretation/Action
- Image Acquisition
- ✅ Image Processing

### Explanation

Image processing is the stage where filtering, enhancement, transformation, and analysis of images occur before interpretation.

---

## Question 4

**Which is the chart that shows how many pixels in an image have a particular brightness level?**

### Options

- ROC curve
- ✅ Image Histogram
- Feature Map
- Image Translation

### Explanation

An image histogram shows the distribution of brightness values in an image:

- X-axis → brightness level
- Y-axis → number of pixels

---

## Question 5

**Select the stages involved in Canny edge detection?**

### Options

- Noise Reduction
- Edge tracking by Hysteresis
- Gradient Calculation
- ✅ All of the above

### Explanation

Canny edge detection includes noise reduction, gradient calculation, double thresholding, and edge tracking by hysteresis.

---

## Question 6

**Which stage in Canny edge detection applies two thresholds (high and low) to classify edges into strong, weak and non-edges?**

### Options

- Noise Reduction
- Gradient Calculation
- ✅ Double Thresholding
- Edge Tracking by Hysteresis

### Explanation

Double thresholding classifies edges into strong, weak, and non-edges using two threshold values.

---

## Question 7

**The horizontal axis of image histogram shows ----- ?**

### Options

- ✅ Different brightness level
- Count of pixels
- Number of channels
- Size of image

### Explanation

The horizontal axis represents intensity or brightness levels (usually 0–255).

---

## Question 8

**Which filter type smoothens image?**

### Options

- ✅ Image Blurring
- Image Sharpening
- Image Translation
- Image Segmentation

### Explanation

Blurring reduces noise and smooths images by averaging neighboring pixel values.

---

## Question 9

**Output of segmentation is typically a _____ image.**

### Options

- Color image
- Grayscale image
- ✅ Binary image
- Compressed image

### Explanation

Segmentation separates objects from background, usually producing a binary image where object and background are represented by two values.

---

## Question 10

**Which thresholding technique is used for dealing with uneven lighting issues in the images?**

### Options

- Binary Thresholding
- Image Histogram
- ✅ Adaptive Thresholding
- Double Thresholding

### Explanation

Adaptive thresholding calculates thresholds locally, making it suitable for uneven lighting conditions.

---

## Question 11

**Which is the OpenCV command used for drawing contour outlines in an image?**

### Options

- cv2.findContours()
- cv2.fillCountours()
- ✅ cv2.drawContours()
- cv2.getContours()

### Explanation

`cv2.drawContours()` is used to draw detected contours on an image.

---

## Question 12

**ORB is a fusion of _____ keypoint detector and _____ descriptor.**

### Options

- SIFT and SURF
- Harris and SIFT
- ✅ FAST keypoint detector and BRIEF descriptor
- HOG and SVM

### Explanation

ORB combines FAST for detecting keypoints and BRIEF for describing them efficiently.

---

## Question 13

**Which technique is effective for human detection in computer vision?**

### Options

- ✅ Histogram of Oriented Gradients (HOG)
- Speeded Up Robust Features (SURF)
- Features from Accelerated Segment Test (FAST)

### Explanation

HOG captures gradient orientation patterns that match human body structures, making it effective for pedestrian detection.

---

## Question 14

**Which layer in CNN is responsible for down sampling of feature maps?**

### Options

- Convolutional Layer
- ✅ Pooling Layer
- Fully-connected Layer
- Output Layer

### Explanation

Pooling layers reduce spatial dimensions and computation while preserving important features.

---

## Question 15

**----- measures the proportion of total predictions (both positive and negative) that the model got correct?**

### Options

- Precision
- ✅ Accuracy
- F1 Score

### Explanation

Accuracy measures overall correctness:

Accuracy = Correct Predictions / Total Predictions
