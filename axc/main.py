import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import config as c
import subprocess

def posixcmd(cmd: str):
    try:
        output = subprocess.run(cmd, shell=True, text=True)
        print(f"{cmd}: {output}")
        return [output, 0]
    except subprocess.CalledProcessError as e:
        print(f"Error executing command {cmd}: {e}")
        return ["error", e.returncode]

def crashlog(e):
    #write crash report to common place
    crash_report = f"{time.now()}"
    return e[1]

def ecode(errc, cout):
    if cout[1] in errc: return 0

    print(f"Fatal error, crashlog generated in {c.ipath}crashlogs...")
    print(f"Fatal error, please send crashlog to code administrator...")
    sys.exit(crashlog(cout))



class gitsync(FileSystemEventHandler):
    def __init__(self, conf):
        self.conf = conf

    def on_modified(self, event):
        cmd = f"git checkout {self.conf.branch} -- {self.conf.rpath}"
        cout = posixcmd(cmd)
        ecode(c.codes, cout)
        time.sleep(1)
            
        cmd = f"git -C {self.conf.rpath} add ."
        cout = posixcmd(cmd)
        ecode(c.codes, cout)
        time.sleep(1)

        cmd = f"git -C {self.conf.rpath} commit -m \"Autosync\""
        cout = posixcmd(cmd)
        ecode(c.codes, cout)
        time.sleep(1)

        cmd = f"git -C {self.conf.rpath} push origin {self.conf.branch}"
        cout = posixcmd(cmd)
        ecode(c.codes, cout)
        time.sleep(1)
        stop

        


if __name__ == "__main__":

    cmd = f"GITHUB_ACCESS_TOKEN={c.gtoken}"
    cout = posixcmd(cmd)
    ecode(c.codes, cout)

    print(cout)


    stop



    confl = []

    for r in c.repo:
        confl.append(c.conf(r[0], r[1], r[3]))
        
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

                if e.returncode == 128:
                    print(f"New branch {r[1]} in {r[2]} local only, branch will be created remotely after next push...")

                print("Error executing command:", e)

        time.sleep(1)

    stop


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
