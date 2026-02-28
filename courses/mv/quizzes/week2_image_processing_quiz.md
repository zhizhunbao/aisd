# Week 2: Fundamentals of Image Processing — Quiz

---

## Multiple Choice Questions (MCQ)

Question 1 (1 point)
What is the primary purpose of image filtering (blurring) in image processing?

Question 1 options:
A) To increase image resolution
B) To reduce noise and smooth the image by averaging neighboring pixels
C) To add artistic effects
D) To compress the image file size

Question 2 (1 point)
Which blurring method is most effective for removing salt-and-pepper noise?

Question 2 options:
A) Average (Mean) blur
B) Gaussian blur
C) Median blur
D) Bilateral filter

Question 3 (1 point)
What are the five stages of the Canny edge detection algorithm, in order?

Question 3 options:
A) Gradient → Thresholding → NMS → Smoothing → Tracking
B) Gaussian smoothing → Gradient calculation → Non-maximum suppression → Double thresholding → Hysteresis edge tracking
C) Sobel → Laplacian → Gaussian → Thresholding → Morphology
D) Noise removal → Segmentation → Classification → Output → Validation

Question 4 (1 point)
In the Canny edge detector, what is the purpose of Non-Maximum Suppression (NMS)?

Question 4 options:
A) To remove all weak edges
B) To thin thick edge bands down to 1-pixel-wide lines
C) To apply the Gaussian filter
D) To connect broken edges

Question 5 (1 point)
What does an image histogram represent?

Question 5 options:
A) The spatial frequency content of an image
B) The distribution of pixel intensity values, with brightness on X-axis and pixel count on Y-axis
C) The color balance between RGB channels
D) The compression ratio of the image

Question 6 (1 point)
When should you use adaptive thresholding instead of simple (global) thresholding?

Question 6 options:
A) When the image is very small
B) When the image has uniform lighting conditions
C) When the image has varying illumination across different regions
D) When processing color images

Question 7 (1 point)
What is the correct order of operations in morphological "Opening"?

Question 7 options:
A) Dilation followed by erosion
B) Erosion followed by dilation
C) Two rounds of dilation
D) Two rounds of erosion

Question 8 (1 point)
In erosion, when is an output pixel set to 1?

Question 8 options:
A) If at least one pixel under the kernel is 1
B) If the center pixel under the kernel is 1
C) If all pixels under the kernel are 1
D) If more than half the pixels under the kernel are 1

Question 9 (1 point)
What does the affine transformation formula y = Ax + b guarantee to preserve?

Question 9 options:
A) Pixel intensity values
B) Image file size
C) Straight lines and parallelism
D) Color information

Question 10 (1 point)
Which of the following is NOT one of the nine key stages of digital image processing mentioned in the slides?

Question 10 options:
A) Image Acquisition
B) Segmentation
C) Neural Network Training
D) Morphological Processing

---

## True/False Questions

Question 11 (1 point)
Sharpening an image reduces noise by smoothing pixel values.

Question 11 options:
True
False

Question 12 (1 point)
The Canny edge detector requires two threshold parameters: a low threshold and a high threshold.

Question 12 options:
True
False

Question 13 (1 point)
In morphological closing, dilation is performed first, followed by erosion.

Question 13 options:
True
False

Question 14 (1 point)
A Gaussian blur kernel assigns equal weights to all pixels in the neighborhood.

Question 14 options:
True
False

Question 15 (1 point)
All nine stages of image processing must be applied to every image processing task.

Question 15 options:
True
False

Question 16 (1 point)
Median filtering computes the average of neighborhood pixels.

Question 16 options:
True
False

Question 17 (1 point)
In the Canny algorithm, hysteresis edge tracking keeps weak edges only if they are connected to strong edges.

Question 17 options:
True
False

---

## Short Answer / Coding Questions

Question 18 (2 points)
Explain the trade-off between blurring and sharpening. Why might you use both in sequence when processing an image?

