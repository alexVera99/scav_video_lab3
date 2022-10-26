"""Solution for Exercise 1."""


import pathlib
import src.lib.utils as ut
import grep.internals as grep


class FfmpegMetadataParser:
    def __wrapper_grep(self, text, pattern):
        matches = grep.Matches(
            text,
            grep.Context(),
            grep.Pattern(pattern)
        )

        return tuple(matches)


    def get_metadata(self, filename_path: pathlib.Path) -> dict:
        """
        Gets metadata from a video container
        :param filename_path: video filename path
        :return: dictionary containing the metadata
        """

        cmd = ["ffmpeg", "-i", filename_path]

        _, stderr = ut.exec_in_shell_wrapper(cmd)

        ut.check_shell_stderr(stderr)

        raw_data = stderr.decode('ascii')

        # Duration
        duration_raw = str(self.__wrapper_grep(raw_data, "Duration")[0])
        print(duration_raw)
        duration = duration_raw.split(",", 1)[0].split(": ", 1)[1]
        print(duration)

        # bitrate
        bitrate_raw = str(self.__wrapper_grep(raw_data, "bitrate")[0])
        bitrate = duration_raw.split(",")[2].split(": ", 1)[1]

        print(bitrate)

        # Streams
        streams_raw = self.__wrapper_grep(raw_data, "Stream")
        print(streams_raw)
        num_streams = len(tuple(streams_raw))
        print(num_streams)
        streams = []

        for _s in streams_raw:
            _s_str = str(_s)

            name, v_type, other_data = _s_str.split(": ", 2)
            name = name.lstrip(" ")
            codec = other_data.split(", ", 1)[0]

            stream_data = {
                "name": name,
                "type": v_type,
                "codec": codec
            }

            streams.append(stream_data)

        # create the metadata dict
        metadata = {
            "duration": duration,
            "bitrate": bitrate,
            "num_streams": num_streams,
            "streams": streams
        }

        return metadata


def main():
    parser = FfmpegMetadataParser()

    video_filename = pathlib.Path("../../data/bbb.mp4")

    metadata = parser.get_metadata(video_filename)

    print(metadata)


if __name__ == "__main__":
    main()
