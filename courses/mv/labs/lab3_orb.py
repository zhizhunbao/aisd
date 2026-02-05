# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
# ---

# # **CST8508 Machine Vision - Lab 3 - Feature Detection and Matching with ORB and BF/FLANN**
#
# **Objective:**
# To familiarize students with ORB for feature detection and BF Matcher or FLANN-based matcher for feature matching in OpenCV.
#
# **Part 1:** Feature Detection with ORB 
#
# **Exercise 1:** Implement ORB to detect key points in an image.
#
# **Part 2:** Feature Matching with ORB and BF/FLANN Matcher 
#
# **Exercise 2:** Match features between two images using ORB and BF matcher or FLANN-based matcher.
#
# **Part 3:** Comparing ORB Performance Under Different Conditions
#
# **Exercise 3:** Explore how changes in image conditions (like lighting, noise, or blurring) affect ORB feature detection and matching.

import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

# +
# Configuration Constants
# 配置常量
IMAGE_PATH = "sample_image.jpg"
OUTPUT_DIR = "lab3_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)
# -

# ## **Common Functions**

def create_orb_detector(nfeatures=500):
    # Requirement: Implement ORB to detect key points
    # 要求：实现 ORB 检测关键点
    # implementation here
    orb = cv2.ORB_create(nfeatures=nfeatures)
    return orb


def match_features(descriptor1, descriptor2):
    # Requirement: Match descriptors between two sets of features
    # 要求：匹配两组特征之间的描述符
    # implementation here
    # 1. Initialize the matcher - consider using BFMatcher or FLANN Matcher
    # 1. 初始化匹配器 - 考虑使用 BFMatcher 或 FLANN 匹配器
    # Use Brute-Force Matcher with Hamming distance for ORB
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # 2. Match the descriptors from both sets of features
    # 2. 匹配两组特征的描述符
    matches = matcher.match(descriptor1, descriptor2)

    # 3. Sort the matches based on their distance to get better matches first
    # 3. 根据距离对匹配进行排序，以便先获得更好的匹配项
    matches = sorted(matches, key=lambda x: x.distance)

    # 4. Return the sorted list of matches
    # 4. 返回排序后的匹配列表
    return matches


# ## **Exercise 1**

def detect_keypoints(image_path, orb_detector):
    # Requirement: Implement ORB to detect key points in an image.
    # 要求：实现 ORB 检测图像中的关键点。
    # implementation here
    # 1. Load the image from the specified path
    # 1. 从指定路径加载图像
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")

    # 2. Use the ORB detector to detect keypoints in the image
    # 2. 使用 ORB 检测器在其检测图像中的关键点
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = orb_detector.detectAndCompute(gray, None)

    # 3. Draw the keypoints on the image for visualization
    # 3. 将关键点绘制在图像上以便可视化
    image_with_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0), flags=0)

    # 4. Return the keypoints and the image with keypoints drawn
    # 4. 返回关键点以及绘制了关键点的图像
    return keypoints, descriptors, image_with_keypoints


# +
# Test Exercise 1
# Create detector
orb = create_orb_detector(nfeatures=500)

# For Exercise 3 comparison, use higher limit to see actual differences
# 为 Exercise 3 对比使用更高上限，以观察实际差异
orb_comparison = create_orb_detector(nfeatures=5000)

# Run detection
kp, des, img_kp = detect_keypoints(IMAGE_PATH, orb)

# Display result
# 显示结果
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(img_kp, cv2.COLOR_BGR2RGB))
plt.title(f"ORB Keypoints Detected: {len(kp)}")
plt.axis('off')
plt.show() # Requirement: Show image directly in the notebook (要求：直接在笔记本中显示图像)
# -

# ## **Exercise 2**

def match_images(image_path1, image_path2, orb_detector):
    # Requirement: Match features between two images using ORB and BF matcher or FLANN-based matcher.
    # 要求：使用 ORB 和 BF 匹配器或基于 FLANN 的匹配器匹配两张图像之间的特征。
    # 1. Detect keypoints and descriptors in both images using the ORB detector
    # 1. 使用 ORB 检测器检测两张图像中的关键点和描述符
    kp1, des1, _ = detect_keypoints(image_path1, orb_detector)
    kp2, des2, _ = detect_keypoints(image_path2, orb_detector)

    # 2. Use a matcher (like FLANN/BF) to find matches between descriptors of both images
    # 2. 使用匹配器（如 FLANN/BF）寻找两张图像描述符之间的匹配项
    matches = match_features(des1, des2)

    # 3. Draw the matches on a combined image showing both input images
    # 3. 将匹配项绘制在显示两个输入图像的组合图像上
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)
    image_with_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, 
                                        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # 4. Return the image with matches drawn
    # 4. 返回绘制了匹配项的图像
    return image_with_matches


