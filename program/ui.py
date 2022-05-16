from pathlib import Path
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import time
import classifier
from classifier import resource_path, show_video_preview
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
enable_images  = IntVar()
flip_video     = IntVar()
frame_skip     = IntVar()
fish_threshold = IntVar()
sampling_rate  = IntVar()

# keep references to the video(s) to process
videos_to_process = []

# open the video file and run classifier.py on it
def open_file(root):
    global videos_to_process
    home = "C:/"        # Default directory for file explorer
    video_file = Path(filedialog.askopenfilename(title="select", initialdir=home))
    videos_to_process = [video_file]
    print(videos_to_process)

    start_processing_button["state"] = "active"
    classifier.show_video_preview(image_frame, videos_to_process[0])

def open_dir(root):
    global videos_to_process
    # prompt user for directory and create list of files
    home = "C:/"
    video_dir  = Path(filedialog.askdirectory(title="select", initialdir=home))
    video_list = [os.path.join(video_dir, file) for file in os.listdir(video_dir)]
    videos_to_process = video_list
    print(videos_to_process)

    start_processing_button["state"] = "active"
    classifier.show_video_preview(image_frame, videos_to_process[0])

def process_input(root):
    # There may only be one video to process, or there may be multiple
    for video_file in videos_to_process:
        print(video_file)

        # place 'program running' widgets
        setup_screen()

        # start the video processing
        begin(image_frame, progress_bar, video_file)

        # reset
        reset_screen()


def setup_screen():

    # hide 'open' buttons while program running
    open_file_button.grid_forget()
    open_folder_button.grid_forget()
    start_processing_button.grid_forget()

    # place progress widgets
    info_label.grid(row=1)
    progress_bar.grid(row=2)
    back_button.grid(row=3)
    legend_label.grid(row=3, column=2)

def reset_screen():
    
    classifier.stop_prog = True

    # remove progress widgets
    info_label.grid_forget()
    progress_bar.grid_forget()
    back_button.grid_forget()
    legend_label.grid_forget()

    # replace default buttons
    open_file_button.grid(row=1)
    open_folder_button.grid(row=2)
    start_processing_button.grid(row=3)

def begin(frame, progress_bar, video_file):

    wipe_image()

    classifier.stop_prog = False
    classifier.main(image_frame, info_label, progress_bar, video_file, enable_images.get(), flip_video.get(), int(frame_skip.get()), int(fish_threshold.get()), int(sampling_rate.get()))

# hover tooltips (modified from: https://stackoverflow.com/a/56749167/11319058)
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
        tw.wm_overrideredirect(True)
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
options_frame.grid_propagate(False)

# options title
optlabel= Label(options_frame, text="Options", height=2, bg="white", font=("Helvetica", 11, "bold"))
optlabel.grid(row=0)

# check boxes
opt1 = Checkbutton(options_frame, text="Flip Video",    variable=flip_video,    onvalue=1, offvalue=0, anchor="w", height=1, bg="white")
opt1.grid(row=1, sticky="w")
AddToolTip([opt1], "Whether to flip the video vertically (shark should always be positioned at the bottom of the frame).")
opt2 = Checkbutton(options_frame, text="Output Images", variable=enable_images, onvalue=1, offvalue=0, anchor="w", height=1, bg="white")
opt2.grid(row=2, sticky="w")
AddToolTip([opt2], "Whether to output images for each frame to a seperate folder.")

# frame skip
e = Entry(options_frame, textvariable=frame_skip, width=2, bg="white")
e.delete(0); e.insert(0, "1"); e.grid(row=3, sticky="w")
el = Label(options_frame, text="Frame Skip", height=2, bg="white")
el.grid(row=3, padx=20, sticky="w")
AddToolTip([e, el], "The ratio of frames to skip.\nE.g. At a value of 6 only 1 in every 6 frames will be processed.")

# fish override threshold
f = Entry(options_frame, textvariable=fish_threshold, width=2, bg="white")
f.delete(0); f.insert(0, "20"); f.grid(row=4, sticky="w")
fl = Label(options_frame, text="Fish Sensitivity", height=2, bg="white")
fl.grid(row=4, padx=20, sticky="w")
AddToolTip([f, fl], "The minimum confidence required to override an object as a fish. Lower value = less false negatives, more false positives.\nE.g. At a value of 20 any object with a fish confidence of 20% or higher will be labeled fish regardless if fish is the dominant label.")

# sampling rate
sr = Entry(options_frame, textvariable=sampling_rate, width=2, bg="white")
sr.delete(0); sr.insert(0, "20"); sr.grid(row=5, sticky="w")
srl = Label(options_frame, text="Sampling Rate", height=2, bg="white")
srl.grid(row=5, padx=20, sticky="w")
AddToolTip([sr, srl], "The rate at which to sample, measured in Hz.\nE.g. At a value of 20, the output CSV will contain 20 entries per second.")

# empty frame for white border on right
Frame(root, width=600, height=20, padx=3, pady=3, bg="white").grid(row=0, column=1, columnspan=4, sticky="nw")
Frame(root, width=20, height=450, padx=3, pady=3, bg="white").grid(row=0, rowspan=5, column=5, sticky="nw")

##### IMAGE ##############################################################################

# configure frame
image_frame = Frame(root, width=600, height=350, padx=3, pady=3, bg="lightgray", relief=SUNKEN)
image_frame.grid(row=1, column=1, sticky="nw")
image_frame.pack_propagate(False)

# remove image from image frame
def wipe_image():
    for widget in image_frame.winfo_children():
        print(widget)
        widget.destroy()

##### PROGRAM ############################################################################

# configure frame
program_frame = Frame(root, width=600, height=100, padx=3, pady=3, bg="white")
program_frame.grid(row=4, rowspan=1, column=1, columnspan=4, sticky="nw")
program_frame.grid_propagate(False)
program_frame.columnconfigure(0, weight=1)

# configure grid
for i in range(0, 10):
    program_frame.rowconfigure(i, weight=1)

# open single video button
open_file_button = Button(program_frame, text="Open Single Video", width=20, command=lambda: open_file(root))
open_file_button.grid(row=1)

# open directory of videos button
open_folder_button = Button(program_frame, text="Open Folder", width=20, command=lambda: open_dir(root))
open_folder_button.grid(row=2)

# start the processing button
start_processing_button = Button(program_frame, text="✔️ Start Processing", width=40, state="disabled", command=lambda: process_input(root))
start_processing_button.grid(row=3)

# video info label, progress bar, and back button (not placed by default)
info_label   = Label(program_frame, text="VIDEO INFORMATION WILL BE HERE", height=2, bg="white")
progress_bar = ttk.Progressbar(program_frame, orient=HORIZONTAL, length=450)
back_button  = Button(program_frame, text = "❌ Quit Processing Video", width=20, command=reset_screen)

# labeled display legend
legend_label = Label(program_frame, text="❔", height=1, bg="white")
AddToolTip([legend_label], "The color of the box around an object reflects its assigned label:\n White = Unidentified Noise\n Gray = Shark Nose/Camera Edge\n Blue = Fish\n Green = Kelp\n Orange = Sunlight\n Brown = Rock")

# create the window
root.resizable(False, False) 
root.mainloop()
