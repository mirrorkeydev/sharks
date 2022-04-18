from pathlib import Path
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import time
import classifier
from classifier import resource_path
import re
import os

root = Tk()

# deafault window size
root.geometry("725x450")

# get current window size
#width  = root.winfo_screenwidth()
#height = root.winfo_screenheight()

# configure grid
for i in range(0, 4):
    root.rowconfigure(i, weight=1)
    root.columnconfigure(i, weight=1)
#root.grid_propagate(0)

# title and icon
root.title("Shark Classifer")
root.iconbitmap(resource_path('shark.ico'))

# used to check for valid file
is_file = False
stop_program = False

# define variables to pass to program and define as integers
enable_images = IntVar()
flip_video    = IntVar()
frame_skip    = IntVar()

# open the video file and run classifier.py on it
def open_file(root):

    stop_program = False    # Used to terminate processes if the user wants to "go back" while the program is running

    home = "C:/"        # Default directory for file explorer
    video_file = Path(filedialog.askopenfilename(title="select", initialdir=home))
    print(video_file)
    is_file = True
    if (is_file):

        # hide 'open' buttons while program running
        open_file_button.grid_forget()
        open_folder_button.grid_forget()

        # palce progress widgets
        progress_bar.grid(row=1)
        back_button.grid(row=2)

        # start the video processing
        begin(image_frame, progress_bar, video_file)

        # reset
        reset_screen()

def open_dir(root):

    stop_program = False    # Used to terminate processes if the user wants to "go back" while the program is running

    # prompt user for directory and create list of files
    home = "C:/"
    video_dir  = Path(filedialog.askdirectory(title="select", initialdir=home))
    video_list = [os.path.join(video_dir, file) for file in os.listdir(video_dir)]

    # run program for each file
    for video_file in video_list:
        print(video_file)

        is_file = True
        if (is_file):

            # hide 'open' buttons while program running
            open_file_button.grid_forget()
            open_folder_button.grid_forget()

            # palce progress widgets
            progress_bar.grid(row=1)
            back_button.grid(row=2)

            # start the video processing
            begin(image_frame, progress_bar, video_file)

        # reset
        reset_screen()


def open_settings():
    window = Toplevel(root)

def reset_screen():
    
    classifier.stop_prog = True

    # remove progress widgets
    back_button.grid_forget()
    progress_bar.grid_forget()

    # replace default buttons
    open_file_button.grid(row=1)
    open_folder_button.grid(row=2)

def begin(frame, progress_bar, video_file):
    classifier.stop_prog = False
    classifier.main(image_frame, progress_bar, video_file, enable_images.get(), flip_video.get(), frame_skip.get())

# Modified from: https://stackoverflow.com/a/56749167/11319058
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def AddToolTip(widgets, text):
    for widget in widgets:
        toolTip = ToolTip(widget)
        widget.bind('<Enter>', lambda event: toolTip.showtip(text))
        widget.bind('<Leave>', lambda event: toolTip.hidetip())

##### OPTIONS ############################################################################

# configure frame
options_frame = Frame(root, width=125, height=450, padx=3, pady=3, bg="white")
options_frame.grid(row=0, rowspan=5, column=0, sticky="nw")
options_frame.grid_propagate(0)

# options title
optlabel= Label(options_frame, text="Options", height=2, bg="white", font=("Helvetica", 11, "bold"))
optlabel.grid(row=0)

# check boxes
opt1 = Checkbutton(options_frame, text="Flip Video",    variable=flip_video,    onvalue=1, offvalue=0, anchor="w", height=1, bg="white")
opt1.grid(row=1, sticky="w")
AddToolTip([opt1], "Whether to flip the video vertically (to position the shark at the bottom).")
opt2 = Checkbutton(options_frame, text="Output Images", variable=enable_images, onvalue=1, offvalue=0, anchor="w", height=1, bg="white")
opt2.grid(row=2, sticky="w")
AddToolTip([opt2], "Whether to output images for each frame processed with objects circled.")

# number entry
e  =  Entry(options_frame, textvariable=frame_skip, width=2, bg="white")
e.delete(0); e.insert(0, "1"); e.grid(row=3, sticky="w")
el = Label(options_frame, text="Frame Skip", height=2, bg="white")
el.grid(row=3)
AddToolTip([e, el], "The ratio of frames to skip. E.g. 6 = Process 1 in every 6 frames.")

# empty frame for white border on right side
Frame(root, width=600, height=20, padx=3, pady=3, bg="white").grid(row=0, column=1, columnspan=4, sticky="nw")
Frame(root, width=20, height=450, padx=3, pady=3, bg="white").grid(row=0, rowspan=5, column=5, sticky="nw")

##### IMAGE ##############################################################################

# configure frame
image_frame = Frame(root, width=600, height=350, padx=3, pady=3, bg="lightgray", relief=SUNKEN)
image_frame.grid(row=1, column=1, sticky="nw")
image_frame.pack_propagate(0)

##### PROGRAM ############################################################################

# configure frame
program_frame = Frame(root, width=600, height=100, padx=3, pady=3, bg="white")
program_frame.grid(row=4, rowspan=1, column=1, columnspan=4, sticky="nw")
program_frame.grid_propagate(0)
program_frame.columnconfigure(0, weight=1)

# configure grid
for i in range(0, 4):
    program_frame.rowconfigure(i, weight=1)

# open single video button
open_file_button = Button(program_frame, text="Open Single Video", width=20, command=lambda: open_file(root))
open_file_button.grid(row=1)

# open directory of videos button
open_folder_button = Button(program_frame, text="Open Folder", width=20, command=lambda: open_dir(root))
open_folder_button.grid(row=2)

# progress bar and back button (not placed by default)
progress_bar = ttk.Progressbar(program_frame, orient=HORIZONTAL, length=450)
back_button  = Button(program_frame, text = "Quit Processing Video", width=20, command=reset_screen)

# quit program button
#quit_button = Button(program_frame, text="Quit Program", width=30, command=root.destroy)
#quit_button.grid(row=2)



# create the window
root.resizable(False, False) 
root.mainloop()
