from pathlib import Path
from tkinter import * #Import the tkinter library
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import time
import extract_video_frames
#import deployments_data

# This is the root window that appears when the program is ran
root = Tk()
root.title("SharkGUI")
root.iconbitmap('shark.ico') #Change icon at top left corner use same root
root.geometry("750x350")

# Globals
#file=""
boolean = False

def open_file(root):
    home = "C:/"
    global dir_root
    dir_root = Path(filedialog.askdirectory( title = "select", initialdir = home))
    test = Label(root, text = f"Retrieved files from {dir_root}")
    test.grid(column=0, row=1)
    boolean = True
    if (boolean == True):
        progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200)
        progress_bar.grid(column=2, row=1)
        begin(root, progress_bar)

# canvas = Text(root, height = 100, width = 100)
# message = "This is working totally fine."
# canvas.grid(column=2, row=1)
# canvas.insert(END, message)

btn_label = Label(root, text="Click to Select Directory: ")
btn_label.grid(column=0, row=0)

open_file_btn = Button(root, text = "Open File", command =lambda: open_file(root))
open_file_btn.grid(column=1, row=0)

def begin(root, progress_bar):
    extract_video_frames.source(root, dir_root, progress_bar)

root.mainloop()