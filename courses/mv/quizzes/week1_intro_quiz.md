# Week 1: Introduction to Machine Vision — Quiz

---

## Multiple Choice Questions (MCQ)

Question 1 (1 point)
What is Machine Vision primarily used for?

Question 1 options:
A) Gaming development
B) 3D animation
C) Imaging-based automatic inspection and analysis
D) Web design

Question 2 (1 point)
Which stage in the Machine Vision workflow deals with analysis and manipulation of images?

Question 2 options:
A) Neural Networks
B) Interpretation/Action
C) Image Acquisition
D) Image Processing

Question 3 (1 point)
What is the key difference between Machine Vision and Computer Vision?

Question 3 options:
A) Machine Vision is only for robots, Computer Vision is for computers
B) Machine Vision emphasizes complete end-to-end systems (hardware + software + decision), while Computer Vision focuses on image understanding algorithms
C) Computer Vision is more advanced than Machine Vision
D) There is no difference; they are the same thing

Question 4 (1 point)
Which of the following best describes a pixel in a digital image?

Question 4 options:
A) A physical dot on a camera sensor
B) A numerical representation at location (x, y) in an image
C) A color name stored in memory
D) A binary value that is always 0 or 1

Question 5 (1 point)
How many values does each pixel in an RGB color image contain?

Question 5 options:
A) 1 (single intensity value)
B) 2 (brightness and color)
C) 3 (Red, Green, Blue)
D) 4 (Red, Green, Blue, Alpha)

Question 6 (1 point)
Why might HSV color space be preferred over RGB for color-based object detection?

Question 6 options:
A) HSV uses fewer bytes per pixel
B) HSV is faster to compute
C) In HSV, the Hue channel separates color information from lighting conditions
D) HSV was invented more recently than RGB

Question 7 (1 point)
What was the significant turning point that revolutionized Machine Vision?

Question 7 options:
A) The invention of CCD sensors in the 1970s
B) The development of the SIFT algorithm in 1999
C) The rise of deep learning techniques, notably AlexNet winning ImageNet in 2012
D) The release of OpenCV in 2000

Question 8 (1 point)
Which image format supports transparency (alpha channel)?

Question 8 options:
A) JPEG
B) RAW
C) PNG
D) BMP

Question 9 (1 point)
What is the main advantage of CMOS sensors over CCD sensors?

Question 9 options:
A) Higher image quality
B) Lower noise
C) Lower power consumption and cheaper manufacturing
D) Better color accuracy

Question 10 (1 point)
In the Machine Vision workflow, what are the three basic stages in order?

Question 10 options:
A) Processing → Acquisition → Action
B) Acquisition → Interpretation → Processing
C) Image Acquisition → Image Processing → Interpretation/Action
D) Sensing → Learning → Output

---

## True/False Questions

Question 11 (1 point)
A grayscale image is represented as a 3D tensor (Height × Width × 3).

Question 11 options:
True
False

Question 12 (1 point)
OpenCV reads images in BGR channel order, not RGB.

Question 12 options:
True
False

Question 13 (1 point)
In OpenCV, pixel coordinates are accessed as image[x, y] (column, row).

Question 13 options:
True
False

Question 14 (1 point)
Deep learning completely replaced all traditional computer vision methods after 2012.

Question 14 options:
True
False

Question 15 (1 point)
JPEG is a lossless image compression format.

Question 15 options:
True
False

Question 16 (1 point)
In the HSV color space, H stands for Hue, S stands for Saturation, and V stands for Value (brightness).

Question 16 options:
True
False

Question 17 (1 point)
CCD sensors are cheaper to manufacture than CMOS sensors.

Question 17 options:
True
False

---

## Short Answer / Coding Questions

Question 18 (2 points)
Define Machine Vision in your own words and explain how it differs from simple image processing.

Question 19 (2 points)
A digital image has a pixel at location (2, 3) with the value [128, 0, 255]. In RGB color space, what does each number represent? What color would this pixel appear to be?

---

## Answer Key

1. **C** — Machine Vision is primarily used for imaging-based automatic inspection and analysis, enabling machines to detect defects, recognize objects, and make automated decisions.

2. **D** — Image Processing is the stage where filtering, enhancement, feature extraction, and analysis of images occur before interpretation.

3. **B** — Machine Vision emphasizes the complete system (hardware + software + decision-making), while Computer Vision focuses primarily on the algorithmic understanding of images. In industry, Machine Vision implies a production-ready system.

4. **B** — A pixel is a numerical representation at a specific (x, y) location in an image. In grayscale, it's a single value [0-255]; in color (RGB), it's a tuple of three values.

5. **C** — Each pixel in an RGB image contains 3 values: Red, Green, and Blue intensities, each ranging from 0 to 255.

6. **C** — In HSV, the Hue channel directly represents the color type, independent of brightness (Value) and vividness (Saturation). This makes it much easier to detect objects of a specific color regardless of lighting variations.

7. **C** — AlexNet winning ImageNet in 2012 marked the shift from hand-crafted features (SIFT, HOG) to deep learning (CNNs that automatically learn features from data).

8. **C** — PNG supports an alpha channel for transparency. JPEG does not support transparency, and RAW is an uncompressed format without alpha support.

9. **C** — CMOS sensors have lower power consumption and are cheaper to manufacture (using standard chip fabrication processes), which is why they dominate smartphones and consumer cameras.

10. **C** — The workflow is: (1) Image Acquisition (camera captures), (2) Image Processing (analyze and extract features), (3) Interpretation/Action (make decisions based on results).

11. **False** — A grayscale image is a 2D matrix (Height × Width) with a single intensity value per pixel. A color (RGB) image is a 3D tensor (H × W × 3).

12. **True** — OpenCV uses BGR (Blue, Green, Red) channel order by default. Converting to RGB is needed when displaying with matplotlib: `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`.

13. **False** — OpenCV accesses pixels as `image[y, x]` (row, column), not `image[x, y]`. This is a common source of bugs.

14. **False** — Traditional methods (template matching, thresholding, SIFT) are still used in constrained industrial environments where they are faster, cheaper, and more interpretable than deep learning.

15. **False** — JPEG uses lossy compression, meaning some image data is permanently lost during compression. PNG is lossless.

16. **True** — H = Hue (color type, 0-360°), S = Saturation (vividness, 0-1), V = Value (brightness, 0-1).

17. **False** — CCD sensors are more expensive to manufacture. CMOS sensors use standard semiconductor fabrication processes, making them significantly cheaper.

18. **Sample Answer:** Machine Vision is a technology that enables machines to interpret and understand visual information from the environment. While image processing focuses on low-level pixel manipulation (filtering, enhancement), Machine Vision encompasses the complete pipeline: capturing images (sensors), processing them to extract meaningful features, and using that information to make decisions or perform actions. It's the difference between adjusting brightness on a photo (image processing) and a factory robot detecting and rejecting defective parts (Machine Vision).

19. **Sample Answer:** In RGB color space, [128, 0, 255] means: R=128 (medium Red), G=0 (no Green), B=255 (maximum Blue). This pixel would appear as a **purple/violet** color — a mix of medium red and full blue, with no green component.
