import cv2
from lane_manager import LANE_POLYGONS, LANE_COLORS


def draw_lanes(frame):
    annotated_frame = frame.copy()
        
    for polygon, color in zip(LANE_POLYGONS, LANE_COLORS):
        overlay = annotated_frame.copy()
    
        cv2.fillPoly(
            img=overlay,
            pts=[polygon],
            color=color,
        )
    
        cv2.addWeighted(
            src1=overlay,
            alpha=0.2,
            src2=annotated_frame,
            beta=0.8,
            gamma=0,
            dst=annotated_frame,
        )
    
        cv2.polylines(
            img=annotated_frame,
            pts=[polygon],
            isClosed=True,
            color=color,
            thickness=2,
        )
            
    return annotated_frame

def draw_detection(frame, detection):
    x1, y1, x2, y2 = detection["bbox"]
    anchor_point = detection["anchor_point"]
    lane_id = detection["lane_id"]
    
    cv2.rectangle(
        img=frame,
        pt1=(x1, y1),
        pt2=(x2, y2),
        color=(255, 255, 0),
        thickness=2
    )
    
    cv2.circle(
        img=frame,
        center=anchor_point,
        radius=4,
        color=(255, 0, 255),
        thickness=-1
    )
    
    confidence = detection["conf"]
    class_name = detection["class_name"]
    track_id = detection["track_id"]
                
    # track_text = track_id if track_id is not None else "?"
    if track_id is not None:
        track_text = track_id
    else:
        track_text = "?"
                    
    lane_text = lane_id if lane_id is not None else "?"
    label = (
        f"{class_name}| ID {track_text} |" 
        f"Lane {lane_text} | {confidence:.2f}"
    )
    
    cv2.putText(
        img=frame,
        text=label,
        org=(x1, max(y1 - 10, 20)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.5,
        color=(255, 255, 255),
        thickness=1,
    )
    
    return frame

def draw_lane_counts(frame, lane_counts):
    for lane_index, count in enumerate(lane_counts):
        text_count = f"Lane {lane_index + 1}: {count}"
                
        text_x = 20
        text_y = 30 * (lane_index + 1)
        text_color = LANE_COLORS[lane_index]
                
        cv2.putText(
            img=frame,
            text=text_count,
            org=(text_x, text_y),
            fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
            fontScale=0.5,
            color=text_color,
            thickness=2
        )
        
    return frame