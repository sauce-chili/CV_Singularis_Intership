from pprint import pprint

from utils.config import ObjectHighlighterConfig
from utils.arguments_helper import parse_args

from implementations.video_object_highlighter_imps import YoloObjectHighlighter


def main(args):
    cfg = ObjectHighlighterConfig()

    object_highlighter = YoloObjectHighlighter(
        weigh_path=cfg.weigh,
        data_classes=cfg.classes_name,
        input_shape=cfg.input_shape  # default for yolov5 img sizes
    )

    highlightable_object = args.highlighted_object

    if highlightable_object not in \
            (supported_highlighting_objects := object_highlighter.get_classes_object().values()):
        print(f'Highlighting of object "{highlightable_object}" is not supported by this version of the program.\n')
        print("Supported for highlighting following objects:")
        pprint(tuple(supported_highlighting_objects))
        exit()

    in_path = args.in_video
    out_path = args.out_path

    print("Highlighting an object...")

    object_highlighter.highlight_object_on_video(
        in_path_video=in_path,
        highlightable_object_class=highlightable_object,
        out_path_video=out_path
    )

    print("Done.")


if __name__ == '__main__':
    args = None
    try:
        args = parse_args()
    except FileNotFoundError as fnf_exp:
        print(str(fnf_exp))
        exit()
    except Exception as exp:
        print(str(exp))
        print("Invalid args. Exit...")
        exit()

    main(args)
