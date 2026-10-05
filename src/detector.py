from pathlib import Path
from ultralytics import YOLO



class YOLODetector:
    def __init__(self, model_path, conf_threshold, classes):
        self.model_path = Path(model_path)
        self.conf_threshold = conf_threshold
        self.classes = classes
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model is not exists. Model Path is {self.model_path}")
        
        self.model = YOLO(str(self.model_path))
        
    def detect(self, frame):
        # result = self.model.predict ... has been replace by track
        result = self.model.track(
            source=frame,
            conf=self.conf_threshold,
            verbose=False,
            classes=self.classes,
            persist=True, # Preserve tracks between consecutive frames
            tracker="bytetrack.yaml"          
        )[0]
        
        boxes = result.boxes
        
        detections = []
        
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            track_id = int(box.id[0]) if box.id is not None else None
            detections.append({             # Add 1 dictionary in detections list
                "bbox": (x1, y1, x2, y2),   # 1 Dictionayry contains 4 attributes 
                "conf": confidence,
                "class_id": class_id,
                "class_name": class_name,
                "track_id": track_id
            })

        return detections