from typing import Protocol


class VideoObjectHighlighter(Protocol):

    def highlight_object_on_video(self, in_path_video: str, highlightable_object_class: str,
                                  out_path_video: str) -> None:
        ...

    def get_classes_object(self) -> dict:
        ...
