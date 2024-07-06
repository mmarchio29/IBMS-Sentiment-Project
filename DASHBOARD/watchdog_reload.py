### Instructions:
### 1. **Install `watchdog`**: Run `pip install watchdog`.
### 2. **Create `watchdog_reload.py`**: Create a file `watchdog_reload.py` with the following content:

import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen, PIPE

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.restart()

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            self.restart()

    def restart(self):
        if self.process:
            self.process.kill()
            self.process.wait()
        self.process = Popen([sys.executable, self.script], stdout=PIPE, stderr=PIPE)

if __name__ == "__main__":
    script = "appdk.py"  # Your Dash app script
    event_handler = ChangeHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()