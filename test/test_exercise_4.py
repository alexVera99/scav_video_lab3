import unittest
from src.lib import exercise_4 as ex4
import pathlib


class TestExercise4(unittest.TestCase):
    def setup_class(self):
        self.video_filename = pathlib.Path("../data/bbb.mp4")
        self.video_filename_2 = pathlib.Path("../data/bbb_2_audio_codecs.mp4")
        self.video_filename_fake = pathlib.Path("/fake/path")

    def test_analyze_broadcasting_standard(self):
        expected_result = sorted(["DVB-T",
                           "ISDB-T",
                           "DTMB"])
        analyzer = ex4.BroadcastingAnalyzer()
        broadcasting_standards = analyzer.analyze(self.video_filename)
        broadcasting_standards = sorted(broadcasting_standards)

        self.assertListEqual(expected_result,
                             broadcasting_standards)

    def test_analyze_broadcasting_standard_2(self):
        expected_result = sorted(["DVB-T",
                           "ISDB-T",
                           "DTMB"])
        analyzer = ex4.BroadcastingAnalyzer()
        broadcasting_standards = analyzer.analyze(self.video_filename_2)
        broadcasting_standards = sorted(broadcasting_standards)

        self.assertListEqual(expected_result,
                             broadcasting_standards)