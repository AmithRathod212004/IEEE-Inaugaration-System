import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from ieee_inauguration.video_launcher import VideoLauncher


class VideoLauncherTests(unittest.TestCase):
    def test_build_launch_command_linux(self) -> None:
        launcher = VideoLauncher()
        with patch.object(sys, "platform", "linux"):
            self.assertEqual(launcher.build_launch_command(Path("video.mp4")), ["xdg-open", "video.mp4"])

    def test_build_launch_command_windows(self) -> None:
        launcher = VideoLauncher()
        with patch.object(sys, "platform", "win32"):
            self.assertEqual(
                launcher.build_launch_command(Path("video.mp4")),
                ["cmd", "/c", "start", "", "video.mp4"],
            )

    def test_build_launch_command_macos(self) -> None:
        launcher = VideoLauncher()
        with patch.object(sys, "platform", "darwin"):
            self.assertEqual(launcher.build_launch_command(Path("video.mp4")), ["open", "video.mp4"])

    def test_launch_invokes_subprocess(self) -> None:
        launcher = VideoLauncher()
        with patch.object(VideoLauncher, "build_launch_command", return_value=["xdg-open", "video.mp4"]), patch(
            "subprocess.Popen"
        ) as popen:
            process = object()
            popen.return_value = process
            returned_process = launcher.launch(Path("video.mp4"))
            popen.assert_called_once_with(["xdg-open", "video.mp4"], shell=False)
            self.assertIs(returned_process, process)

    def test_launch_raises_runtime_error_when_process_fails(self) -> None:
        launcher = VideoLauncher()
        with patch.object(VideoLauncher, "build_launch_command", return_value=["xdg-open", "video.mp4"]), patch(
            "subprocess.Popen", side_effect=OSError("missing")
        ):
            with self.assertRaises(RuntimeError):
                launcher.launch(Path("video.mp4"))


if __name__ == "__main__":
    unittest.main()