# +
# Test Exercise 2
# Create a transformed version for matching
original_img = cv2.imread(IMAGE_PATH)
(h, w) = original_img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated_img = cv2.warpAffine(original_img, M, (w, h))
ROTATED_IMAGE_PATH = "sample_image_rotated.jpg"
cv2.imwrite(ROTATED_IMAGE_PATH, rotated_img)

# Run matching
img_matching_result = match_images(IMAGE_PATH, ROTATED_IMAGE_PATH, orb)

# Display result
# 显示结果
plt.figure(figsize=(15, 8))
plt.imshow(cv2.cvtColor(img_matching_result, cv2.COLOR_BGR2RGB))
plt.title("ORB Feature Matching (Original vs Rotated)")
plt.axis('off')
plt.show() # Requirement: Show image directly in the notebook (要求：直接在笔记本中显示图像)
# -

# ## **Exercise 3**

def compare_orb_performance(image_path, orb_detector):
    # Requirement: Explore how changes in image conditions affect ORB feature detection and matching.
    # 要求：探索图像状况的变化如何影响 ORB 特征检测和匹配。
    # implementation here
    # Key steps:
    # 1. Apply different conditions to the image (like changing brightness, adding noise, or blurring)
    # 1. 对图像应用不同的状况（如改变亮度、添加噪声或模糊）
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Condition: Blurring
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Condition: Noise
    np.random.seed(42)
    noise = np.random.normal(0, 25, gray.shape).astype(np.uint8)
    noisy = cv2.add(gray, noise)
    
    # Condition: Brightness
    bright = cv2.convertScaleAbs(gray, alpha=1.2, beta=50)

    # 2. Detect features using ORB for each altered image
    # 2. 为每个变换后的图像使用 ORB 检测特征
    kp_ref, des_ref = orb_detector.detectAndCompute(gray, None)
    kp_blur, des_blur = orb_detector.detectAndCompute(blurred, None)
    kp_noise, des_noise = orb_detector.detectAndCompute(noisy, None)
    kp_bright, des_bright = orb_detector.detectAndCompute(bright, None)

    # Draw keypoints on each image for visualization
    # 在每张图上绘制关键点以便可视化
    img_ref_kp = cv2.drawKeypoints(gray, kp_ref, None, color=(0, 255, 0), flags=0)
    img_blur_kp = cv2.drawKeypoints(blurred, kp_blur, None, color=(0, 255, 0), flags=0)
    img_noise_kp = cv2.drawKeypoints(noisy, kp_noise, None, color=(0, 255, 0), flags=0)
    img_bright_kp = cv2.drawKeypoints(bright, kp_bright, None, color=(0, 255, 0), flags=0)

    # 3. Compare the number and quality of features detected under each condition
    # 3. 比较每种状况下检测到的特征数量和质量
    comparison_results = {
        'Original': len(kp_ref),
        'Blurred': len(kp_blur),
        'Noisy': len(kp_noise),
        'Bright': len(kp_bright)
    }

    # 4. (Optional) Match features with a reference image to see how well ORB performs under each condition
    # 4.（可选）与参考图像匹配特征，查看 ORB 在各种状况下的表现
    return comparison_results, [img_ref_kp, img_blur_kp, img_noise_kp, img_bright_kp]


# +
# Test Exercise 3
results, altered_images = compare_orb_performance(IMAGE_PATH, orb_comparison)

# Plot summary
plt.figure(figsize=(10, 5))
plt.bar(results.keys(), results.values(), color=['blue', 'green', 'red', 'orange'])
plt.ylabel('Number of Keypoints')
plt.title('ORB Performance Comparison')
plt.show() # Requirement: Show summary plot (要求：显示总结图表)

# Plot visual conditions
titles = ['Original', 'Blurred', 'Noisy', 'Bright']
plt.figure(figsize=(20, 5))
for i in range(4):
    plt.subplot(1, 4, i+1)
    plt.imshow(cv2.cvtColor(altered_images[i], cv2.COLOR_BGR2RGB))
    plt.title(f"{titles[i]} (KPs: {results[titles[i]]})")
    plt.axis('off')
plt.show() # Requirement: Show visual condition comparison (要求：显示视觉状况对比)
# -
