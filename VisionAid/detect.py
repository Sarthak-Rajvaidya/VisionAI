import time
import cv2
from ultralytics import YOLO


def load_model():
    # Downloads yolov8n.pt (about 6 MB) automatically on first run
    return YOLO("yolov8n.pt")


def detect(model, frame, conf=0.5):
    """Run detection on one frame and return a clean list of results."""
    results = model(frame, conf=conf, verbose=False)[0]
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        detections.append({
            "label": model.names[int(box.cls[0])],
            "conf": float(box.conf[0]),
            "box": (x1, y1, x2, y2),
        })
    return detections


def draw(frame, detections):
    for d in detections:
        x1, y1, x2, y2 = d["box"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 180, 0), 2)
        text = f'{d["label"]} {d["conf"]:.2f}'
        cv2.putText(frame, text, (x1, max(y1 - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 180, 0), 2)


def main():
    model = load_model()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW avoids slow startup on Windows
    if not cap.isOpened():
        print("Could not open camera. Try changing 0 to 1 in VideoCapture.")
        return

    print("Running. Press 'q' in the video window to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Failed to read frame.")
            break

        start = time.time()
        detections = detect(model, frame)
        latency_ms = (time.time() - start) * 1000

        draw(frame, detections)
        cv2.putText(frame, f"Detection: {latency_ms:.0f} ms", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("VisionAid", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()