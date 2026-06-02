import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time
import subprocess
import os
import urllib.request

# ==========================================================
#          IEEE WOMEN'S SOCIETY - THUMBS UP LAUNCH
# ==========================================================

VIDEO_PATH = r"E:\handshake\WhatsApp Video 2026-02-23 at 7.42.37 PM.mp4"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

CONFIRMATION_FRAMES = 10   # ~0.3 sec at 30 FPS
MIN_DET_CONF = 0.4
MIN_PRESENCE_CONF = 0.4
MIN_TRACK_CONF = 0.4
HIDDEN_TRIGGER_KEY = ord('h')
play_video = False

# ==========================================================
#              TWO THUMBS UP DETECTION FUNCTION
# ==========================================================

THUMB_TIP = 4
THUMB_MCP = 2
INDEX_TIP = 8
INDEX_PIP = 6
MIDDLE_TIP = 12
MIDDLE_PIP = 10
RING_TIP = 16
RING_PIP = 14
PINKY_TIP = 20
PINKY_PIP = 18


def ensure_model_file():
    if os.path.exists(MODEL_PATH):
        return
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def detect_two_thumbs_up(hand_landmarks_list):
    """
    Detect two thumbs-up gesture (2 hands required)
    Returns: True / False
    """
    if len(hand_landmarks_list) != 2:
        return False

    thumbs_up_count = 0

    for hand_landmarks in hand_landmarks_list:
        # Get landmarks
        landmarks = hand_landmarks
        
        # Thumb tip and base
        thumb_tip = landmarks[THUMB_TIP]
        thumb_mcp = landmarks[THUMB_MCP]
        
        # Other finger tips and PIPs
        index_tip = landmarks[INDEX_TIP]
        index_pip = landmarks[INDEX_PIP]
        
        middle_tip = landmarks[MIDDLE_TIP]
        middle_pip = landmarks[MIDDLE_PIP]
        
        ring_tip = landmarks[RING_TIP]
        ring_pip = landmarks[RING_PIP]
        
        pinky_tip = landmarks[PINKY_TIP]
        pinky_pip = landmarks[PINKY_PIP]

        # Thumb pointing up
        thumb_up = thumb_tip.y < thumb_mcp.y
        
        # Other fingers folded (tips below PIPs)
        index_folded = index_tip.y > index_pip.y
        middle_folded = middle_tip.y > middle_pip.y
        ring_folded = ring_tip.y > ring_pip.y
        pinky_folded = pinky_tip.y > pinky_pip.y
        
        fingers_folded = index_folded and middle_folded and ring_folded and pinky_folded
        
        if thumb_up and fingers_folded:
            thumbs_up_count += 1

    return thumbs_up_count == 2


# ==========================================================
#                     INITIAL SETUP
# ==========================================================

print("="*70)
print("👍 IEEE WOMEN'S SOCIETY - INAUGURATION LAUNCH SYSTEM")
print("="*70)
print("\n🎯 Starting camera for hand detection...")
print("   Show TWO THUMBS UP to launch video")
print("   Hidden trigger: press 'H'")
print("   Press ESC to exit\n")
print("="*70 + "\n")

# ==========================================================
#                     CAMERA & HAND DETECTION
# ==========================================================

# Initialize MediaPipe Hand Landmarker (Tasks API)
try:
    ensure_model_file()
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=2,
        min_hand_detection_confidence=MIN_DET_CONF,
        min_hand_presence_confidence=MIN_PRESENCE_CONF,
        min_tracking_confidence=MIN_TRACK_CONF,
    )
    landmarker = vision.HandLandmarker.create_from_options(options)
    print("✓ Hand detection enabled")
except Exception as e:
    print(f"❌ Hand detection failed to start: {e}")
    print("Exiting...")
    raise SystemExit(1)

# Initialize camera with retries/backends
def open_camera_with_retries():
    indices = [0, 1, 2, 3]
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF]
    for index in indices:
        for backend in backends:
            cap_try = cv2.VideoCapture(index, backend)
            if not cap_try.isOpened():
                cap_try.release()
                continue
            # Warm up and ensure we can read at least one frame
            for _ in range(20):
                ret, _ = cap_try.read()
                if ret:
                    return cap_try
                time.sleep(0.05)
            cap_try.release()
    return None


cap = open_camera_with_retries()
if cap is None:
    print("❌ Camera not found or no frames available. Exiting...")
    raise SystemExit(1)

