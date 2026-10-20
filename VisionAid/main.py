import time

import cv2

from detect import load_model, detect, draw
from priority import prioritise
from speak import Speaker

COOLDOWN = 6         # seconds before the same message repeats
URGENT_COOLDOWN = 2  # urgent warnings repeat faster


def main():
    model = load_model()
    speaker = Speaker()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Could not open camera. Try changing 0 to 1 in VideoCapture.")
        return

    last_spoken = {}
    last_text = ""
    print("Running. Press 'q' in the video window to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        h, w = frame.shape[:2]

        start = time.time()
        detections = detect(model, frame)
        latency_ms = (time.time() - start) * 1000

        items = prioritise(detections, w, h)

        # Speak ONE message per frame: the most important one that is off cooldown
        now = time.time()
        for item in items:
            key = (item["label"], item["zone"], item["level"])
            wait = URGENT_COOLDOWN if item["urgent"] else COOLDOWN
            if now - last_spoken.get(key, 0) > wait:
                if speaker.say(item["text"], urgent=item["urgent"]):
                    last_spoken[key] = now  # only mark as spoken if it was really queued
                    last_text = item["text"]
                    break

        draw(frame, detections)
        cv2.putText(frame, f"Detection: {latency_ms:.0f} ms", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, last_text, (10, h - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 120, 0), 2)
        cv2.imshow("VisionAid", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    speaker.stop()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()