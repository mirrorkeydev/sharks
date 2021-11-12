# This script runs through all known cvs/video pairs and extracts frames
# where any event occurs, outputting them into /extractedframes/{event_name} directories
# in your current working directory.

import openpyxl
import ffmpeg
import re
from pathlib import Path
from collections import defaultdict
from deployments_data import deployments

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
    .run()
  )

def main():
  for deployment in deployments:
    print("Processing videos from {location}, deployment {deployment}".format(**deployment))
    vids_to_check = defaultdict(list)

    # Mark videos to extract frames from
    num_frames_found = 0
    for csv_file in deployment["csv_dir"].iterdir():
      match = re.match(deployment["regex_pattern"]["csv"], csv_file.stem)
      if match == None:
        print(f"Warning: Unable to extract ID from csv '{csv_file.name}'. File name did not match the expected format. Skipping.")
        continue
      vid_num = match[1]

      wb_obj = openpyxl.load_workbook(str(csv_file)) 
      sheet = wb_obj.active

      for row in sheet.iter_rows(min_row=2, values_only=True):
        time, event = row[0], row[3]
        if not isinstance(time, float) or not isinstance(event, str):
          continue
        if event != None:
          vids_to_check[vid_num].append((time, event))
          num_frames_found += 1

    print(f"Found {num_frames_found} frames to select from videos")

    # Extract frames
    num_frames_created = 0
    vid_nums_processed = set()
    for vid_file in deployment["vid_dir"].iterdir():
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
          frames_dir_name = f"extractedframes2/{event}"
          newdir = Path.cwd().joinpath(frames_dir_name)
          newdir.mkdir(parents=True, exist_ok=True)
          
          num_frames_to_extract = 10
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

    # This may be less than the number of frames selected, because the video
    # that it tries to get frames from may not exist.
    # TODO: I would expect it to throw an error when the video doesn't exist,
    # but it's not currently doing so. Need to investigate why that is.
    print(f"Exported {num_frames_created} frames") 

  print("\n - Completed successfully -")

if __name__ == "__main__":
  main()
