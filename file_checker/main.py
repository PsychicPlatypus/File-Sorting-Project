from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

import os
import time

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(DOWNLOAD_PATH):
            src = Path(DOWNLOAD_PATH + "/" + filename)
            print(src)
            new_destination = Path(FOLDER_DESTINATION + "/" + filename)
            print(new_destination)
            os.rename(src, new_destination)


DOWNLOAD_PATH = Path("/DummyOne")
FOLDER_DESTINATION = Path("/Dummy")


def main():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOAD_PATH, FOLDER_DESTINATION)
    print("Press CTRL - C to QUIT")
    try:
        while True:
            print("Handling")
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop
        observer.join

if __name__ == "__main__":
    main()