import numpy as np
import pandas as pd
import supervision as sv
from inference.models.utils import get_roboflow_model

model = get_roboflow_model(model_id="frc-scouting-application/2", api_key="LleUqOq0BI8fAzfMQGn8")
tracker = sv.ByteTrack()
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# Initialize a dictionary to hold previous positions and velocities
object_data = {}

# List to store results for CSV
results_list = []


def callback(frame: np.ndarray, frame_index: int) -> np.ndarray:
    global object_data
    results = model.infer(frame)[0]
    detections = sv.Detections.from_inference(results)
    detections = tracker.update_with_detections(detections)

    # Process each detection
    for class_id, tracker_id, bbox in zip(detections.class_id, detections.tracker_id, detections.xyxy):
        current_position = np.array([(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2])  # Center of the bounding box
        if tracker_id not in object_data:
            object_data[tracker_id] = {
                'previous_position': current_position,
                'velocity': np.array([0.0, 0.0]),
                'acceleration': np.array([0.0, 0.0]),
                'last_frame': frame_index
            }
        else:
            previous_position = object_data[tracker_id]['previous_position']
            time_elapsed = 1  # Assuming frame rate is constant and equals 1 second for simplicity

            # Calculate distance traveled
            distance = np.linalg.norm(current_position - previous_position)
            velocity = distance / time_elapsed

            # Calculate acceleration
            previous_velocity = object_data[tracker_id]['velocity']
            acceleration = (velocity - np.linalg.norm(previous_velocity)) / time_elapsed

            # Update the object data
            object_data[tracker_id]['previous_position'] = current_position
            object_data[tracker_id]['velocity'] = np.array([velocity * np.cos(np.arctan2(current_position[1] - previous_position[1], current_position[0] - previous_position[0]))),velocity * np.sin(np.arctan2(current_position[1] - previous_position[1], current_position[0] - previous_position[0]))])
            object_data[tracker_id]['acceleration'] = acceleration
            object_data[tracker_id]['last_frame'] = frame_index

            # Store results for CSV
            results_list.append({
                'tracker_id': tracker_id,
                'frame_index': frame_index,
                'position_x': current_position[0],
                'position_y': current_position[1],
                'velocity': np.linalg.norm(object_data[tracker_id]['velocity']),
                'acceleration': object_data[tracker_id]['acceleration'],
            })

            labels = [
        f"#{tracker_id} {results.names[class_id]}"
        for class_id, tracker_id
            in zip(detections.class_id, detections.tracker_id)
    ]

    annotated_frame = box_annotator.annotate(frame.copy(), detections = detections)
    return label_annotator.annotate(
        annotated_frame, detections=detections, labels=labels)


sv.process_video(
    source_path="people-walking.mp4",
    target_path="result.mp4",
    callback=callback
)

# Save results to CSV after processing the video
df = pd.DataFrame(results_list)
df.to_csv("tracking_results.csv", index=False)
