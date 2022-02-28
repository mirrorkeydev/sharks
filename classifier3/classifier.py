# =============================================== #
#
# classify all objects in video, export labels
# input:  video, pretrained serialized model
# output: frame labels as csv
# 
# pyinstaller -F --noconsole classifier.py
#
# need to do:
# model + icon image should be bundled
#
# =============================================== #

# This workaround allows us to import from pipeline/ without
# having to install it as a package or restructure the project.
import sys
from pathlib import Path
SELF_PATH = Path(__file__)
sys.path.append(str(SELF_PATH.parent.parent))

from csv     import writer
from math    import floor
from pickle  import load
from imageio import *
from numpy                import copy, full
from skimage              import data, filters, util, color, morphology, measure, transform
from skimage.measure      import label, regionprops
from skimage.transform    import rescale
from skimage.segmentation import flood_fill
from skimage.util         import crop
from sklearn.ensemble     import RandomForestClassifier
from sklearn.neighbors    import _partition_nodes
from pipeline.blob_extraction import process_image, extract_blobs, get_blob_features

# parameters
model_file  = "./trained_model.json"
output_file = "output.csv"

upsidedown  = True  # does the footage need to be flipped 180 degrees?
frame_step  = 6     # only looks at every nth frame
scale       = 0.5   # image scale multiplier
border_size = 25    # number of pixels
stop_prog = False   # did the user click the back button?

def main(root, progress_bar, video_file, slider):

##### FILES & THINGS & WHATEVER ##########################################################

    # load the model (this sucks, model needs to be bundled with .exe)
    try:
        rf = load(open(model_file, "rb"))
    except:
        print("Error: Cannot find/load model, probably because the file", model_file, "does not exist. Try running build_classifier.py.")
        quit()

    # load the output file
    try:
        csv = open(output_file, 'w', newline="")
        csv_writer = writer(csv) 
        csv_writer.writerow(["Time", "Frame", "Number of not-fish", "Number of fish"])
        time = 0
    except:
        print("Error: Cannot open", output_file, ".")
        quit()

    # video time
    print("Reading 1 in every", frame_step, "frames, predicting labels for all found objects, and exporting them as a gif.\nMight take a minute.\n")

    # read video
    video = get_reader(video_file, 'ffmpeg')
    num_frames = video.count_frames() # can take a few seconds on larger videos, but nice to know how long it will take
    fps        = video.get_meta_data()['fps']
    
    # Progress bar for loading the video files
    progress_bar['maximum'] = num_frames
    progress_bar['value'] = 0
    root.update_idletasks()

    # each every i frames
    for frame, image in enumerate(video):
        # End process if user went back to the main menu
        if(stop_prog):
            print("Process Terminated")
            return
        # Update the progress bar
        progress_bar['value'] = frame
        root.update()

        if frame % frame_step == 0:

##### IMAGE PROCESSING ###################################################################

            processed_images = process_image(image, upsidedown)

##### CLASSIFIER TIME ####################################################################

            # label objects in image
            blobs = extract_blobs(processed_images.final, processed_images.rescaled)
            not_fish_count, fish_count = 0, 0

            # get properties of each object
            for blob_num, props in enumerate(blobs):
                # End process if user went back to the main menu
                if(stop_prog):
                    print("Process Terminated")
                    return
                features, _ = get_blob_features(props, processed_images.grayscaled)
                feature_vector = [val for _, val in features.items()]

                # test model with features
                confidence = int(rf.predict_proba([feature_vector])[0][1] * slider.get())
                if rf.predict([feature_vector])[0] == 1:
                    fish_count += 1
                else:
                    not_fish_count += 1

##### OUTPUT RESULTS #####################################################################

            # create and write row to output
            row = [str(round(time, 1)), str(frame), str(not_fish_count), str(fish_count)]
            csv_writer.writerow(row)

            # update timestamp
            time += (frame_step / floor(fps + 0.5))
    
    # Remove Progress bar upon completion
    progress_bar.forget()
