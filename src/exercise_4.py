"""Solution for Exercise 4."""
import pathlib

from src import exercise_1 as ex1


class BroadcastingAnalyzer:
    """Analyze the audio metadata of a video."""

    def __init__(self):
        """No params."""
        self.standard_to_audio = {
            "DVB-T": ["AAC", "AC3", "MP3"],
            "ISDB-T": ["AAC"],
            "ATSC": ["AC3"],
            "DTMB": ["DRA", "AAC", "AC3", "MP2", "MP3"]
        }

    def analyze(self, filename_path: pathlib.Path):
        """
        Analyze the audio metadata of the given video to and \
        return which standard it can fit in.

        :param filename_path: video filename to be analyzed
        :return: list of the standards the video can fit in.
        """
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
    """
    Test the above functions.

    :return no return
    """
    video_filename = pathlib.Path("../data/bbb.mp4")

    analyzer = BroadcastingAnalyzer()
    standards = analyzer.analyze(video_filename)

    print(standards)


if __name__ == "__main__":
    main()
