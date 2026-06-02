# IEEE-Inauguration-System

IEEE Inauguration System is a Python computer-vision launch portal for the IEEE Women in Engineering (WIE) **"Aadhya"** inauguration event.

## Features
- Full-screen Tkinter launch UI with event branding.
- Live webcam processing with OpenCV.
- Real-time Two Thumbs Up recognition using MediaPipe Hands (TensorFlow Lite powered).
- Automatic inauguration video launch via Python subprocess when gesture is detected.
- Modular code for GUI, gesture logic, video launch, and asset path management.

## Project Structure
- `ieee_inauguration/app.py` – GUI + webcam detection loop.
- `ieee_inauguration/gesture.py` – gesture recognition logic.
- `ieee_inauguration/video_launcher.py` – OS-specific video launch command.
- `ieee_inauguration/assets.py` – event asset path helpers.
- `assets/` – place event assets (video/logo) here.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run
1. Add your video file at: `assets/inauguration_video.mp4`
2. (Optional) Add event logo at: `assets/event_logo.png`
3. Start the app:

```bash
python -m ieee_inauguration
```

## Usage
- Launches in full-screen mode.
- Click **Start Gesture Detection**.
- Show **Two Thumbs Up** simultaneously to the webcam.
- The inauguration video opens automatically in the system default video player.
- Press `Esc` to exit the app.

## Testing
```bash
python -m unittest discover -s tests -q
```
