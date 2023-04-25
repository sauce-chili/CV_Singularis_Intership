from dataclasses import dataclass
import numpy as np


@dataclass
class PredictionResult:
    class_name: str
    confidence: float
    bbox: np.ndarray
