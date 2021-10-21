from pathlib import Path

# Change this depending on where your /Scored_video_and_data/ directory is located
dir_root = Path(r'D:/sharks-box/Box Sync')

# Certain groups of csvs/videos use different ID schemes to associate a csv with a video.
# These rexeg patterns will extract a comparable ID from both the csv and video names.
# Scheme A sample -> csv: video000025.xlsx, vid: 000000025.mov (note the difference in 0 padding)
# Scheme B sample -> csv: CC_7017-20129 JR.xlsx, vid: CC_7017-20129.mov
regex_a = { "csv": r'[Vv]ideo\s?0*(\d+)', "vid": r'\D*0+(\d+)' }
regex_b = { "csv": r'(\S+)\sJR', "vid": r'(\S+)' }

deployments = [
  {
    "location": "CC 2015",
    "deployment": "CC_2_18",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CC 2015_INDEXED/CSV Files/CC_2_18')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CC 2015_INDEXED/CC_2_18 Converted Files')),
    "regex_pattern": regex_a,
  },
  {
    "location": "CC 2015",
    "deployment": "CC_2_19",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CC 2015_INDEXED/CSV Files/CC_2_19')),
    # Not all videos have been processed, so less frames will be grabbed than calculated.
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CC 2015_INDEXED/CC_2_19 Converted')),
    "regex_pattern": regex_a,
  },
  {
    "location": "SA 2017",
    "deployment": "CC_7_06",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2017_INDEXED/CSV Files/CC_7_06')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2017_INDEXED/CC_7_06 Converted Videos')),
    "regex_pattern": regex_a,
  },
  {
    "location": "CA 2017",
    "deployment": "CC_07_07_D1",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/20171007 CC_07_07_D1')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/20171007 CC_07_07_D1 Converted')),
    "regex_pattern": regex_a,
  },
  {
    "location": "CA 2017",
    "deployment": "TOM_CC0704_20171102",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/TOM_CC0704_20171102')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/TOM_CC0704_20171102')),
    # This one has a unique video file name pattern that warranted its own regex.
    # TODO: maybe talk to Dr. Chapple about standardizing these formats so I don't have to
    # write all these regexes. We could script the change so it wouldn't take too long.
    "regex_pattern":  { **regex_a, "vid": r'.+-(\d+)' },
  },
  {
    "location": "CA 2017",
    "deployment": "TOM_CC0704_20171105",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/TOM_CC0704_20171105')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/TOM_CC0704_20171105')),
    "regex_pattern": regex_b,
  },
  {
    "location": "CA 2017",
    "deployment": "TOM_CC0705_20171015",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/TOM_CC0705_20171015')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/TOM_CC0705_20171015 Converted')),
    "regex_pattern": regex_a,
  },
]
