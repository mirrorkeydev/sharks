from pathlib import Path

# Change this depending on where your /Scored_video_and_data/ directory is located
dir_root = Path(r'D:/sharks-box/Box Sync')

# Certain groups of csvs/videos use different ID schemes to associate a csv with a video.
# These rexeg patterns will extract a comparable ID from both the csv and video names.
# Scheme A sample -> csv: video000025.xlsx, vid: 000000025.mov (note the difference in 0 padding)
# Scheme B sample -> csv: CC_7017-20129 JR.xlsx, vid: CC_7017-20129.mov
# Scheme C sample -> csv: ANI_CC0707_2019-209-27.xlsx, vid: ANI_CC0707_2019-209-27.mov (identical)
# Scheme D sample -> csv: CC_08_D1 809.xlsx, vid: FILE0809.mov
regex_a = { "csv": r'[Vv]ideo\s?0*(\d+)', "vid": r'\D*0+(\d+)' }
regex_b = { "csv": r'(\S+)\sJR', "vid": r'(\S+)' }
regex_c = { "csv": r'(\S+)', "vid": r'(\S+)' }
regex_d = { "csv": r".+ 0?(\d+)", "vid": r"FI(?:LE)?0(\d+)"}

deployments = [
  {
    "location": "SA 2014",
    "deployment": "CC_08_D3",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2014_INDEXED/CC_08_D3')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2014_INDEXED/CC_08_D3/CC 8_3 Deployment 20')),
    "regex_pattern": regex_d,
    "upsidedown": True,
  },
  # This one has over "50% kelp" but it's a lot of false positives.
  {
    "location": "SA 2014",
    "deployment": "CC_08_D2",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2014_INDEXED/CC_08_D2')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2014_INDEXED/CC_08_D2/Videos')),
    "regex_pattern": regex_d,
    "upsidedown": True,
  },
  {
    "location": "SA 2014",
    "deployment": "CC_08_D1",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2014_INDEXED/CC_08_D1')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2014_INDEXED/CC_08_D1/CC 8_1 deployment 01')),
    "regex_pattern": regex_d,
    "upsidedown": True,
  },
  {
    "location": "CA 2015",
    "deployment": "CC_2_24_D1",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/Classified CSV Files/CC_2_24_D1')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/White_Shark_CC_2_24_D1 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "CA 2015",
    "deployment": "CC_2_21_D2",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/Classified CSV Files/CC_2_21_D2')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/White_Shark_CC_2_21_D2 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "CA 2015",
    "deployment": "CC_2_21_D1",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/Classified CSV Files/CC_2_21_D1')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/White_Shark_CC_2_21_D1 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "CA 2015",
    "deployment": "CC_2_15_D2",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/Classified CSV Files/CC_2_15_D2')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/White_Shark_CC_2_15_D2 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "CA 2015",
    "deployment": "CC_2_15_D1",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/Classified CSV Files/CC_2_15_D1')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/White_Shark_CC_2_15_D1 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "CA 2015",
    "deployment": "CC_2_13_D1",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/Classified CSV Files/CC_2_13_D1')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2015_INDEXED/White_Shark_CC_2_13_D1 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": True,
  },
  {
    "location": "CA 2017",
    "deployment": "20171007 CC_07_07_D1",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/20171007 CC_07_07_D1')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/20171007 CC_07_07_D1 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "CA 2018",
    "deployment": "TOM_CC0705_20181101",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2018_INDEXED/CSV files/TOM_CC0705_20181101')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2018_INDEXED/TOM_CC_0705_20181111_Active')),
    "regex_pattern": regex_c,
    "upsidedown": True,
  },
  {
    "location": "CA 2018",
    "deployment": "FAR_CC0737_20181021",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2018_INDEXED/CSV files/FAR_CC0737_20181021')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2018_INDEXED/FAR_CC0737_20181021')),
    "regex_pattern": regex_c,
    "upsidedown": False,
  },
  {
    "location": "CA 2018",
    "deployment": "APT_CC0705_20180810",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2018_INDEXED/CSV files/APT_CC0705_20180810')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2018_INDEXED/APT_CC0705_20180810')),
    "regex_pattern": regex_c,
    "upsidedown": False,
  },
  {
    "location": "CA 2018",
    "deployment": "APT_CC0705_07182018",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2018_INDEXED/CSV files/APT_CC0705_07182018')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2018_INDEXED/APT_CC0705_07182018')),
    "regex_pattern": regex_c,
    "upsidedown": False,
  },
  {
    "location": "CA 2019",
    "deployment": "APT_CC0704_20190829",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2019_INDEXED/CSV Files/APT_CC0704_20190829')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2019_INDEXED/APT_CC0704_20190829')),
    "regex_pattern": regex_c,
    "upsidedown": False,
  },
  {
    "location": "CA 2019",
    "deployment": "ANO_CC0707_20191113",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2019_INDEXED/CSV Files/ANO_CC0707_20191113')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2019_INDEXED/ANO_CC0707_20191113')),
    "regex_pattern": regex_c,
    "upsidedown": False,
  },
  {
    "location": "CC 2015",
    "deployment": "CC_2_18",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CC 2015_INDEXED/CSV Files/CC_2_18')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CC 2015_INDEXED/CC_2_18 Converted Files')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "CC 2015",
    "deployment": "CC_2_19",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CC 2015_INDEXED/CSV Files/CC_2_19')),
    # Not all videos have been processed, so less frames will be grabbed than calculated.
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CC 2015_INDEXED/CC_2_19 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "SA 2017",
    "deployment": "CC_7_06",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2017_INDEXED/CSV Files/CC_7_06')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/SA 2017_INDEXED/CC_7_06 Converted Videos')),
    "regex_pattern": regex_a,
    "upsidedown": True,
  },
  {
    "location": "CA 2017",
    "deployment": "CC_07_07_D1",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/20171007 CC_07_07_D1')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/20171007 CC_07_07_D1 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
  {
    "location": "CA 2017",
    "deployment": "TOM_CC0704_20171102",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/TOM_CC0704_20171102')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/TOM_CC0704_20171102')),
    # This one has a unique video file name pattern that warranted its own regex.
    "regex_pattern":  { **regex_a, "vid": r'.+-(\d+)' },
    "upsidedown": False,
  },
  {
    "location": "CA 2017",
    "deployment": "TOM_CC0704_20171105",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/TOM_CC0704_20171105')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/TOM_CC0704_20171105')),
    "regex_pattern": regex_b,
    "upsidedown": False,
  },
  {
    "location": "CA 2017",
    "deployment": "TOM_CC0705_20171015",
    "csv_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/CSV Files/TOM_CC0705_20171015')),
    "vid_dir": dir_root.joinpath(Path(r'Scored_video_and_data/CA 2017_INDEXED/TOM_CC0705_20171015 Converted')),
    "regex_pattern": regex_a,
    "upsidedown": False,
  },
]
