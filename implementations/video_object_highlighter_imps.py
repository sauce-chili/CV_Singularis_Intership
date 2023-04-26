from pathlib import Path
from typing import Iterable

import torch
import numpy as np
import cv2

from yolov5.utils.dataloaders import LoadImages
from yolov5.utils.general import scale_boxes, non_max_suppression, check_img_size
from yolov5.utils.torch_utils import select_device
from yolov5.models.common import DetectMultiBackend

from implementations.data.prediction_result import PredictionResult
from entities.video_object_highlighter import VideoObjectHighlighter


class YoloObjectHighlighter(VideoObjectHighlighter):

    def __init__(self, weigh_path: str, data_classes: str, input_shape: tuple):

        name = Path(weigh_path)
        path = name.with_suffix('.pt') if name.suffix == '' and not name.is_dir() else name  # checkpoint path

        self.__device = select_device("cpu")
        # ATTENTION: If the path cannot be found, the download will start from the yolo git hub(its very long)
        model = DetectMultiBackend(path, device=self.__device, data=data_classes, dnn=False, fp16=False)

        self.__classes = model.names

        self.__img_shape = check_img_size(input_shape, model.stride)
        model.warmup(imgsz=(1, 3, *self.__img_shape))  # Run inference
        self.__model = model

        self.__conf_thresh = 0.65
        self.__iou_thresh = 0.50

        # for display debug info TODO remove this
        self.__debug = False

    def highlight_object_on_video(self, in_path_video: str, highlightable_object_class: str,
                                  out_path_video: str):
        # TODO check if the paths exists

        # Dataloader
        frame_provider = LoadImages(in_path_video, img_size=self.__img_shape,
                                    stride=self.__model.stride, auto=self.__model.pt)

        video_writer = self.__get_video_writer(frame_provider.cap, out_path_video)

        for _, transform_img, original_img, vid_cap, _ in frame_provider:
            # frame transformation for input-layer
            transform_img = self.__convert_to_input_img(transform_img)

            if self.__debug: cv2.imshow("Origin", original_img)

            # predict
            pred = self.__model(transform_img)
            # normalizing predictions by removing overlapping predictions
            pred = non_max_suppression(pred, self.__conf_thresh, self.__iou_thresh, agnostic=False)

            # conversion of predictions to ``PredictionResult's``
            detected_object: list[PredictionResult] = self.__processing_prediction(pred, transform_img,
                                                                                   original_img)

            # selection of only necessary predictions
            filter_func = lambda det: det.class_name == highlightable_object_class
            detected_object = list(filter(filter_func, detected_object))

            if detected_object == []: continue

            # mask where only objects are selected ``highlightable_object_class``
            mask = self.__highlight_object(original_img, detected_object)

            # save frame with ``highlightable_object_class``
            video_writer.write(mask)

            if self.__debug:
                cv2.imshow("Mask", mask)
                print(list(detected_object))
                cv2.waitKey(33)

        video_writer.release()

    def __get_video_writer(self, cam_capture: cv2.VideoCapture,
                           out_video_path: str) -> cv2.VideoWriter:

        w = cam_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = cam_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        shape = (int(w), int(h))

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        fps = cam_capture.get(cv2.CAP_PROP_FPS)

        return cv2.VideoWriter(out_video_path, fourcc, fps, shape)

    def __convert_to_input_img(self, image):

        im = torch.from_numpy(image).to(self.__device)
        im = im.half() if self.__model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.mp4.0

        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        return im

    def __processing_prediction(self, pred, transform_img, original_img) -> list[PredictionResult]:

        result: list[PredictionResult] = []

        for det in filter(lambda d: d is not None, pred):  # per image

            im0 = original_img.copy()  # , getattr(frame_provider, 'frame', 0)

            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_boxes(transform_img.shape[2:], det[:, :4], im0.shape).round()

            result += [
                PredictionResult(
                    class_name=self.__classes[int(cls)],
                    confidence=float(conf),
                    bbox=np.array([int(cord) for cord in xyxy], dtype=int)
                )
                for *xyxy, conf, cls in reversed(det)
            ]

        return result

    def __highlight_object(self, image: np.ndarray, detected_objects: Iterable[PredictionResult]) -> np.ndarray:

        mask = np.zeros_like(image)

        for x_min, y_min, x_max, y_max in [det.bbox for det in detected_objects]:

            mask[y_min: y_max, x_min: x_max] = image[y_min: y_max, x_min: x_max]

        return mask

    def get_classes_object(self):
        return self.__classes
