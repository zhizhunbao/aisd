"""
CST8508 Machine Vision – Final Project
Webcam Person Detection, Tracking, and Centering

This script streams from a laptop webcam, detects people using
RTMDet-s (mmdetection), tracks them with ByteTrack, and shows
which direction the camera needs to move to center the person.

Course: CST8508 – Machine Vision
Date  : March 2026
"""

# --- Overview ---
# Streams webcam video, runs person detection (RTMDet-s), tracks with
# ByteTrack, picks the biggest bounding box, and tells the user which
# way the camera should move to center that person.

# --- Dependencies ---
# opencv-python, numpy, torch, mmengine, mmcv, mmdet, supervision
# See README or report for full install steps.

import cv2
import json
import numpy as np
import os
import sys
import time

# Try importing mmdet – needed for RTMDet-s
try:
    from mmdet.apis import DetInferencer
    MMDET_AVAILABLE = True
except ImportError:
    MMDET_AVAILABLE = False
    print("[WARNING] mmdet not installed. Install with:")
    print("  pip install -U openmim")
    print("  mim install mmengine \"mmcv>=2.0.0\" mmdet")

# Try importing supervision – needed for ByteTrack tracker
try:
    import supervision as sv
    SUPERVISION_AVAILABLE = True
except ImportError:
    SUPERVISION_AVAILABLE = False
    print("[WARNING] supervision not installed. Install with:")
    print("  pip install supervision")


# =============================================
# Configuration
# =============================================
# Settings live in config.json so we can tweak
# thresholds, resolution, etc. without touching code.

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "config.json")

DEFAULT_CONFIG = {
    "model_name": "rtmdet_s_8xb32-300e_coco",
    "device": "cpu",
    "person_class_id": 0,
    "confidence_threshold": 0.5,
    "camera_id": 0,
    "frame_width": 640,
    "frame_height": 480,
    "center_tolerance_ratio": 0.05,
    "crop_padding_ratio": 0.8,
    "crop_display_size": [480, 480],
    "bytetrack": {
        "track_activation_threshold": 0.25,
        "lost_track_buffer": 30,
        "minimum_matching_threshold": 0.8,
        "frame_rate": 30
    }
}


