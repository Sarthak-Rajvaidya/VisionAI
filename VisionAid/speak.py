import queue
import threading
import time

import pyttsx3


class Speaker:
    """Speaks text in a background thread so the video loop never freezes."""

    def __init__(self, rate=170):
        self.q = queue.Queue(maxsize=3)  # small queue: old messages get dropped, not piled up
        self.rate = rate
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        # The engine must be created inside the thread that uses it
        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate)
        while True:
            text = self.q.get()
            if text is None:
                break
            engine.say(text)
            engine.runAndWait()

    def say(self, text):
        try:
            self.q.put_nowait(text)
        except queue.Full:
            pass  # speaker is busy, skip this message

    def stop(self):
        self.q.put(None)


if __name__ == "__main__":
    s = Speaker()
    s.say("VisionAid speech test")
    time.sleep(3)