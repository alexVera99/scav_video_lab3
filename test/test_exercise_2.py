"""Test for Exercise 2."""
import unittest
import pathlib

from src import exercise_2 as ex2, exercise_1 as ex1

class TestExercise2(unittest.TestCase):
    """
    Test exercise_2.py
    """
    def setup_class(self):
        """
        Initialize common data for all tests.
        :return: no return
        """
        self.video_filename = pathlib.Path("../data/bbb.mp4")
        self.video_filename_fake = pathlib.Path("/fake/path")

    def test_run_pipeline(self):
        """
        Test run_pipeline() function positively.
        :return: no return
        """
        expected_metadata = {
                            "duration": "00:01:00.00",
                            "bitrate": "674 kb/s",
                            "num_streams": 3,
                            "streams": [
                                {
                                    "name": "Stream #0:0[0x1](und)",
                                    "type": "Video",
                                    "codec": "h264 (High) (avc1 / 0x31637661)"
                                },
                                {
                                    "name": "Stream #0:1[0x2](und)",
                                    "type": "Audio",
                                    "codec": "mp3 (mp4a / 0x6134706D)"
                                },
                                {
                                    "name": "Stream #0:2[0x3](und)",
                                    "type": "Audio",
                                    "codec": "aac (LC) (mp4a / 0x6134706D)"
                                }
                            ]
                        }

        mp4_container = ex2.run_pipeline(self.video_filename, 0, 60)

        parser = ex1.FfmpegMetadataParser()

        mp4_container_metadata = parser.get_metadata(mp4_container)

        self.assertDictEqual(mp4_container_metadata,
                             expected_metadata)

    def test_run_pipeline_no_such_a_file(self):
        """
        Test run_pipeline() function when the given file \
        does not exist.
        :return: no return
        """
        with self.assertRaises(Exception):
            ex2.run_pipeline(self.video_filename_fake, 0, 60)
