from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import json
import time

DOWNLOAD_PATH = "C:\Windows\System32\cmd.exe"
FOLDER_DESTINATION = "C:\\"

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(DOWNLOAD_PATH):
            src = DOWNLOAD_PATH + "/" + filename
            new_destination = FOLDER_DESTINATION + "/" + filename
            os.rename(src, new_destination)


def main():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOAD_PATH, FOLDER_DESTINATION)
    print("Press Q to QUIT")
    while True:
        print("Handling")
        time.sleep(10)
    
    observer.stop
    observer.join

if __name__ == "__main__":
    main()