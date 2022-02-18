from pathlib import Path
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import time
import classifier

# This is the root window that appears when the program is ran
root = Tk()
root.title("SharkGUI")
root.iconbitmap('shark.ico') #Change icon at top left corner use same root
root.geometry("750x350")

# Globals
boolean = False
enable_images = IntVar()    # Tkinter integer variable

def open_file(root):
    home = "C:/"        # Default directory for file explorer
    video_file = Path(filedialog.askopenfilename(title = "select", initialdir = home))
    boolean = True
    if (boolean == True):
        # Hide open file button and label while the program processes a selected file
        #btn_label.grid_forget()
        #open_file_btn.grid_forget()

        # Set up progress bar
        progress_label = Label(root, text="Loading Video File...")
        progress_label.grid(column = 3, row = 0)
        progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200)
        progress_bar.grid(column=4, row=0)

        # Start the video processing
        begin(root, progress_bar, video_file)

        # completion message
        test2 = Label(root, text = f"Finished labeling frames, output is located in: output.csv")
        test2.grid(column=0, row=2)

        btn_label.grid(column=0, row=0)
        open_file_btn.grid(column=1, row=0)


btn_label = Label(root, text="Click to Select Video File: ")
btn_label.grid(column=0, row=0)

open_file_btn = Button(root, text = "Open File", command =lambda: open_file(root))
open_file_btn.grid(column=1, row=0)

# Application settings label
settings_label = Label(root, text="Settings")
settings_label.grid(column = 0, row = 6)

# Enable image output setting
check_box = Checkbutton(root, text='Output Images',variable=enable_images, onvalue=1, offvalue=0)
check_box.grid(column = 0, row = 7)

# Confidence Level setting
slider = Scale(root, from_=0, to=100, orient=HORIZONTAL)
slider.grid(column = 0, row = 8)

def begin(root, progress_bar, video_file):
    classifier.main(root, progress_bar, video_file, slider)

root.mainloop()