def load_config(path=CONFIG_PATH):
    """Read config.json; use defaults if the file is missing."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"Config loaded from {path}")
        return config
    print(f"Config file not found at {path}, using defaults.")
    return DEFAULT_CONFIG.copy()


# =============================================
# Detector Setup – RTMDet-s
# =============================================
# We use the pre-trained RTMDet-s from mmdetection.
# DetInferencer downloads the config + weights automatically
# and handles all the pre/post-processing for us.

def init_detector(config):
    """Load RTMDet-s via DetInferencer. Returns the inferencer object."""
    if not MMDET_AVAILABLE:
        raise RuntimeError("mmdet is not installed.")

    model_name = config["model_name"]
    device = config["device"]
    print(f"[INFO] Loading {model_name} on device '{device}' ...")
    inferencer = DetInferencer(
        model=model_name,
        device=device,
        show_progress=False
    )
    print(f"[INFO] {model_name} loaded successfully.")
    return inferencer


# =============================================
# Tracker Setup – ByteTrack
# =============================================
# ByteTrack keeps track of people across frames
# by matching detections using IoU. Each person
# gets a stable ID that persists over time.

def init_tracker(config):
    """Create a ByteTrack tracker using params from config."""
    if not SUPERVISION_AVAILABLE:
        raise RuntimeError("supervision is not installed.")

    bt_cfg = config["bytetrack"]
    tracker = sv.ByteTrack(
        track_activation_threshold=bt_cfg["track_activation_threshold"],
        lost_track_buffer=bt_cfg["lost_track_buffer"],
        minimum_matching_threshold=bt_cfg["minimum_matching_threshold"],
        frame_rate=bt_cfg["frame_rate"]
    )
    print("[INFO] ByteTrack tracker initialized.")
    return tracker


# =============================================
# Detection – run RTMDet-s on a frame
# =============================================
# We only care about person detections (label 0)
# so everything else gets filtered out.

def detect_persons(inferencer, frame, config):
    """Run detection on one frame; return only person bboxes, scores, labels."""
    result = inferencer(
        frame,
        show=False,
        no_save_vis=True,
        no_save_pred=True,
        print_result=False
    )

    pred = result['predictions'][0]
    bboxes = np.array(pred['bboxes']) if pred['bboxes'] else np.empty((0, 4))
    scores = np.array(pred['scores']) if pred['scores'] else np.empty(0)
    labels = np.array(pred['labels']) if pred['labels'] else np.empty(0, dtype=int)

    if len(labels) == 0:
        return np.empty((0, 4)), np.empty(0), np.empty(0, dtype=int)

    # Filter: person class only (label 0) and above confidence threshold
    person_id = config["person_class_id"]
    threshold = config["confidence_threshold"]
    mask = (labels == person_id) & (scores >= threshold)

    return bboxes[mask], scores[mask], labels[mask].astype(int)


# =============================================
# Tracking – assign IDs across frames
# =============================================

def track_persons(tracker, bboxes, scores, labels):
    """Feed detections into ByteTrack; returns Detections with tracker IDs."""
    if len(bboxes) == 0:
        detections = sv.Detections.empty()
        detections = tracker.update_with_detections(detections)
        return detections

    detections = sv.Detections(
        xyxy=bboxes.astype(np.float32),
        confidence=scores.astype(np.float32),
        class_id=labels.astype(int)
    )
    tracked = tracker.update_with_detections(detections)
    return tracked


# =============================================
# Pick the biggest person (by bbox area)
# =============================================
# If there are multiple people, we only track
# the one with the largest bounding box.

def select_largest_person(detections):
    """Return the bbox and ID of the person with the biggest area."""
    if len(detections) == 0:
        return None, None

    widths = detections.xyxy[:, 2] - detections.xyxy[:, 0]
    heights = detections.xyxy[:, 3] - detections.xyxy[:, 1]
    areas = widths * heights
    idx = np.argmax(areas)

    bbox = detections.xyxy[idx]
    tracker_id = (detections.tracker_id[idx]
                  if detections.tracker_id is not None else -1)

    return bbox, tracker_id


# =============================================
# Centering Logic
# =============================================
# Compare the person's bbox center to the frame center.
# If the person is off-center, tell the user which way
# the camera should move and by how many pixels.

def calculate_centering(bbox, frame_width, frame_height, tolerance_ratio):
    """Figure out which direction the camera needs to move and by how much."""
    # Image center
    img_cx = frame_width / 2
    img_cy = frame_height / 2

    # Person bbox center
    x1, y1, x2, y2 = bbox
    box_w = x2 - x1
    box_h = y2 - y1
    person_cx = x1 + box_w / 2
    person_cy = y1 + box_h / 2

    # How far off-center the person is
    dx = person_cx - img_cx   # positive => person is right of center
    dy = person_cy - img_cy   # positive => person is below center

    # Small dead zone so we don't spam messages when nearly centered
    tol_x = frame_width * tolerance_ratio
    tol_y = frame_height * tolerance_ratio

    directions = []

    # Check horizontal offset
    if person_cx < img_cx - tol_x:
        directions.append(
            f"Camera must move to the left ({abs(dx):.0f}px)")
    elif person_cx > img_cx + tol_x:
        directions.append(
            f"Camera must move to the right ({abs(dx):.0f}px)")

    # Check vertical offset
    if person_cy < img_cy - tol_y:
        directions.append(
            f"Camera must move up ({abs(dy):.0f}px)")
    elif person_cy > img_cy + tol_y:
        directions.append(
            f"Camera must move down ({abs(dy):.0f}px)")

    is_centered = len(directions) == 0

    return directions, dx, dy, is_centered


# =============================================
# Crop view – zoom into the target person
# =============================================

def crop_centered_view(frame, bbox, config):
    """Crop around the target person with some padding, then resize."""
    h_frame, w_frame = frame.shape[:2]
    x1, y1, x2, y2 = bbox
    box_w = x2 - x1
    box_h = y2 - y1

    pad_ratio = config["crop_padding_ratio"]
    pad_w = int(box_w * pad_ratio)
    pad_h = int(box_h * pad_ratio)

    crop_x1 = max(0, int(x1 - pad_w))
    crop_y1 = max(0, int(y1 - pad_h))
    crop_x2 = min(w_frame, int(x2 + pad_w))
    crop_y2 = min(h_frame, int(y2 + pad_h))

    crop = frame[crop_y1:crop_y2, crop_x1:crop_x2]

    if crop.size == 0:
        size = tuple(config["crop_display_size"])
        return np.zeros((*size, 3), dtype=np.uint8)

    display_size = tuple(config["crop_display_size"])
    return cv2.resize(crop, display_size)


# =============================================
# Main video loop
# =============================================
# Reads frames from webcam, runs detection + tracking,
# draws everything on screen. Press 'q' to quit.

def video_stream():
    """Main loop: webcam → detect → track → center → display."""
    # Load settings from config.json
    config = load_config()

    # Set up the detector and tracker
    inferencer = init_detector(config)
    tracker = init_tracker(config)

    # Open webcam (using DirectShow on Windows)
    cam_id = config["camera_id"]
    cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"[ERROR] Could not open webcam (camera_id={cam_id}).")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["frame_width"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["frame_height"])

    print("[INFO] Starting webcam stream... Press 'q' to quit.")
    print("=" * 60)

    frame_count = 0
    fps_start = time.time()
    fps_display = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Could not read frame from webcam.")
            break

        h_frame, w_frame = frame.shape[:2]
        frame_count += 1

        # Save a clean copy before we draw on the frame
        clean_frame = frame.copy()

        # Detect people
        bboxes, scores, labels = detect_persons(inferencer, frame, config)

        # Track them across frames
        tracked = track_persons(tracker, bboxes, scores, labels)

        # Draw bounding boxes and IDs for all detected people
        for i in range(len(tracked)):
            bx1, by1, bx2, by2 = tracked.xyxy[i].astype(int)
            tid = (tracked.tracker_id[i]
                   if tracked.tracker_id is not None else -1)
            conf = (tracked.confidence[i]
                    if tracked.confidence is not None else 0.0)

            # Green box for each person
            cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
            label_text = f"Person ID:{tid} ({conf:.2f})"
            cv2.putText(frame, label_text, (bx1, by1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Pick the biggest person
        target_bbox, target_id = select_largest_person(tracked)

        if target_bbox is not None:
            # Red box on the target person
            tx1, ty1, tx2, ty2 = target_bbox.astype(int)
            cv2.rectangle(frame, (tx1, ty1), (tx2, ty2), (0, 0, 255), 3)
            cv2.putText(frame, f"TARGET ID:{target_id}",
                        (tx1, ty1 - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Calculate centering offset
            tol = config["center_tolerance_ratio"]
            directions, dx, dy, is_centered = calculate_centering(
                target_bbox, w_frame, h_frame, tol
            )

            # Crosshair at frame center
            center_x, center_y = w_frame // 2, h_frame // 2
            cv2.drawMarker(frame, (center_x, center_y), (0, 255, 255),
                           cv2.MARKER_CROSS, 30, 2)

            # Dot at person center
            person_cx = int((target_bbox[0] + target_bbox[2]) / 2)
            person_cy = int((target_bbox[1] + target_bbox[3]) / 2)
            cv2.circle(frame, (person_cx, person_cy), 6, (255, 0, 255), -1)

            # Line from frame center to person center
            cv2.line(frame, (center_x, center_y),
                     (person_cx, person_cy), (255, 255, 0), 1, cv2.LINE_AA)

            # Show direction messages
            if is_centered:
                cv2.putText(frame, "CENTERED - Good!",
                            (10, h_frame - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                y_pos = h_frame - 20 - (len(directions) - 1) * 30
                for i, msg in enumerate(directions):
                    # Green for left/right, Red for up/down (per spec)
                    if "left" in msg or "right" in msg:
                        color = (0, 255, 0)    # green
                    else:
                        color = (0, 0, 255)    # red
                    cv2.putText(frame, msg,
                                (10, y_pos + i * 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                                color, 2)

            # Show offset numbers
            cv2.putText(frame, f"Offset: dx={dx:+.0f}px  dy={dy:+.0f}px",
                        (w_frame - 320, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

            # Cropped view centered on target
            cropped = crop_centered_view(clean_frame, target_bbox, config)

            # Add text overlay on the cropped view
            ch, cw = cropped.shape[:2]
            cv2.putText(cropped, f"Target ID:{target_id}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(cropped, f"Offset: dx={dx:+.0f}px  dy={dy:+.0f}px",
                        (cw - 300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
            if is_centered:
                cv2.putText(cropped, "CENTERED", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                for i, msg in enumerate(directions):
                    if "left" in msg or "right" in msg:
                        color = (0, 255, 0)    # green
                    else:
                        color = (0, 0, 255)    # red
                    cv2.putText(cropped, msg, (10, 60 + i * 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                color, 2)
            cv2.imshow("Person Focus (Cropped) - Press 'q' to quit", cropped)

        else:
            # Nobody found – show a message
            cv2.putText(frame, "No person detected",
                        (w_frame // 2 - 150, h_frame - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Blank cropped window
            disp_size = tuple(config["crop_display_size"])
            blank = np.zeros((*disp_size, 3), dtype=np.uint8)
            cv2.putText(blank, "No person detected", (100, 220),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(blank, "Searching...", (160, 260),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("Person Focus (Cropped) - Press 'q' to quit", blank)

        # HUD overlay
        elapsed = time.time() - fps_start
        if elapsed > 0:
            fps_display = frame_count / elapsed
        cv2.putText(frame,
                    f"Persons: {len(tracked)}  FPS: {fps_display:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Model: RTMDet-s | Tracker: ByteTrack",
                    (10, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Display the full frame window
        cv2.imshow("Full View - Person Detection & Tracking", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Video stream stopped.")


# =============================================
# Entry point
# =============================================
if __name__ == "__main__":
    print("=" * 60)
    print("CST8508 Machine Vision – Final Project")
    print("Webcam Person Detection, Tracking & Centering")
    print("Model  : RTMDet-s (mmdetection, COCO pre-trained)")
    print("Tracker: ByteTrack (supervision)")
    print("Target : Person class only (COCO label 0)")
    print("=" * 60)
    print()

    # Make sure all dependencies are available
    if not MMDET_AVAILABLE:
        print("[ERROR] mmdet is required. Install with:")
        print("  pip install -U openmim")
        print("  mim install mmengine \"mmcv>=2.0.0\" mmdet")
        sys.exit(1)
    if not SUPERVISION_AVAILABLE:
        print("[ERROR] supervision is required. Install with:")
        print("  pip install supervision")
        sys.exit(1)

    video_stream()


# =============================================
# Results
# =============================================
# - RTMDet-s detects people well on CPU (~1.5-3 FPS).
# - ByteTrack gives stable IDs across frames.
# - Largest bbox selection works when multiple people are visible.
# - Direction messages and pixel offsets update in real time.
# - The cropped view follows the target person smoothly.

# =============================================
# Evaluation
# =============================================
# Strengths:
#   - Much better than Haar Cascade (detects full body, not just face).
#   - ByteTrack IDs stay consistent even with brief occlusions.
#   - Config file makes it easy to tweak without editing code.
#
# Limitations:
#   - CPU-only is slow (~1.5-3 FPS). GPU would be much faster.
#   - Misses people in very dark scenes.
#   - "Biggest box" doesn't always mean the most important person.
#
# Challenges:
#   - Getting mmdetection installed on Windows was tricky (version matching).
#   - First few frames from webcam can be dark (camera warm-up).
#   - Had to find the right confidence threshold (0.5 worked best).

# =============================================
# Lessons Learned
# =============================================
# 1. RTMDet-s is a good fit for real-time webcam work – fast enough
#    on CPU and accurate enough for person detection.
# 2. DetInferencer makes it really easy to load and run models
#    without worrying about configs or checkpoints manually.
# 3. ByteTrack + supervision library was simple to plug in.
# 4. Filtering to person-only before tracking saves time.
# 5. The centering logic is straightforward – just compare centers.
#    Adding a small dead zone prevents flickering messages.
# 6. Keeping settings in config.json is way easier than hardcoding.
# 7. Could extend this later to control a real pan-tilt camera,
#    or add person re-identification across multiple cameras.
