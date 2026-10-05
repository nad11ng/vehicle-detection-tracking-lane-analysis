import cv2
import imageio.v2 as imageio

from config import VIDEO_PATH, MODEL_PATH, CONF_THRESHOLD, VEHICLE_CLASSES
from detector import YOLODetector
from visualizer import draw_lanes, draw_detection, draw_lane_counts
from lane_manager import analyze_lanes


def main():

    detector = YOLODetector(
        model_path=MODEL_PATH,
        conf_threshold=CONF_THRESHOLD,
        classes=VEHICLE_CLASSES
    )
    
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    width_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_seconds = total_frames / fps
    
    print(f"Frame width is: {width_frame}")
    print(f"Frame height is: {height_frame}")
    print(f"FPS is: {fps:.2f}")
    print(f"Number of frame is: {total_frames}")
    print(f"Video duration is: {duration_seconds:.2f}")
    
    
    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            detections = detector.detect(frame)
            analyzed_detections, lane_counts = analyze_lanes(detections)

            annotated_frame = draw_lanes(frame)

            for detection in analyzed_detections:
                annotated_frame = draw_detection(
                    frame=annotated_frame,
                    detection=detection,
                )

            annotated_frame = draw_lane_counts(
                frame=annotated_frame,
                lane_counts=lane_counts,
            )

            cv2.imshow("Annotated Video", annotated_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()