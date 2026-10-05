import numpy as np
import cv2

LANE_POLYGONS = [
    np.array([[80, 304], [201, 88], [247, 90], [178, 313]], dtype=np.int32),   # Lane 1
    np.array([[187, 315], [255, 86], [298, 88], [310, 320]], dtype=np.int32),  # Lane 2
    np.array([[319, 320], [305, 88], [345, 89], [444, 318]], dtype=np.int32),  # Lane 3
    np.array([[454, 314], [351, 87], [389, 88], [555, 309]], dtype=np.int32)   # Lane 4
]

LANE_COLORS = [ # BGR 
    (255, 0, 0),    # Lane 1: blue
    (0, 255, 0),    # Lane 2: green
    (0, 0, 255),    # Lane 3: red
    (0, 255, 255),  # Lane 4: yellow
]


def get_bottom_center(bbox):
    x1, y1, x2, y2 = bbox
    
    anchor_x = int((x1 + x2) / 2)
    anchor_y = (y2)
    
    anchor_center = (anchor_x, anchor_y)
    
    return anchor_center


def get_lane_id(point):
    for lane_index, polygon in enumerate(LANE_POLYGONS):
        result = cv2.pointPolygonTest(polygon, point, False)
        if result >= 0:
            return lane_index + 1
        
    return None

def analyze_lanes(detections):
    analyzed_detections = []
    lane_counts = [0] * len(LANE_POLYGONS)

    for detection in detections:
        analyzed_detection = detection.copy()

        anchor_point = get_bottom_center(detection["bbox"])
        lane_id = get_lane_id(anchor_point)

        analyzed_detection["anchor_point"] = anchor_point
        analyzed_detection["lane_id"] = lane_id

        if lane_id is not None:
            lane_counts[lane_id - 1] += 1

        analyzed_detections.append(analyzed_detection)

    return analyzed_detections, lane_counts