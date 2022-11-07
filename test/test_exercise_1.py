"""Test for Exercise 1."""
import pathlib
import unittest
from src import exercise_1 as ex1


class TestExercise1(unittest.TestCase):
    """
    Test exercise_1.py
    """
    def setup_class(self):
        """
        Initialize common data for all tests.
        :return: no return
        """
        self.video_filename = pathlib.Path("../data/bbb.mp4")
        self.video_filename_fake = pathlib.Path("/fake/path")

    def test_get_metadata(self):
        """
        Test get_metadata() function positively.
        :return: no return
        """
        expected_data = {
            "duration": "00:09:56.48",
            "bitrate": "829 kb/s",
            "num_streams": 2,
            "streams": [
                {
                    "name": "Stream #0:0[0x1](und)",
                    "type": "Video",
                    "codec": "h264 (Constrained Baseline) (avc1 / 0x31637661)",
                },
                {
                    "name": "Stream #0:1[0x2](und)",
                    "type": "Audio",
                    "codec": "aac (LC) (mp4a / 0x6134706D)"
                }
            ]
        }

        parser = ex1.FfmpegMetadataParser()

        metadata = parser.get_metadata(self.video_filename)

        self.assertDictEqual(metadata, expected_data)

    def test_get_metadata_no_such_a_file(self):
        """
        Test get_metadata() function when the given file \
        does not exist.
        :return: no return
        """
        parser = ex1.FfmpegMetadataParser()

        with self.assertRaises(Exception):
            parser.get_metadata(self.video_filename_fake)
