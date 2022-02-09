# This script runs through all known cvs/video pairs and extracts frames
# where any event occurs, outputting them into /extractedframes/{event_name} directories
# in your current working directory.

import openpyxl
import ffmpeg
import re
from pathlib import Path
from collections import defaultdict

from pytest import skip
import deployments_data

# GUI Imports
import os
from tkinter import * # Import the tkinter library
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
import time


def extract_frame(vid_path: Path, time: float, out_path: Path) -> None:
  '''
  Extracts a frame from the input vid_path at time `time` and outputs the file
  at the specified output path. Note that ffmpeg cannot create new directories,
  only files, so the entire path (sans file) must already exist.
  '''
  if not isinstance(time, float):
    print(f"extract_frame expected time to be a float, but got {type(time)}.")
    return
  (
    ffmpeg
    .input(str(vid_path), ss=time)
    .output(str(out_path), vframes=1)
    .global_args('-loglevel', 'error')
    .global_args('-n') # Never overwrite file if it already exists
    .run()
  )

def source(root, dir_root, progress_bar):
  curr_file = 0
  deployments = deployments_data.run_deployments(dir_root)
  #deployments_data.run_deployments(file)
  for deployment in deployments:
    
    #------------ GUI ------------------
    # Create textbox to display messages to the screen
    canvas = Text(root, height = 20, width = 50)
    message = "Processing videos from {location}, deployment {deployment}".format(**deployment)
    canvas.grid(column=2, row=2)
    canvas.insert(END, message)
    #print("\n-----------------------------------------------------------")
    #print("Processing videos from {location}, deployment {deployment}".format(**deployment))
    #--------------------------------------------

    vids_to_check = defaultdict(list)

    skipped_files = []

    # Mark videos to extract frames from
    num_frames_found = 0
    num_files = 0
    for csv_file in deployment["csv_dir"].iterdir():
      num_files += 1

    progress_bar['maximum'] = num_files
    progress_bar['value'] = 0
    root.update_idletasks()

    for csv_file in deployment["csv_dir"].iterdir():
      if str(csv_file.suffix).lower() != ".xlsx":
        skipped_files.append(csv_file.name)
        continue
      match = re.match(deployment["regex_pattern"]["csv"], csv_file.stem)
      if match == None:
        message2 = f"Warning: Unable to extract ID from csv '{csv_file.name}'. File name did not match the expected format. Skipping."
        canvas.insert(END, message2)
        continue
      vid_num = match[1]

      wb_obj = openpyxl.load_workbook(str(csv_file)) 
      sheet = wb_obj.active

      for row in sheet.iter_rows(min_row=2, values_only=True):
        time, event, pov = row[0], row[3], row[4]
        if not isinstance(time, float) or (not isinstance(event, str) and not isinstance(pov, str)):
          #print(f"I'm a debug message for row: {row}")
          continue
        if (event is not None and "kelp" in event.lower()) or (pov is not None and "kelp" in pov.lower()):
          vids_to_check[vid_num].append((time, event if event is not None and "kelp" in event.lower() else pov))
          num_frames_found += 1
      curr_file += 1
      progress_bar['value'] = curr_file
      root.update_idletasks()
      
    message3 = f"Found {num_frames_found} frames to select from videos"
    canvas.insert(END, message3)
    if len(skipped_files) > 0:
      message4 = f"Skipped non-excel files: {skipped_files}."
      canvas.insert(END, message4)

    # Extract frames
    num_frames_created = 0
    vid_nums_processed = set()
    skipped_video_files = []

    for vid_file in deployment["vid_dir"].iterdir():
      
      if str(vid_file.suffix).lower() != ".mov":
        skipped_video_files.append(vid_file.name)
        continue
      match = re.match(deployment["regex_pattern"]["vid"], vid_file.stem)
      if match == None:
        message5 = f"Warning: Name of video file '{vid_file.name}' did not match the expected format. Skipping."
        canvas.insert(END, message5)
        continue
      vid_num = match[1]

      # There are some duplicates like 0000022.mov and 0000022 (2).mov, so we just
      # mark that we've already seen this video number and ignore future duplicates
      if vid_num not in vid_nums_processed:
        vid_nums_processed.add(vid_num)

        for time, event in vids_to_check[vid_num]:
          frames_dir_name = f"extractedframeskelp/{event}"
          newdir = Path.cwd().joinpath(frames_dir_name)
          newdir.mkdir(parents=True, exist_ok=True)
          
          num_frames_to_extract = 5
          spf = (1/30)
          adjusted_time = time - spf*num_frames_to_extract/2

          for _ in range(num_frames_to_extract):
            print(adjusted_time)
            try:
              extract_frame(vid_file, adjusted_time, newdir.joinpath(f"{deployment['location']}-{deployment['deployment']}-{vid_num}-{'%.3f'%(adjusted_time)}.png"))
              num_frames_created += 1
            except Exception as e:
              print(e)
            adjusted_time += spf

    if len(skipped_video_files) > 0:
      message6 = f"Skipped non-video files: {skipped_video_files}."
      canvas.insert(END, message6)
    # This may be less than the number of frames selected, because the video
    # that it tries to get frames from may not exist.
    # TODO: I would expect it to throw an error when the video doesn't exist,
    # but it's not currently doing so. Need to investigate why that is.
    message7 = f"Exported {num_frames_created} frames"
    canvas.insert(END, message7)


  message8 = "\n - Completed successfully -"
  canvas.insert(END, message8)

