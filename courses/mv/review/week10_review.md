# Week 10 Review — Sensors and Sensor Fusion

> 📋 Based on instructor's revision topics:
> **Single sensor vs multi sensor analysis, Sensor fusion, Application of sensor fusion, Types of sensors and trade-offs, CCD vs CMOS**

---

## Q1: CCD vs CMOS Sensor Comparison

| Feature | CCD | CMOS |
|---|---|---|
| **Image quality** | Higher quality, less noise | Improved, now comparable |
| **Light sensitivity** | More sensitive (better low-light) | Less sensitive |
| **Power consumption** | **More power** | **Less power** |
| **Cost** | **More expensive** | **Cheaper** |
| **Shutter type** | **Global shutter** (captures all at once → no motion artifacts) | **Rolling shutter** (line by line → may cause skew/wobble) |

---

## Q2: Five Sensor Types and Their Trade-offs

| Sensor | How it works | Advantages | Disadvantages |
|---|---|---|---|
| **Camera** | Optical sensor captures 2D images | High resolution, color, low cost | Affected by rain, fog, snow, lighting, distance |
| **Depth sensor** | Structured Light / ToF ranging | Provides 3D depth information | Affected by ambient light interference |
| **Thermal** | Detects infrared radiation | **Very robust** to lighting and weather | Low resolution, struggles when foreground/background temperature difference is small |
| **LiDAR** | Emits laser pulses to measure distance | 360° 3D point cloud, high accuracy, long range | **Expensive**, sparse data, affected by weather |
| **Radar** | Uses radio waves | Penetrates fog/rain, works at night, measures velocity | Low accuracy/resolution, cannot achieve 360° |

---

## Q3: Single Sensor vs Multi-Sensor Analysis

| Aspect | Single Sensor | Multi-Sensor (Fusion) |
|---|---|---|
| **Simplicity** | ✅ Simple to implement and maintain | ❌ More complex |
| **Cost** | ✅ Lower cost | ❌ Higher cost |
| **Accuracy** | Accurate for specific variables | **Higher overall accuracy** |
| **Redundancy** | ❌ None | ✅ Overlapping data improves reliability |
| **Complementary** | ❌ Single data source | ✅ Different sensors provide complementary data |
| **Resilience** | ❌ Single point of failure | ✅ More robust, can handle individual sensor failure |

---

## Q4: What is Sensor Fusion?

**Sensor Fusion** = combining data from multiple sensors to improve information **accuracy and reliability**.

**Why?** Data from a single sensor may be limited or flawed; combining multi-source data provides a more comprehensive understanding of the environment.

**Techniques:**

| Method | Description |
|---|---|
| **Averaging** | Simple method |
| **Kalman filters** | Probabilistic estimation method |
| **Neural networks** | Complex deep learning fusion |
| **Weighted averaging** | Weight based on sensor reliability |
| **Probabilistic fusion** | Based on probabilistic models |

---

## Q5: Sensor Fusion Data Processing Pipeline

| Step | Description |
|---|---|
| **1. Preprocessing** | Calibration, noise reduction, normalization |
| **2. Alignment & Synchronization** | Precisely merge data streams in time and space |
| **3. Fusion Algorithms** | Weighted averaging, probabilistic fusion, or model-based methods |
| **4. Unified Output** | A dataset more accurate and comprehensive than any single sensor |

---

## Q6: Applications of Sensor Fusion

| Application | Sensors Used | Purpose |
|---|---|---|
| **Autonomous driving** | Camera + Radar + LiDAR + Ultrasonic | 360° environment perception, safe navigation |
| **Mobile devices** | Accelerometer + Gyroscope + Magnetometer | Position tracking and orientation (AR) |
| **Robotics** | Tactile + Visual + Auditory | Complex environment interaction |
| **Drones** | GPS + Inertial + Camera | Precise navigation and stability |

---

## Q7: What are the challenges of sensor fusion?

| Challenge | Description |
|---|---|
| **Data heterogeneity** | Significant differences in quality, resolution, and update rate across sensors |
| **Timing & Synchronization** | Need to precisely align multiple data streams |
| **Computational resources** | Processing massive multi-source data requires significant compute |
| **Security & Privacy** | More sensors collect more sensitive information |
