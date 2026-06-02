"""Tkinter GUI and webcam loop for the IEEE Inauguration System."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None  # type: ignore[assignment]

from .assets import resolve_asset
from .config import DEFAULT_CONFIG
from .gesture import GestureDetector
from .video_launcher import VideoLauncher


class InaugurationApp(tk.Tk):
    """Full-screen launch portal that detects gesture and launches video."""

    def __init__(self) -> None:
        super().__init__()
        self.config_data = DEFAULT_CONFIG
        self.title(self.config_data.title)
        self.attributes("-fullscreen", True)
        self.configure(bg="#0f172a")

        self.detector = GestureDetector()
        self.video_launcher = VideoLauncher()
        self.capture = None
        self.detected_frames = 0
        self._video_launched = False

        self.bind("<Escape>", lambda _event: self.close())
        self._build_ui()

    def _build_ui(self) -> None:
        tk.Label(
            self,
            text="IEEE WIE",
            font=("Helvetica", 56, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
        ).pack(pady=(90, 10))

        tk.Label(
            self,
            text=self.config_data.event_name,
            font=("Helvetica", 28),
            fg="#cbd5e1",
            bg="#0f172a",
        ).pack(pady=12)

        self.status_label = tk.Label(
            self,
            text="Show two thumbs up together to start inauguration video",
            font=("Helvetica", 18),
            fg="#38bdf8",
            bg="#0f172a",
        )
        self.status_label.pack(pady=24)

        tk.Button(
            self,
            text="Start Gesture Detection",
            font=("Helvetica", 18, "bold"),
            bg="#2563eb",
            fg="white",
            padx=30,
            pady=12,
            command=self.start_detection,
        ).pack(pady=30)

    def start_detection(self) -> None:
        if cv2 is None:
            messagebox.showerror("OpenCV Missing", "OpenCV is required to read webcam feed.")
            return

        if self.capture is None:
            self.capture = cv2.VideoCapture(self.config_data.camera_index)

        if not self.capture.isOpened():
            messagebox.showerror("Camera Error", "Unable to open webcam.")
            return

        self.status_label.config(text="Detection started. Hold Two Thumbs Up...")
        self._update_detection_loop()

    def _update_detection_loop(self) -> None:
        if self._video_launched or self.capture is None:
            return

        ok, frame = self.capture.read()
        if not ok:
            self.status_label.config(text="Camera frame unavailable. Retrying...")
            self.after(100, self._update_detection_loop)
            return

        result = self.detector.process_frame(frame)
        if cv2 is not None and result.frame is not None:
            cv2.imshow("IEEE Inauguration Gesture Detection", result.frame)
            cv2.waitKey(1)

        if result.detected:
            self.detected_frames += 1
        else:
            self.detected_frames = 0

        if self.detected_frames >= self.config_data.required_consecutive_detections:
            self._launch_inauguration_video()
            return

        self.after(40, self._update_detection_loop)

    def _launch_inauguration_video(self) -> None:
        video_path = resolve_asset(self.config_data.video_file)
        if not Path(video_path).exists():
            messagebox.showerror("Asset Missing", f"Video file not found: {video_path}")
            return

        self.video_launcher.launch(video_path)
        self._video_launched = True
        self.status_label.config(text="Inauguration video launched successfully!")
        self._cleanup_capture()

    def _cleanup_capture(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        if cv2 is not None:
            cv2.destroyAllWindows()

    def close(self) -> None:
        self._cleanup_capture()
        self.detector.close()
        self.destroy()


def run_app() -> None:
    app = InaugurationApp()
    app.mainloop()
