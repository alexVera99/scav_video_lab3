"""Solution for Exercise 3."""
import pathlib
import utils as ut


def get_video_dims(filename_path: pathlib.Path) -> tuple:
    """
    Get resolution of the video frames.

    :param filename_path:
    :return: width and height of the video.
    """
    cmd = ["ffprobe", "-v", "error",
           "-select_streams", "v:0",
           "-show_entries", "stream=width,height",
           "-of", "csv=s=x:p=0", filename_path]

    output, stderr = ut.exec_in_shell_wrapper(cmd)

    ut.check_shell_stderr(stderr, f"Could not get the size of "
                                  f"the video {filename_path}")

    width, height = output.decode().replace("\n", "").split("x")

    return int(width), int(height)


def resize_video(filename_path: pathlib.Path,
                 width: int = -1, height: int = -1,
                 output_filename: str = ""):
    """
    Resize in the given dimensions. Inspired from \
    https://ottverse.com/change-resolution-resize-scale-video-using-ffmpeg/.

    :param filename_path: video filename path
    :param height: expected height
    :param width: expected width
    :param output_filename: output filename
    :return: created video filename
    """
    w_video, h_video = get_video_dims(filename_path)

    width, height = get_new_scaling(w_video, h_video, width, height)

    if output_filename == "":
        video_name = filename_path.name.split(".")[0]
        output_filename = f"{video_name}_resize_{width}_{height}"

    output_filename_path = ut.rename_from_path(filename_path, output_filename)

    cmd = ["ffmpeg", "-y", "-i", filename_path,
           "-aspect:v", f"{width}:{height}",
           "-vf", f"scale={width}:{height}",
           "-preset", "slow", "-crf", "18",
           output_filename_path]

    _, stderr = ut.exec_in_shell_wrapper(cmd)

    ut.check_shell_stderr(stderr,
                          f"Could not resize the video {filename_path}")

    return output_filename_path


def force_to_be_multiple_of_2(num: int):
    """
    Force a number to be even.

    :param num: any integer number
    :return: even integer number
    """
    if num % 2 == 0:
        return num
    return num + 1


def get_new_scaling(width: int, height: int,
                    target_width: int = -1,
                    target_height: int = -1) -> tuple:
    """
    Given a dimension, it computes the other dimension as a multiple of 2.\
    Only one target dimension should be given, and it should be a multiple
    of 2. Example: automatic_scaling(w, h, target_width = 280), or \
    automatic_scaling(w, h, target_height = 280).

    :param width: original width
    :param height: original height
    :param target_width: target width. If -1, it will be computed
    :param target_height: target height. If -1, it will be computed
    :return: a tuple with the new dimensions: (w, h)
    """
    if target_width == -1 and target_height == -1:
        raise Exception("At least one dimension should be given")

    if target_width == -1:
        if target_height % 2 != 0:
            raise Exception(f"target_height ({target_height}) is not "
                            "multiple of 2.")
        result = round(target_height / height * width)

        result = force_to_be_multiple_of_2(result)

        w_h = (result, target_height)

    elif target_height == -1:
        if target_width % 2 != 0:
            raise Exception(f"target_height ({target_width}) is not "
                            "multiple of 2.")
        result = round(target_width / width * height)

        result = force_to_be_multiple_of_2(result)

        w_h = (target_width, result)

    else:
        w_h = (target_width, target_height)

    return w_h


def main():
    """
    Test the above functions.

    :return no return
    """
    video_filename = pathlib.Path("../data/bbb.mp4")

    resolutions_w_h = [[-1, 720], [-1, 480],
                       [360, 240], [160, 120]]

    for _w, _h in resolutions_w_h:
        out_filename = resize_video(video_filename, _w, _h)
        print(f"Video created in {out_filename}")


if __name__ == "__main__":
    main()
