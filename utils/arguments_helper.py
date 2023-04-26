import os
from argparse import ArgumentParser
from datetime import datetime
from enum import Enum


class __ArgsTemplate(Enum):
    IN_VIDEO = '--in_video'
    HIGHLIGHTED_OBJECT = '--highlighted_object'
    OUT_PATH = '--out_path'
    OUT_FILE_NAME = '--out_file_name'


class __HelpArgsTemplate(Enum):
    IN_VIDEO = 'path to video which you want to highlight an object'
    HIGHLIGHTED_OBJECT = 'name of the object to highlight'
    OUT_PATH = 'path to the output directory or file(with suffix)'
    OUT_FILE_NAME = 'name of the source file with suffix(if not assigned, ' \
                    'it will be generated from the name of the source)'


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(__ArgsTemplate.IN_VIDEO.value, type=str, required=True,
                        help=__HelpArgsTemplate.IN_VIDEO.value)

    parser.add_argument(__ArgsTemplate.HIGHLIGHTED_OBJECT.value, type=str, required=True,
                        help=__HelpArgsTemplate.HIGHLIGHTED_OBJECT.value)

    parser.add_argument(__ArgsTemplate.OUT_PATH.value, type=str, required=True,
                        help=__HelpArgsTemplate.OUT_PATH.value)

    parser.add_argument(__ArgsTemplate.OUT_FILE_NAME.value, type=str,
                        help=__HelpArgsTemplate.OUT_FILE_NAME.value)

    args = parser.parse_args()

    # Check if input video file exists
    if not os.path.isfile(args.in_video):
        raise FileNotFoundError(f'Input video file {args.in_video} does not exist.')

    # Check if output path is a directory
    if os.path.isdir(args.out_path):

        if not args.out_file_name:
            # Generate output file name using input video file name and current datetime
            input_video_name = os.path.basename(args.in_video)
            input_video_name_no_ext, input_video_ext = os.path.splitext(input_video_name)
            current_datetime_str = datetime.now().strftime("%d-%m-%Y-%H-%M")
            args.out_file_name = f'{input_video_name_no_ext}_{current_datetime_str}{input_video_ext}'

        args.out_path = os.path.join(args.out_path, args.out_file_name)

    elif not os.path.exists(args.out_path):
        raise FileNotFoundError(f'Output path {args.out_path} does not exist.')

    return args
