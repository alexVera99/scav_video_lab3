"""Exercise 5: It is an application merging the behaviour of all the\
other exercises."""
import pathlib
import json

import src.exercise_1 as ex_1
import src.exercise_2 as ex_2
import src.exercise_3 as ex_3
import src.exercise_4 as ex_4


def execute_exercise_1_option():
    """
    Execute logic for exercise 1.

    :return: no return
    """
    video_filename = input("Video filename (it must be a valid relative"
                           " or absolute valid path): ")
    video_filename = pathlib.Path(video_filename)

    parser = ex_1.FfmpegMetadataParser()

    metadata = parser.get_metadata(video_filename)

    print("\nThe metadata found is:\n")
    print(json.dumps(metadata, indent=4))


def execute_exercise_2_option():
    """
    Execute logic for exercise 2.

    :return: no return
    """
    video_filename = input("Video filename (it must be a valid relative"
                           " or absolute valid path): ")
    video_filename = pathlib.Path(video_filename)

    start_cut = int(input("Second number to start cut: "))
    n_secs_cut = int(input("Number of seconds of the resulting video: "))

    mp4_container = ex_2.run_pipeline(video_filename,
                                      start_cut,
                                      n_secs_cut)

    print(f"Video created in {mp4_container}")


def execute_exercise_3_option():
    """
    Execute logic for exercise 3.

    :return:
    """
    video_filename = input("Video filename (it must be a valid relative"
                           " or absolute valid path): ")
    video_filename = pathlib.Path(video_filename)

    target_width = int(input("Target width (must be multiple of 2 or "
                             "-1 to create automatically based on the "
                             "other dimension):\n"))

    target_height = int(input("Target height (must be multiple of 2 or "
                              "-1 to create automatically based on the "
                              "other dimension):\n"))

    out_filename = ex_3.resize_video(video_filename,
                                     target_width,
                                     target_height)

    print(f"Video created in {out_filename}")


def execute_exercise_4_option():
    """
    Execute logic for exercise 4.

    :return: no return
    """
    video_filename = input("Video filename (it must be a valid relative"
                           " or absolute valid path): ")

    analyzer = ex_4.BroadcastingAnalyzer()
    standards = analyzer.analyze(video_filename)

    print("\nThe recommended standards are:")
    print("".join([f"{i}) {_st}\n" for i, _st in enumerate(standards, start=1)]))


def main():
    """
    Execute the logic of the main menu to select which exercise you \
    want to use.

    :return: no return
    """
    n_options = 4
    options = list(range(1, n_options + 1))

    while True:
        option = int(input("Choose the exercise: \n"
                           "1) Exercise 1: Extract metadata from mp4 video\n"
                           "2) Exercise 2: Create a mp4 container with video, "
                           "mp3 audio and aac audio with lower bitrate.\n"
                           "3) Exercise 3: Resize a video.\n"
                           "4) Exercise 4: Analyze the possible broadcasting"
                           "standard that a video could fit\n"))

        if option in options:
            print(f"\nYou have selected option {option}\n")
            break

        print("Please, provide a valid option")
    if option == 1:
        execute_exercise_1_option()
    if option == 2:
        execute_exercise_2_option()
    if option == 3:
        execute_exercise_3_option()
    if option == 4:
        execute_exercise_4_option()


if __name__ == "__main__":
    main()
