import sys
import time

import cv2
from ultralytics import YOLOWorld

from priority import describe
from speak import Speaker

SPEAK_EVERY = 3     # seconds between guidance messages
NOT_FOUND_EVERY = 8  # seconds between "not seen" hints


def main():
    target = " ".join(sys.argv[1:]).strip() or input("What should I find? ").strip()
    if not target:
        print("Nothing to find.")
        return

    model = YOLOWorld("yolov8s-worldv2.pt")  # downloads on first run
    model.set_classes([target])              # tell it what to look for
    speaker = Speaker()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Could not open camera. Try changing 0 to 1.")
        return

    speaker.say(f"Looking for {target}")
    last_msg_time = 0
    last_text = f"Looking for {target}"
    print(f"Searching for: {target}. Press 'q' to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        h, w = frame.shape[:2]

        results = model(frame, conf=0.25, verbose=False)[0]
        best = None
        for box in results.boxes:
            conf = float(box.conf[0])
            if best is None or conf > best["conf"]:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                best = {"label": target, "conf": conf, "box": (x1, y1, x2, y2)}

        now = time.time()
        if best:
            x1, y1, x2, y2 = best["box"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 180, 0), 2)
            cv2.putText(frame, f'{target} {best["conf"]:.2f}', (x1, max(y1 - 8, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 180, 0), 2)
            if now - last_msg_time > SPEAK_EVERY:
                info = describe(best, w, h)
                if speaker.say(info["text"]):
                    last_msg_time = now
                    last_text = info["text"]
        elif now - last_msg_time > NOT_FOUND_EVERY:
            msg = f"{target} not seen. Turn slowly left or right."
            if speaker.say(msg):
                last_msg_time = now
                last_text = msg

        cv2.putText(frame, last_text, (10, h - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 120, 0), 2)
        cv2.imshow("VisionAid - Find", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    speaker.stop()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()