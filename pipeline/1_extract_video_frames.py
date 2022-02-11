# This script runs through all known cvs/video pairs and extracts frames where any event
# occurs, outputting them into /{extracted_frames_directory_name}/{event_name} directories
# in your current working directory.
#
# Before you run this script:
# 1. Change `dir_root` in `deployments_data.py` to point at the correct root
#    on the machine you're running the script on.

import openpyxl
import ffmpeg
import re
from pathlib import Path
from collections import defaultdict
import random
from deployments_data import deployments

extracted_frames_directory_name = "rawframes" # This directory will be auto-created.

def extract_frame(vid_path: Path, time: float, out_path: Path, num_frames: int, needs_flipped: bool) -> None:
  '''
  Extracts a frame from the input vid_path at time `time` and outputs the file
  at the specified output path. Note that ffmpeg cannot create new directories,
  only files, so the entire path (sans file) must already exist.
  '''
  if not isinstance(time, float):
    print(f"extract_frame expected time to be a float, but got {type(time)}.")
    return

  stream = ffmpeg.input(str(vid_path), ss=time)
  if needs_flipped:
    stream = ffmpeg.vflip(stream)
  stream = ffmpeg.output(stream, str(out_path), vframes=num_frames)
  stream = stream.global_args('-loglevel', 'error')
  stream = stream.global_args('-n') # Never overwrite file if it already exists
  ffmpeg.run(stream)

def main():
  skippers = {"kelp": 0, "rock": 0}
  total_distribution = {}
  total_sum = 0
  for deployment in deployments:
    print("\n-----------------------------------------------------------")
    print("Processing videos from {location}, deployment {deployment}".format(**deployment))
    vids_to_check = defaultdict(list)

    skipped_files = []

    # Mark videos to extract frames from
    num_frames_found = 0
    for csv_file in deployment["csv_dir"].iterdir():
      if str(csv_file.suffix).lower() != ".xlsx":
        skipped_files.append(csv_file.name)
        continue
      match = re.match(deployment["regex_pattern"]["csv"], csv_file.stem)
      if match == None:
        print(f"Warning: Unable to extract ID from csv '{csv_file.name}'. File name did not match the expected format. Skipping.")
        continue
      vid_num = match[1]

      wb_obj = openpyxl.load_workbook(str(csv_file)) 
      sheet = wb_obj.active

      for row in sheet.iter_rows(min_row=2, values_only=True):
        time, event, pov = row[0], row[3], row[4]
        if not isinstance(time, float):
          continue
        
        include = False
        event_name = "NoEvent"
        things_of_interest = ["kelp", "fish", "seal", "rock", "shark (g)"]

        if event is None and pov is None:
          # Ususally we skip these frames where nothing is happening, but 
          # we do want some samples of conditions where nothing is seen.
          include = random.randint(0, 5000) == 1 # 1 in 5,000 chance
    
        if pov is not None:
          include = any([word in pov.lower() for word in things_of_interest])
          event_name = pov

        if event is not None:
          include = any([word in event.lower() for word in things_of_interest])
          event_name = event

        if "rock" in event_name.lower():
          event_name = "Reef or Rock" # the original name has a slash which is bad for filenames

        if include:
          vids_to_check[vid_num].append((time, event_name))
          num_frames_found += 1

    print(f"Found {num_frames_found} events to select from videos")
    if len(skipped_files) > 0:
      print(f"Skipped non-excel files: {skipped_files}.")

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
        print(f"Warning: Name of video file '{vid_file.name}' did not match the expected format. Skipping.")
        continue
      vid_num = match[1]

      # There are some duplicates like 0000022.mov and 0000022 (2).mov, so we just
      # mark that we've already seen this video number and ignore future duplicates
      if vid_num not in vid_nums_processed:
        vid_nums_processed.add(vid_num)

        for time, event in vids_to_check[vid_num]:
          frames_dir_name = f"{extracted_frames_directory_name}"
          newdir = Path.cwd().joinpath(frames_dir_name)
          newdir.mkdir(parents=True, exist_ok=True)
          
          num_frames_to_extract = 1

          if "kelp" in event.lower():
            # There's so many of these that we don't want to extract every single one.
            # This logic only extracts every 1 of 20 kelp occurences.
            if skippers["kelp"] < 20:
              skippers["kelp"] += 1
              continue
            else:
              skippers["kelp"] = 0

          if "rock" in event.lower():
            if skippers["rock"] < 40:
              skippers["rock"] += 1
              continue
            else:
              skippers["rock"] = 0

          if any([word in event.lower() for word in ["fish"]]):
            # For these specific events, we want to extract more frames than usual.
            num_frames_to_extract = 1

          if any([word in event.lower() for word in ["seal", "shark"]]):
            # For these specific events, we want to extract more frames than usual.
            num_frames_to_extract = 5

          if event in total_distribution:
            total_distribution[event] += num_frames_to_extract
          else:
            total_distribution[event] = num_frames_to_extract

          spf = (1/30) # seconds per frame
          adjusted_time = time - spf*num_frames_to_extract/2

          try:
            extract_frame(vid_file,
            adjusted_time,
            newdir.joinpath(f"{deployment['location']}-{deployment['deployment']}-{vid_num}-{event}-{'%.3f'%(adjusted_time)}-%03d.png"),
            num_frames_to_extract,
            deployment['upsidedown'])
            num_frames_created += num_frames_to_extract
          except Exception as e:
            print(e)

    if len(skipped_video_files) > 0:
      print(f"Skipped non-video files: {skipped_video_files}.")
    print(f"Exported {num_frames_created} frames") 
    total_sum += num_frames_created

  print("sum = ", total_sum)
  print(total_distribution)
  print("\n - Completed successfully -")

if __name__ == "__main__":
  main()
