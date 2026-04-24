# Week 9 Review — Object Tracking

> 📋 Based on instructor's revision topics:
> **Object tracking vs object detection, Single vs multiple object tracking, Single stage vs multi stage object trackers, Application of multiple object tracking, ByteTrack, Tools for MOT development**

---

## Q1: What is the difference between object tracking and object detection?

| Aspect | Object Detection | Object Tracking |
|---|---|---|
| **Scope** | Single frame | Across frames |
| **Task** | Detect + classify objects | Estimate positions over time |
| **Identity** | No ID assignment | **Assign unique ID** per object |
| **Occlusion** | Fails if occluded | **Handles occlusion** |
| **Input** | Image | Video (sequence of frames) |

**Object tracking 3-step process:**
1. Object detection → detect objects (bounding boxes)
2. Assign unique ID → assign unique identifier
3. Track across frames → track between frames and store information

---

## Q2: Single Object Tracking vs Multiple Object Tracking (SOT vs MOT)

| Aspect | SOT (Single Object Tracking) | MOT (Multiple Object Tracking) |
|---|---|---|
| **Targets** | One object | Multiple objects |
| **Complexity** | Lower | **Higher** |
| **Key difficulty** | Maintaining identity under appearance & scale changes | Distinguishing similar objects + inter-object occlusion |

**Additional MOT complexity:** Dynamic number of targets, nonlinear motion, objects appearing/disappearing, identity assignment in crowded scenes

---

## Q3: Single-Stage vs Two-Stage Trackers

| Aspect | Single-Stage | Two-Stage |
|---|---|---|
| **Process** | Detection + tracking in one network | Detection → Association (separate) |
| **Speed** | **Faster** | Slower |
| **Accuracy** | May sacrifice accuracy | **Higher accuracy** |
| **Representative** | **FairMOT**, **CenterTrack** | **DeepSORT**, **ByteTrack**, **OCSort** |
| **Best for** | Real-time applications | Crowded/complex scenes |

**Two-Stage association algorithms:** Kalman filtering (motion prediction), Hungarian algorithm (assignment), IoU matching, ReID features (appearance)

---

## Q4: What is ByteTrack? How does it work?

**ByteTrack** — an innovative two-stage MOT method whose key innovation is **associating every detection box** (including low-confidence ones).

### ByteTrack Workflow:

| Step | Description |
|---|---|
| **1. Object Detection** | Use YOLO/Faster R-CNN to detect objects in each frame |
| **2. Stage 1 Association** | Match high-confidence detections with existing tracklets |
| **3. Stage 2 Association** | Match low-confidence detections based on IoU + appearance features (cosine similarity) → **recover missed targets** |
| **4. Gating Mechanism** | Filter redundant detections |

**Key innovation:** Does not discard low-confidence detections → recovers potentially missed real objects

---

## Q5: What are the applications of MOT?

| Application | Description |
|---|---|
| **Urban traffic** | Vehicle and pedestrian tracking → safety and traffic flow optimization |
| **Retail** | Analyze customer behavior and store traffic |
| **Sports analytics** | Track player movements to provide insights |
| **Surveillance** | Security monitoring and threat detection |

---

## Q6: What are the tools for MOT development?

| Category | Tools |
|---|---|
| **Frameworks** | TensorFlow, PyTorch |
| **Tracking toolkits** | DeepSORT, FairMOT |
| **Annotation** | CVAT, LabelBox |
| **Evaluation** | MOTChallenge, VOT |
| **Deployment** | NVIDIA DeepStream, OpenCV |

**MOT evaluation metrics:** MOTA (Multiple Object Tracking Accuracy), MOTP (Multiple Object Tracking Precision), IoU

---

## Q7: What are the challenges in object tracking?

| Challenge | Description |
|---|---|
| **Rapid movement** | Objects moving at high speed are difficult to match |
| **Size/shape changes** | Object size and shape change across frames |
| **Occlusions** | Need to maintain identity after objects are occluded |
| **Varying lighting** | Changing lighting conditions affect appearance features |
| **Real-time processing** | Inference must be completed within limited time |
| **Similar appearances** | Distinguishing different objects with similar appearances |
