import numpy as np
import supervision as sv
from inference.models.utils import get_roboflow_model

model = get_roboflow_model(model_id="frc-scouting-application/2", api_key="LleUqOq0BI8fAzfMQGn8")
tracker = sv.ByteTrack()
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()

def callback(frame: np.ndarray, _: int) -> np.ndarray:
    results = model.infer(frame)[0]
    detections = sv.Detections.from_inference(results)
    detections = tracker.update_with_detections(detections)
    
    labels = [
        f"#{tracker_id} {class_id}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]

    annotated_frame = box_annotator.annotate(
        frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(
        annotated_frame, detections=detections, labels=labels)
    return trace_annotator.annotate(
        annotated_frame, detections=detections)

sv.process_video(
    source_path="video.mp4",
    target_path="result.mp4",
    callback=callback
)