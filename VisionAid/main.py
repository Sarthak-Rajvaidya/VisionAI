import time

import cv2

from detect import load_model, detect, draw
from speak import Speaker

COOLDOWN = 5  # seconds before the same object is announced again


def main():
    model = load_model()
    speaker = Speaker()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Could not open camera. Try changing 0 to 1 in VideoCapture.")
        return

    last_spoken = {}  # label -> time it was last announced
    print("Running. Press 'q' in the video window to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        start = time.time()
        detections = detect(model, frame)
        latency_ms = (time.time() - start) * 1000

        now = time.time()
        for d in sorted(detections, key=lambda d: -d["conf"]):
            label = d["label"]
            if now - last_spoken.get(label, 0) > COOLDOWN:
                speaker.say(label)
                last_spoken[label] = now

        draw(frame, detections)
        cv2.putText(frame, f"Detection: {latency_ms:.0f} ms", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("VisionAid", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    speaker.stop()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()