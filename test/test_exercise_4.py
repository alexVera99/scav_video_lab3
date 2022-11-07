"""Test for Exercise 4."""
import unittest
import pathlib

from src import exercise_4 as ex4


class TestExercise4(unittest.TestCase):
    """
    Test exercise_4.py
    """
    def setup_class(self):
        """
        Initialize common data for all tests.
        :return: no return
        """
        self.video_filename = pathlib.Path("../data/bbb.mp4")
        self.video_filename_2 = pathlib.Path("data/bbb_2_audio_codecs.mp4")
        self.video_filename_3 = pathlib.Path("data/bbb_audio_ac3.mp4")
        self.video_filename_fake = pathlib.Path("/fake/path")

    def test_analyze_broadcasting_standard(self):
        """
        Test analyze() function positively.
        :return: no return
        """
        expected_result = sorted(["DVB-T",
                           "ISDB-T",
                           "DTMB"])
        analyzer = ex4.BroadcastingAnalyzer()
        broadcasting_standards = analyzer.analyze(self.video_filename)
        broadcasting_standards = sorted(broadcasting_standards)

        self.assertListEqual(expected_result,
                             broadcasting_standards)

    def test_analyze_broadcasting_standard_2(self):
        """
        Test analyze() function positively.
        :return: no return
        """
        expected_result = sorted(["DVB-T",
                           "ISDB-T",
                           "DTMB"])
        analyzer = ex4.BroadcastingAnalyzer()
        broadcasting_standards = analyzer.analyze(self.video_filename_2)
        broadcasting_standards = sorted(broadcasting_standards)

        self.assertListEqual(expected_result,
                             broadcasting_standards)

    def test_analyze_broadcasting_standard_3(self):
        """
        Test analyze() function positively.
        :return: no return
        """
        expected_result = sorted(["DVB-T",
                                  "ATSC",
                                  "DTMB"])

        analyzer = ex4.BroadcastingAnalyzer()
        broadcasting_standards = analyzer.analyze(self.video_filename_3)
        broadcasting_standards = sorted(broadcasting_standards)

        self.assertListEqual(expected_result,
                             broadcasting_standards)

    def test_analyze_no_such_file_or_directory(self):
        """
        Test analyze() function when the given file \
        does not exist.
        :return: no return
        """
        analyzer = ex4.BroadcastingAnalyzer()
        with self.assertRaises(Exception):
            analyzer.analyze(self.video_filename_fake)
