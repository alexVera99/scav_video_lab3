"""Solution for exercise 2."""
import pathlib
import src.lib.utils as ut
import datetime
from enum import Enum
import src.lib.exercise_1 as ex1
import json


class Codec(Enum):
    ACC = "m4a"
    MP3 = "mp3"


def cut_n_secs(filename_path: pathlib.Path, start: int,
               n_secs: int, output_filename: str = ""):
    """
    Cut N seconds of the video at a given starting time.

    :param filename_path: path of the video to cut
    :param start: starting time in seconds
    :param n_secs: number of seconds to cut
    :param output_filename: filename of the output video
    :return: filename path of the created video
    """
    if output_filename == "":
        img_name = filename_path.name.split(".")[0]
        output_filename = f"{img_name}_cut_{start}_{n_secs}"

    output_filename_path = ut.rename_from_path(filename_path, output_filename)

    start_sexagesimal = str(datetime.timedelta(seconds=start))
    n_sexagesimal = str(datetime.timedelta(seconds=n_secs))

    cmd = ["ffmpeg", "-y", "-i", filename_path,
           "-ss", start_sexagesimal,
           "-t", n_sexagesimal,
           output_filename_path]

    _, stderr = ut.exec_in_shell_wrapper(cmd)

    ut.check_shell_stderr(stderr, f"Could not cut the video {filename_path}")

    return output_filename_path


def export_audio_from_video(filename_path: pathlib.Path,
                            codec: Codec,
                            reduce_bitrate: bool = False,
                            output_filename: str = ""):
    """
    Extract the audio from a given video and export it as\
    MP3 stereo track.

    :param filename_path: path of the video
    :param codec: enum of type Codec
    :param reduce_bitrate: reduce the bitrate of the audio
    :param output_filename: filename of the output video
    :return: filename path of the created video
    """

    if output_filename == "":
        video_name = filename_path.name.split(".")[0]
        output_filename = f"{video_name}"

    output_filename_path = ut.rename_from_path(filename_path,
                                               output_filename,
                                               codec.value)
    if reduce_bitrate:
        cmd = ["ffmpeg",
               "-i", filename_path,
               "-map", "0:a",
               "-b:a", " 64k",
               "-y", output_filename_path]
    else:
        cmd = ["ffmpeg",
               "-i", filename_path,
               "-map", "0:a",
               "-y", output_filename_path]

    _, stderr = ut.exec_in_shell_wrapper(cmd)

    ut.check_shell_stderr(stderr,
                          f"Could extract the audio from {filename_path}")

    return output_filename_path


def build_container(video_filename_path: pathlib.Path,
                    mp3_audio_filename_path: pathlib.Path,
                    acc_audio_filename_path: pathlib.Path,
                    output_filename_path: pathlib.Path = pathlib.Path("")):
    """

    :param video_filename_path: video path
    :param mp3_audio_filename_path: mp3 audio path
    :param acc_audio_filename_path: acc audio path
    :param output_filename_path: output filename
    :return:
    """
    if output_filename_path == pathlib.Path(""):
        output_filename_path = pathlib.Path("output")
        output_filename_path = ut.rename_from_path(video_filename_path,
                                                   output_filename_path,
                                                   "mp4")

    cmd = ["ffmpeg", "-y",
           "-i", video_filename_path,
           "-i", mp3_audio_filename_path,
           "-i", acc_audio_filename_path,
           "-map", "0:v", "-c:v", "copy",
           "-map", "1:a", "-c:a", "copy",
           "-map", "2:a", "-c:a", "copy",
           output_filename_path]

    _, stderr = ut.exec_in_shell_wrapper(cmd)

    ut.check_shell_stderr(stderr,
                          f"Could join in a container the streams:\n"
                          f" {video_filename_path},\n"
                          f"{mp3_audio_filename_path} and\n"
                          f"{acc_audio_filename_path}")

    return output_filename_path


def run_pipeline(filename_path: pathlib.Path,
                 cut_start=0,
                 cut_duration=60):
    """
    Cut video at cut_start second with a duration of cut_duration seconds, \
    then it creates a mp4 video stream, mp3 audio stream and acc audio \
    stream. Finally, it creates a mp4 containter containing the 3 streams.

    :param filename_path: input video filename
    :param cut_start: second to start cutting
    :param cut_duration: duration of the cut video
    :return: mp4 container path
    """
    cut_filename_path = cut_n_secs(filename_path, cut_start, cut_duration)

    audio_mp3_filename_path = export_audio_from_video(cut_filename_path,
                                                      Codec.MP3)
    audio_acc_filename_path = export_audio_from_video(cut_filename_path,
                                                      Codec.ACC,
                                                      reduce_bitrate=True)
    mp4_container_path = build_container(cut_filename_path,
                         audio_mp3_filename_path,
                         audio_acc_filename_path)

    return mp4_container_path



def main():
    """
    Test the above functions.

    :return no return
    """
    filename_path = pathlib.Path("../../data/bbb.mp4")

    mp4_container = run_pipeline(filename_path, 0, 60)

    parser = ex1.FfmpegMetadataParser()

    mp4_container_metadata = parser.get_metadata(mp4_container)
    print(json.dumps(mp4_container_metadata, indent=4))


if __name__ == "__main__":
    main()
