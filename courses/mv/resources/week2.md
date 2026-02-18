# Digital Image Processing Basics

Last Updated : 22 Feb, 2023

Digital Image Processing means processing digital image by means of a digital computer. We can also say that it is a use of computer algorithms, in order to get enhanced image either to extract some useful information.

 Digital image processing is the use of algorithms and mathematical models to process and analyze digital images. The goal of digital image processing is to enhance the quality of images, extract meaningful information from images, and automate image-based tasks.

### The basic steps involved in digital image processing are:

1. Image acquisition: This involves capturing an image using a digital camera or scanner, or importing an existing image into a computer.
2. Image enhancement: This involves improving the visual quality of an image, such as increasing contrast, reducing noise, and removing artifacts.
3. Image restoration: This involves removing degradation from an image, such as blurring, noise, and distortion.
4. Image segmentation: This involves dividing an image into regions or segments, each of which corresponds to a specific object or feature in the image.
5. Image representation and description: This involves representing an image in a way that can be analyzed and manipulated by a computer, and describing the features of an image in a compact and meaningful way.
6. Image analysis: This involves using algorithms and mathematical models to extract information from an image, such as recognizing objects, detecting patterns, and quantifying features.
7. Image synthesis and compression: This involves generating new images or compressing existing images to reduce storage and transmission requirements.
8. Digital image processing is widely used in a variety of applications, including medical imaging, remote sensing, computer vision, and multimedia.

## Image processing mainly include the following steps:

1.Importing the image via image acquisition tools;
2.Analysing and manipulating the image;
3.Output in which result can be altered image or a report which is based on analysing that image.

## What is an image?

An image is defined as a two-dimensional function, **F(x,y)** , where x and y are spatial coordinates, and the amplitude of **F** at any pair of coordinates (x,y) is called the **intensity** of that image at that point. When x,y, and amplitude values of **F** are finite, we call it a  **digital image** .
In other words, an image can be defined by a two-dimensional array specifically arranged in rows and columns.
Digital Image is composed of a finite number of elements, each of which elements have a particular value at a particular location.These elements are referred to as  *picture elements,image elements,and pixels* .A *Pixel* is most widely used to denote the elements of a Digital Image.

## Types of an image

1. **BINARY IMAGE** - The binary image as its name suggests, contain only two pixel elements i.e 0 & 1,where 0 refers to black and 1 refers to white. This image is also known as Monochrome.
2. **BLACK AND WHITE IMAGE** - The image which consist of only black and white color is called BLACK AND WHITE IMAGE.
3. **8 bit COLOR FORMAT** - It is the most famous image format.It has 256 different shades of colors in it and commonly known as Grayscale Image. In this format, 0 stands for Black, and 255 stands for white, and 127 stands for gray.
4. **16 bit COLOR FORMAT** - It is a color image format. It has 65,536 different colors in it.It is also known as High Color Format. In this format the distribution of color is not as same as Grayscale image.

A 16 bit format is actually divided into three further formats which are Red, Green and Blue. That famous RGB format.

## Image as a Matrix

As we know, images are represented in rows and columns we have the following syntax in which images are represented:

![](https://media.geeksforgeeks.org/wp-content/uploads/gfg2-5.png "Click to enlarge")

The right side of this equation is digital image by definition. Every element of this matrix is called image element , picture element , or pixel.

## DIGITAL IMAGE REPRESENTATION IN MATLAB:

![](https://media.geeksforgeeks.org/wp-content/uploads/gfg3-6.png "Click to enlarge")

In MATLAB the start index is from 1 instead of 0. Therefore, f(1,1) = f(0,0).
henceforth the two representation of image are identical, except for the shift in origin.
In MATLAB, matrices are stored in a variable i.e X,x,input_image , and so on. The variables must be a letter as same as other programming languages.

## PHASES OF IMAGE PROCESSING:

1. **ACQUISITION** - It could be as simple as being given an image which is in digital form. The main work involves:
   a) Scaling
   b) Color conversion(RGB to Gray or vice-versa)
2. **IMAGE ENHANCEMENT** - It is amongst the simplest and most appealing in areas of Image Processing it is also used to extract some hidden details from an image and is subjective.
3. **IMAGE RESTORATION** - It also deals with appealing of an image but it is objective(Restoration is based on mathematical or probabilistic model or image degradation).
4. **COLOR IMAGE PROCESSING** - It deals with pseudocolor and full color image processing color models are applicable to digital image processing.
5. **WAVELETS AND MULTI-RESOLUTION PROCESSING** - It is foundation of representing images in various degrees.
6. **IMAGE COMPRESSION** -It involves in developing some functions to perform this operation. It mainly deals with image size or resolution.
7. **MORPHOLOGICAL PROCESSING** -It deals with tools for extracting image components that are useful in the representation & description of shape.
8. **SEGMENTATION PROCEDURE** -It includes partitioning an image into its constituent parts or objects. Autonomous segmentation is the most difficult task in Image Processing.
9. **REPRESENTATION & DESCRIPTION** -It follows output of segmentation stage, choosing a representation is only the part of solution for transforming raw data into processed data.
10. **OBJECT DETECTION AND RECOGNITION** -It is a process that assigns a label to an object based on its descriptor.

## OVERLAPPING FIELDS WITH IMAGE PROCESSING

![](https://media.geeksforgeeks.org/wp-content/cdn-uploads/digital-image-processing.png "Click to enlarge")

 **According to block 1** ,if input is an image and we get out image as a output, then it is termed as Digital Image Processing.
 **According to block 2** ,if input is an image and we get some kind of information or description as a output, then it is termed as Computer Vision.
 **According to block 3** ,if input is some description or code and we get image as an output, then it is termed as Computer Graphics.
 **According to block 4** ,if input is description or some keywords or some code and we get description or some keywords as a output,then it is termed as Artificial Intelligence

Advantages of Digital Image Processing:

1. Improved image quality: Digital image processing algorithms can improve the visual quality of images, making them clearer, sharper, and more informative.
2. Automated image-based tasks: Digital image processing can automate many image-based tasks, such as object recognition, pattern detection, and measurement.
3. Increased efficiency: Digital image processing algorithms can process images much faster than humans, making it possible to analyze large amounts of data in a short amount of time.
4. Increased accuracy: Digital image processing algorithms can provide more accurate results than humans, especially for tasks that require precise measurements or quantitative analysis.

### Disadvantages of Digital Image Processing:

1. High computational cost: Some digital image processing algorithms are computationally intensive and require significant computational resources.
2. Limited interpretability: Some digital image processing algorithms may produce results that are difficult for humans to interpret, especially for complex or sophisticated algorithms.
3. Dependence on quality of input: The quality of the output of digital image processing algorithms is highly dependent on the quality of the input images. Poor quality input images can result in poor quality output.
4. Limitations of algorithms: Digital image processing algorithms have limitations, such as the difficulty of recognizing objects in cluttered or poorly lit scenes, or the inability to recognize objects with significant deformations or occlusions.
5. Dependence on good training data: The performance of many digital image processing algorithms is dependent on the quality of the training data used to develop the algorithms. Poor quality training data can result in poor performance of the algorit

## REFERENCES

Digital Image Processing (Rafael c. gonzalez)

** Reference books:**

"Digital Image Processing" by Rafael C. Gonzalez and Richard E. Woods.
"Computer Vision: Algorithms and Applications" by Richard Szeliski.
"Digital Image Processing Using MATLAB" by Rafael C. Gonzalez, Richard E. Woods, and Steven L. Eddins.
