"""Solution for Exercise 4."""
import pathlib

from src.lib import utils as ut
from src.lib import exercise_1 as ex1


class BroadcastingAnalyzer:
    def __init__(self):
        self.standard_to_audio = {
            "DVB-T": ["AAC", "AC3", "MP3"],
            "ISDB-T": ["AAC"],
            "ATSC": ["AC3"],
            "DTMB": ["DRA", "AAC", "AC3", "MP2", "MP3"]
        }

    def analyze(self, filename_path: pathlib.Path):
        parser = ex1.FfmpegMetadataParser()
        metadata = parser.get_metadata(filename_path)

        accepted_broadcasting_standards = []

        for stream in metadata["streams"]:
            if stream["type"].lower() != "audio":
                continue
            codec = stream["codec"].split(" ")[0].upper()

            for standard, audio_c_accepted in self.standard_to_audio.items():
                if codec not in audio_c_accepted:
                    continue
                if standard in accepted_broadcasting_standards:
                    continue
                accepted_broadcasting_standards.append(standard)

        return accepted_broadcasting_standards


def main():
    video_filename = pathlib.Path("../../data/bbb.mp4")

    analyzer = BroadcastingAnalyzer()
    standards = analyzer.analyze(video_filename)

    print(standards)


if __name__ == "__main__":
    main()
