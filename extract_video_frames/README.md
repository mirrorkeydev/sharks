# Extract Video Frames
This script runs through all known cvs/video pairs and extracts frames where any event occurs, outputting them into /extractedframes/{event_name} directories in your current working directory.

# Setup
Change `dir_root` in `deployments_data.py` to point at the correct root on the machine you're running the script on.

# Run
```bash
python extract_video_frames.py
```
