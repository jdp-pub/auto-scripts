from tkinter import *

def tbox(master):
    box = Entry(master)
    box.pack()
    box.focus_set()
    return box

def genw():
    master = Tk()

    box1 = tbox(master)
    box2 = tbox(master)
    box3 = tbox(master)
    box4 = tbox(master)
    box5 = tbox(master)

    def callback():
        fpath = box1.get()
        uname = box2.get()
        upass = box3.get()
        repo = box4.get()
        branch = box5.get()

        print(f"{fpath}, {uname}, {upass}, {repo}, {branch}")

    b = Button(master, text = "OK", width = 10, command = callback)
    b.pack()

    mainloop()