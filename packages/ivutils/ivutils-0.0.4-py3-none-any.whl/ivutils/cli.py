import argparse
import sys
import ast
from configparser import SectionProxy, ConfigParser
import ivutils.video as vidutils
import ivutils.image as imgutils

def parse(s:str, default: any=None)-> any: return ast.literal_eval(s) if s else default


def extract_frames(sect: SectionProxy):
    in_filename = sect["in_filename"]
    out_directory = sect["out_directory"]
    out_file_pattern = sect["out_file_pattern"]
    frame_intervals = parse(sect["frame_intervals"], [])
    frame_ranges = parse(sect["frame_ranges"], [])
    resize_dim = parse(sect["resize_dim"], (320,240))

    hfile = vidutils.get_file_handle(in_filename)
    _, _, _, fps = vidutils.get_details(hfile)
    for i in range(len(frame_ranges)):
        f_interval = frame_intervals[i]
        f_range = frame_ranges[i]
        start_sec = vidutils.convert_sec(f_range[0])
        end_sec = vidutils.convert_sec(f_range[1])
        start_frame, end_frame = vidutils.get_frame_ids([start_sec, end_sec], fps=fps)
        out_file = out_file_pattern.format(vid_id=i)
        out_dir = out_directory.format(vid_id=i)

        vidutils.extract_video_frames(
            out_dir=out_dir,
            out_file_pattern = out_file,
            in_handle=hfile,
            frame_interval=f_interval,
            resize_dim=resize_dim,
            start_frame=start_frame,
            end_frame=end_frame
        )
    vidutils.release_file_handle(hfile)


def resize_images(sect: SectionProxy):
    root_directory = sect["root_directory"]
    out_file_format = sect["out_file_format"]
    search_ext = parse(sect["search_ext"], ["jpg"])
    resize_dim = parse(sect["resize_dim"], (640, 480))
    mappings_file = parse(sect["mappings_file"], None)
    imgutils.resize_images(root_directory, out_file_format, search_ext, resize_dim, mappings_file)

def batch_images(sect: SectionProxy):
    src_dirs = parse(sect["source_directories"], [])
    src_dir_pattern = sect["src_dir_pattern"]
    in_pattern = sect["input_pattern"]
    out_file_format = sect["output_file_format"]
    grid_size = parse(sect["grid_size"], (4,16))
    wrap_last_img = parse(sect["wrap_last_image"],False)
    imgutils.batch_image_grid(in_pattern, out_file_format, grid_size, src_dirs, src_dir_pattern, wrap_last_img)

def run():
    job_types = ["extract_frames", "resize_images", "batch_images"]

    parser = argparse.ArgumentParser(description="CLI tool for Image / Video processing tasks")

    parser.add_argument('job_type', choices=job_types,
                        help='Type of job to execute (choices: {})'.format(', '.join(job_types)))

    parser.add_argument('config_filename', type=str, help='Path to the INI file')

    args = parser.parse_args()
    job_type, config_filename = vars(args).values()

    config = ConfigParser()
    config.read(args.config_filename)
    sect = config[job_type]

    if job_type == "extract_frames":
        extract_frames(sect)
    elif job_type == "batch_images":
        batch_images(sect)
    else:
        raise ValueError(f"Invalid value for input arg [job_type]: {job_type}")

if __name__ == "__main__":
    run()