import queue
import threading
import time

import pyttsx3


class Speaker:
    """Speaks text in a background thread so the video loop never freezes."""

    def __init__(self, rate=170):
        self.q = queue.Queue(maxsize=3)
        self.rate = rate
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        engine = pyttsx3.init()  # must be created inside this thread
        engine.setProperty("rate", self.rate)
        while True:
            text = self.q.get()
            if text is None:
                break
            engine.say(text)
            engine.runAndWait()

    def say(self, text, urgent=False):
        """Returns True if the message was queued, False if it was dropped."""
        if urgent:
            # Throw away waiting messages so the warning is spoken next
            try:
                while True:
                    self.q.get_nowait()
            except queue.Empty:
                pass
        try:
            self.q.put_nowait(text)
            return True
        except queue.Full:
            return False

    def stop(self):
        self.q.put(None)


if __name__ == "__main__":
    s = Speaker()
    s.say("VisionAid speech test")
    time.sleep(3)