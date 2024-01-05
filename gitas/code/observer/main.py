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
        cmd = f"git checkout {self.conf.branch} -- {self.conf.rpath}"
        output = subprocess.check_output(cmd, shell=True, text=True)
        try:
            output = subprocess.check_output(cmd, shell=True, text=True)
            print(f"git checkout {self.conf.branch} -- {self.conf.rpath}:", output)
        except subprocess.CalledProcessError as e:
            print("Error executing command:", e)
        
        stop

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
        
        cmd = f"git ls-remote --heads {r[2]}"
        output = subprocess.check_output(cmd, shell=True, text=True)
        if r[1] in output:
            print(f"Working branch found for {r[2]}...")
        else:
            print(f"Creating working branch for {r[2]}...")
            cmd = f"cd {r[0]} && git checkout -b {r[1]}"
            try:
                output = subprocess.check_output(cmd, shell=True, text=True)
                print(f"{r[2]} branch {r[1]} created...", output)
            except subprocess.CalledProcessError as e:
                print("Error executing command:", e)


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
