from pathlib import Path
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import time
import classifier
from classifier import resource_path

# This is the root window that appears when the program is ran
root = Tk()
root.title("SharkGUI")
root.iconbitmap(resource_path('shark.ico')) #Change icon at top left corner use same root
root.geometry("750x350")

# Globals
is_file = False             # Boolean used to check for valid file

enable_images = IntVar()    # Tkinter integer variable
flip_video    = IntVar()

def open_file(root):
    global stop_program
    stop_program = False    # Used to terminate processes if the user wants to "go back" while the program is running

    home = "C:/"        # Default directory for file explorer
    video_file = Path(filedialog.askopenfilename(title = "select", initialdir = home))
    is_file = True
    if (is_file):
        # Hide open file button and label while the program processes a selected file
        open_file_btn.place_forget()
        open_folder_btn.place_forget()

        # Set up progress bar
        progress_label.place(relx=0.28, rely=0.5, anchor=CENTER)
        progress_bar.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Go Back Button (Stops Process)
        back_btn.place(relx=0, rely=0, anchor=NW)

        # Start the video processing
        begin(root, progress_bar, video_file)

        # completion message
        done_lbl = Label(root, text = f"Finished labeling frames, output is located in: output.csv")
        done_lbl.place(relx=0, rely=0, anchor=SW)

def open_settings():
    window = Toplevel(root)

def reset_screen():
    classifier.stop_prog = True
    back_btn.place_forget()
    progress_label.place_forget()
    progress_bar.place_forget()

    open_file_btn.place(relx=0.5, rely=0.4, anchor=CENTER)
    open_folder_btn.place(relx=0.5, rely=0.5, anchor=CENTER)
    quit_btn.place(relx=0.5, rely=0.6, anchor=CENTER)

def begin(root, progress_bar, video_file):
    classifier.main(root, progress_bar, video_file, enable_images.get(), flip_video.get())

# Initializers
back_btn = Button(root, text = "<--- Return to Menu", command = reset_screen)
progress_label = Label(root, text="Loading Video File...")
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=200)

# Open a single file
open_file_btn = Button(root, text = "Open Single File", command =lambda: open_file(root))
open_file_btn.place(relx=0.5, rely=0.4, anchor=CENTER)

# Open a folder of videos
open_folder_btn = Button(root, text = "Open Folder", command =lambda: open_file(root))
open_folder_btn.place(relx=0.5, rely=0.5, anchor=CENTER)

# Quit the program
quit_btn = Button(root, text = "Quit Program", command = root.destroy)
quit_btn.place(relx=0.5, rely=0.6, anchor=CENTER)

# Application settings
img = PhotoImage(file = resource_path('SettingsIcon2.png'))
setting_btn = Button(root, image = img, command = open_settings)
setting_btn.pack(side=TOP, anchor=NE)

# # Enable flip video setting
check_box = Checkbutton(root, text='Flip Video',variable=flip_video, onvalue=1, offvalue=0)
check_box.pack()

# # Enable image output setting
check_box = Checkbutton(root, text='Output Images',variable=enable_images, onvalue=1, offvalue=0)
check_box.pack()

# # Confidence Level setting
# slider = Scale(root, from_=0, to=100, orient=HORIZONTAL)
# slider.pack()

root.mainloop()
