from implementations.video_object_highlighter_imp import YoloObjectHighlighter


classes_name_path = 'venv\Lib\site-packages\yolov5\data\coco128.yaml'
weights_path = 'configuration/yolov5m.pt'

path_to_source = 'D:\\programms\\Python\\CV_Singularis_Intership\\res\\1.mp4'
output_path = "D:\\programms\\Python\\CV_Singularis_Intership\\output\\"

out_file_name = '1.mp4'

model = YoloObjectHighlighter(weights_path, classes_name_path, (640, 640))
model.highlight_object_on_video(in_path_video=path_to_source,
                                out_path_folder=output_path,
                                out_file_name=out_file_name,
                                highlightable_object_class="cat")
