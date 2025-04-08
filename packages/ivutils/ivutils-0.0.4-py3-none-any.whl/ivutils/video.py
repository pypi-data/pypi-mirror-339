import cv2
import os
import re
from PIL import Image
import inspect


def get_file_handle(filename: str) -> cv2.VideoCapture:
    return cv2.VideoCapture(filename)


def release_file_handle(handle: cv2.VideoCapture):
    if handle is not None:
        handle.release()


def get_details(handle: cv2.VideoCapture) -> tuple[int, int, int, float]:
    """
    Returns a tuple of length, width, height, fps
    :param handle:
    :return:
    """
    length = int(handle.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(handle.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(handle.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = handle.get(cv2.CAP_PROP_FPS)
    return length, width, height, fps


def convert_sec(timestamp: str):
    """
    Convert a video timestamp (MM:SS) to seconds.

    Args:
        timestamp (str): Timestamp in the format MM:SS.

    Returns:
        int: Timestamp in seconds.
    """
    minutes, seconds = map(int, timestamp.split(':'))
    return minutes * 60 + seconds


def get_frame_ids(time_stamps: list[int], in_handle: cv2.VideoCapture = None, fps: float = None):
    """
    Calculate frame IDs from timestamps.

    Args:
    time_stamps (list[int]): List of timestamps in seconds.
    in_handle (cv2.VideoCapture, optional): Video capture object. Defaults to None.
    fps (int, optional): Frames per second. Defaults to None.

    Returns:
    list[int]: List of frame IDs.

    Raises:
    AssertionError: If neither in_handle nor fps is provided.
    """

    assert (in_handle is None) ^ (fps is None), "This function must take either in_handle or fps as input."

    if fps is None:
        fps = in_handle.get(cv2.CAP_PROP_FPS)

    # Calculate frame IDs
    frame_ids = [int(round(timestamp * fps)) for timestamp in time_stamps]

    # Ensure frame IDs are non-negative
    frame_ids = [max(frame_id, 0) for frame_id in frame_ids]
    return frame_ids


def extract_video_frames(
        out_dir: str,
        out_file_pattern: str,
        in_filename: str = None,
        in_handle: cv2.VideoCapture = None,
        frame_interval: int = 1,
        resize_dim: tuple[int, int] = None,
        start_frame: int = 0,
        end_frame: int = None
):
    assert (in_handle is None) ^ (
            in_filename is None), "This function must take either in_handle or in_filename as input. Not both."

    def resize(frame):
        return cv2.resize(frame, resize_dim)

    def do_nothing(frame):
        return frame

    def process_video(cap: cv2.VideoCapture, start_frame: int, end_frame: int):
        frame_count = start_frame

        max_frames, frame_width, frame_height, _ = get_details(cap)

        # Set the transformation function based on resize_dim
        if resize_dim is not None and (frame_width, frame_height) != resize_dim:
            transform_func = resize
        else:
            transform_func = do_nothing

        if end_frame is None:
            end_frame = max_frames

        assert (0 <= start_frame <= end_frame <= max_frames), f"Invalid range of start_frame: {start_frame} to end_frame: {end_frame}"

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        while True:
            # Read frame from video
            ret, frame = cap.read()

            # Break loop if frame is not read successfully
            if not ret or frame_count >= end_frame:
                break

            # Increment frame counter
            frame_count += 1

            # Check if it's time to extract an image
            if frame_count % frame_interval == 0:
                final_filename = out_file_pattern.format(frame_id=frame_count,
                                                         step_id=(frame_count - start_frame) // frame_interval)
                frame = transform_func(frame)
                print(f"writing to file: {final_filename}")
                # Save resized frame to file
                cv2.imwrite(os.path.join(out_dir, final_filename), frame)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if in_filename is not None:
        hfile = get_file_handle(in_filename)
        process_video(hfile, start_frame, end_frame)
        release_file_handle(hfile)

    elif in_handle is not None:
        process_video(in_handle, start_frame, end_frame)


def reindex_file_sequence(src_dir: str, file_pattern: str, precision: int = 1, init_seq_val: int = 0):
    """
    Analyses all the files of a directory to filter on a sequence pattern. Then iterates over the pattern to find any missing values and re-indexes the files to form a continious sequence

    :param src_dir:
    :param file_pattern:
    :param precision:
    :param init_seq_val:
    :return:
    """

    def sequence_generator():
        seq_id = init_seq_val
        seq_id_pattern = re.compile(file_pattern).pattern
        seq_id_pattern = seq_id_pattern.replace("^", "").replace("$", "").replace("__", "_")
        while True:
            file_name = seq_id_pattern.replace("(?P<seq_id>\\d{6})", f"{seq_id:0{precision}d}").replace("\\", "")
            yield file_name
            seq_id += 1

    files = [f for f in os.listdir(src_dir) if re.search(file_pattern, f)]
    seq_gen = sequence_generator()
    for actual in files:
        expected = next(seq_gen)
        print(f"expected: {expected}")
        if actual != expected:
            print(f"rename {actual} to {expected}")
            os.rename(os.path.join(src_dir, actual), os.path.join(src_dir, expected))
