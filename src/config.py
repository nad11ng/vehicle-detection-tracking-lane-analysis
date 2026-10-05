from pathlib import Path


PARENT_DIR = Path(__file__).resolve().parent.parent

VIDEO_PATH = PARENT_DIR / "inputs" / "videos" / "autobahn.mp4"
MODEL_PATH = PARENT_DIR / "models" / "yolo26n.pt"


CONF_THRESHOLD = 0.5

VEHICLE_CLASSES = [
    2,  # car
    5,  # bus
    7,  # truck
]