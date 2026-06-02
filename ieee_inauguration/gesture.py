"""Gesture recognition logic for Two Thumbs Up detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None  # type: ignore[assignment]

try:
    import mediapipe as mp
except ImportError:  # pragma: no cover
    mp = None  # type: ignore[assignment]


THUMB_TIP = 4
THUMB_IP = 3
THUMB_MCP = 2
INDEX_TIP, INDEX_PIP = 8, 6
MIDDLE_TIP, MIDDLE_PIP = 12, 10
RING_TIP, RING_PIP = 16, 14
PINKY_TIP, PINKY_PIP = 20, 18


@dataclass
class GestureResult:
    detected: bool
    frame: Optional[Any] = None


def _is_thumb_up(landmarks: Iterable[Any]) -> bool:
    lm = list(landmarks)
    thumb_extended = lm[THUMB_TIP].y < lm[THUMB_IP].y < lm[THUMB_MCP].y
    other_fingers_folded = all(
        lm[tip].y > lm[pip].y
        for tip, pip in ((INDEX_TIP, INDEX_PIP), (MIDDLE_TIP, MIDDLE_PIP), (RING_TIP, RING_PIP), (PINKY_TIP, PINKY_PIP))
    )
    return thumb_extended and other_fingers_folded


def has_two_thumbs_up(hand_landmark_sets: Iterable[Iterable[Any]]) -> bool:
    """Return True when at least two detected hands are showing thumbs up."""

    thumbs_up_count = sum(1 for landmarks in hand_landmark_sets if _is_thumb_up(landmarks))
    return thumbs_up_count >= 2


class GestureDetector:
    """Processes webcam frames and detects the two-thumbs-up gesture."""

    def __init__(self) -> None:
        self._mp_hands = None
        self._hands = None
        self._mp_draw = None

        if mp is not None:
            self._mp_hands = mp.solutions.hands
            self._mp_draw = mp.solutions.drawing_utils
            self._hands = self._mp_hands.Hands(
                max_num_hands=2,
                min_detection_confidence=0.6,
                min_tracking_confidence=0.6,
            )

    def close(self) -> None:
        if self._hands is not None:
            self._hands.close()

    def process_frame(self, frame: Any) -> GestureResult:
        if cv2 is None or self._hands is None:
            return GestureResult(detected=False, frame=frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb)
        hand_landmarks = []

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                hand_landmarks.append(hand.landmark)
                if self._mp_draw is not None:
                    self._mp_draw.draw_landmarks(frame, hand, self._mp_hands.HAND_CONNECTIONS)

        return GestureResult(detected=has_two_thumbs_up(hand_landmarks), frame=frame)
