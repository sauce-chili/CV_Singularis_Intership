import os.path
import yaml


class ObjectHighlighterConfig:

    def __init__(self):
        path = "configuration/ObjectHighlighterConfig.yaml"
        cfg = None

        if not os.path.isfile(path):
            raise FileExistsError(f"Config file {path} isn't exist.")

        with open(path, 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)

        self.weigh = cfg["weigh"]
        self.classes_name = cfg["classes_name"]

        w = int(cfg["input_shape"]["width"])
        h = int(cfg["input_shape"]["height"])
        self.input_shape = (w, h)