else:
    print("✓ Camera started successfully")
    print("  Show TWO THUMBS UP to trigger video\n")
    
    # Setup fullscreen window for camera feed
    window_name = "👍 Show Two Thumbs Up"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Get screen resolution
    screen_width = 1920
    screen_height = 1080
    
    gesture_counter = 0
    confirmed_time = None
    manual_trigger = False
    
    # ==========================================================
    #                        MAIN LOOP
    # ==========================================================
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠ Camera feed lost")
            break
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        # Resize to fullscreen
        fullscreen_frame = cv2.resize(frame, (screen_width, screen_height), 
                                     interpolation=cv2.INTER_LINEAR)
        
        gesture_detected = False
        
        # Hand detection
        rgb = cv2.cvtColor(fullscreen_frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        results = landmarker.detect(mp_image)
        
        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                for lm in hand_landmarks:
                    x = int(lm.x * screen_width)
                    y = int(lm.y * screen_height)
                    cv2.circle(fullscreen_frame, (x, y), 4, (0, 255, 0), -1)
            
            # Check for two thumbs up
            if len(results.hand_landmarks) == 2:
                gesture_detected = detect_two_thumbs_up(results.hand_landmarks)
        
        if manual_trigger:
            gesture_detected = True
        
        # Gesture confirmation logic
        if gesture_detected:
            gesture_counter += 1
            title_text = "THUMBS UP DETECTED!" if not manual_trigger else "Launch ACTIVATED!"
            cv2.putText(fullscreen_frame, title_text, 
                       (screen_width//2 - 350, 100),
                       cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)
            
            # Show counter
            progress = min(gesture_counter / CONFIRMATION_FRAMES, 1.0)
            bar_width = int(800 * progress)
            cv2.rectangle(fullscreen_frame, (screen_width//2 - 400, 150), 
                         (screen_width//2 - 400 + bar_width, 200), (0, 255, 0), -1)
            cv2.rectangle(fullscreen_frame, (screen_width//2 - 400, 150), 
                         (screen_width//2 + 400, 200), (255, 255, 255), 3)
        else:
            gesture_counter = max(0, gesture_counter - 1)
            confirmed_time = None
            
            # Show instructions
            cv2.putText(fullscreen_frame, "Show TWO THUMBS UP to launch video", 
                       (screen_width//2 - 450, screen_height - 100),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)
        
        # Check if gesture confirmed
        if gesture_counter >= CONFIRMATION_FRAMES:
            if confirmed_time is None:
                confirmed_time = time.time()
                if manual_trigger:
                    print("\n✓ Launch Activated ")
                else:
                    print("\n✓ Two Thumbs Up Detected!")
                print("🎬 Launching video in 1 second...")
            
            # Show success message
            cv2.putText(fullscreen_frame, "SUCCESS! Playing Video...", 
                       (screen_width//2 - 400, screen_height//2),
                       cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)
            
            # Wait 1 second then launch
            if time.time() - confirmed_time > 1.0:
                play_video = True
                break
        
        cv2.imshow(window_name, fullscreen_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # ESC to exit
        if key == 27:
            print("✗ Exiting...")
            cap.release()
            cv2.destroyAllWindows()
            exit()
        
        if key == HIDDEN_TRIGGER_KEY or key == ord('H'):
            manual_trigger = True
            gesture_counter = CONFIRMATION_FRAMES
        
    
    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()

cv2.destroyAllWindows()

# ==========================================================

if not play_video:
    print("\n" + "="*70)
    print("✗ Video not triggered (no thumbs up detected)")
    print("="*70 + "\n")
    raise SystemExit(0)

print("\n" + "="*70)
print("🎬 PLAYING INAUGURATION VIDEO...")
print("="*70 + "\n")

vlc_paths = [
    r"C:\Program Files\VLC\vlc.exe",
    r"C:\Program Files (x86)\VLC\vlc.exe",
]

vlc_found = False

for path in vlc_paths:
    if os.path.exists(path):
        print(f"Playing with VLC: {VIDEO_PATH}\n")
        subprocess.run([path, "--fullscreen", "--play-and-exit", VIDEO_PATH])
        vlc_found = True
        break

if not vlc_found:
    print(f"Playing with Windows Media Player: {VIDEO_PATH}\n")
    try:
        subprocess.run([r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe", VIDEO_PATH])
    except:
        subprocess.run(["start", VIDEO_PATH], shell=True)

print("\n" + "="*70)
print("✓ Video playback completed!")
print("="*70 + "\n")