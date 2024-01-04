import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import config as c
import subprocess


class gitsync(FileSystemEventHandler):
    def __init__(self, conf):
        self.conf = conf

    def on_modified(self, event):
        cmd = f"git -C {self.conf.rpath} add ."
        output = subprocess.check_output(cmd, shell=True, text=True)
        print(f"git add {self.conf.rpath}:", output)
        
        cmd = f"git -C {self.conf.rpath} commit -m \"Autosync\""
        output = subprocess.check_output(cmd, shell=True, text=True)
        print(f"git commit {self.conf.rpath}:", output)
        

        cmd = f"git -C {self.conf.rpath} push origin {self.conf.branch}"
        output = subprocess.check_output(cmd, shell=True, text=True)
        print(f"git push {self.conf.branch}:", output)
        stop


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
