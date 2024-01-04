import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import config as c


class gitsync(FileSystemEventHandler):
    def __init__(self, conf):
        self.conf = conf

    def on_modified(self, event):
        os.system(f"git -C {self.conf.rpath} add .")
        os.system(f"git -C {self.conf.rpath} commit -m \"Autosync\"")
        os.system(f"git -C {self.conf.rpath} push origin {self.conf.branch}")


if __name__ == "__main__":

    confl = []

    for r in c.repo:
        confl.append(c.conf(r[0], r[1]))

    for i in confl:
        event_handler = gitsync(i)
        observer = Observer()
        observer.schedule(event_handler, path=i.rpath, recursive=True)
        observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
