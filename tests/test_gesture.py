import unittest

from ieee_inauguration.gesture import has_two_thumbs_up


class Landmark:
    def __init__(self, y: float) -> None:
        self.y = y


def make_thumb_up() -> list[Landmark]:
    lm = [Landmark(0.5) for _ in range(21)]
    lm[2].y = 0.5
    lm[3].y = 0.4
    lm[4].y = 0.3
    lm[6].y = 0.3
    lm[8].y = 0.6
    lm[10].y = 0.3
    lm[12].y = 0.6
    lm[14].y = 0.3
    lm[16].y = 0.6
    lm[18].y = 0.3
    lm[20].y = 0.6
    return lm


def make_open_hand() -> list[Landmark]:
    lm = [Landmark(0.5) for _ in range(21)]
    lm[2].y = 0.5
    lm[3].y = 0.4
    lm[4].y = 0.3
    lm[6].y = 0.6
    lm[8].y = 0.2
    return lm


class GestureTests(unittest.TestCase):
    def test_detects_two_thumbs_up(self) -> None:
        self.assertTrue(has_two_thumbs_up([make_thumb_up(), make_thumb_up()]))

    def test_rejects_when_only_one_thumb_up(self) -> None:
        self.assertFalse(has_two_thumbs_up([make_thumb_up(), make_open_hand()]))


if __name__ == "__main__":
    unittest.main()