Question 19 (2 points)
Given a 3×3 region of pixel values: `[[80, 90, 85], [95, 100, 110], [105, 115, 120]]`, calculate the output of applying a 3×3 average filter to the center pixel.

---

## Answer Key

1. **B** — Blurring reduces noise by averaging neighboring pixels, which smooths out rapid intensity changes. It softens the image, reducing detail and noise.

2. **C** — Median blur replaces each pixel with the median of its neighborhood, which effectively removes salt-and-pepper noise (extreme outlier values) without smearing edges as much as average blur.

3. **B** — The five stages in order are: (1) Gaussian smoothing for noise reduction, (2) Gradient calculation using Sobel kernels, (3) Non-maximum suppression to thin edges, (4) Double thresholding to classify strong/weak/non-edges, (5) Hysteresis edge tracking to connect weak edges to strong ones.

4. **B** — NMS thins the thick gradient response bands produced by Sobel into precise 1-pixel-wide edge lines. It keeps only the local maximum gradient value along the gradient direction.

5. **B** — A histogram shows the distribution of pixel intensities: the X-axis represents brightness levels (0-255), the Y-axis shows how many pixels have each brightness value. Left-skewed = dark image; right-skewed = bright.

6. **C** — Adaptive thresholding computes a different threshold for each pixel based on its local neighborhood, which handles varying illumination. Simple thresholding uses one global value and fails when lighting is uneven.

7. **B** — Opening = erosion followed by dilation. Erosion first removes small noise, then dilation restores the object's shape. Closing (A) is the opposite: dilation first, then erosion.

8. **C** — In erosion, the output pixel is 1 only if ALL pixels under the kernel are 1. If any pixel is 0, the output is 0. This shrinks white regions and removes small white noise.

9. **C** — Affine transformations preserve collinearity (points on a line remain on a line) and parallelism (parallel lines remain parallel). They include translation, rotation, scaling, and shearing.

10. **C** — Neural Network Training is not one of the nine stages. The nine stages are: Acquisition, Enhancement, Restoration, Morphological Processing, Segmentation, Object Recognition, Representation & Description, Compression, and Color Image Processing.

11. **False** — Sharpening ENHANCES edges and details by amplifying intensity differences between adjacent pixels. This actually amplifies noise rather than reducing it. Blurring (not sharpening) reduces noise.

12. **True** — Canny uses two thresholds: a high threshold to identify strong edges and a low threshold to identify weak edges. Weak edges connected to strong edges are kept; isolated weak edges are discarded.

13. **True** — Closing = dilation first (fills small holes, connects gaps), then erosion (restores shape). This removes small black holes inside foreground objects.

14. **False** — A Gaussian kernel assigns higher weights to the center pixel and lower weights to surrounding pixels, following a Gaussian (bell curve) distribution. An average filter assigns equal weights.

15. **False** — Based on the application, a combination of only 2-3 steps may suffice. Not all nine stages are required for every task.

16. **False** — Median filtering takes the MEDIAN (middle value when sorted) of the neighborhood pixels, not the average. This is why it's effective against salt-and-pepper noise — extreme outliers don't affect the median.

17. **True** — Hysteresis tracking examines weak edges: if a weak edge pixel is connected (adjacent) to a strong edge pixel, it is kept as a real edge. If a weak edge is isolated (not connected to any strong edge), it is discarded as noise.

18. **Sample Answer:** Blurring and sharpening are fundamentally opposing operations. Blurring smooths the image by averaging neighbors, which reduces noise but also blurs edges and fine details. Sharpening enhances edges by amplifying intensity differences, but also amplifies noise. In practice, a common workflow is to first blur the image to remove noise, then apply limited sharpening to recover important edge details. This sequence gives better results than using either technique alone — the initial blur removes noise that would otherwise be amplified by sharpening.

19. **Sample Answer:** The 3×3 average filter sums all 9 values and divides by 9:
    Sum = 80 + 90 + 85 + 95 + 100 + 110 + 105 + 115 + 120 = 900
    Average = 900 / 9 = **100**
    The center pixel value remains 100 in this case because the original value equals the neighborhood average.
