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

import os
from csv     import writer
from math    import floor
from pickle  import load
from imageio import *
from numpy                import copy, full, argmax, max
from skimage              import data, filters, util, color, morphology, measure, transform
from skimage.measure      import label, regionprops
from skimage.transform    import rescale
from skimage.segmentation import flood_fill
from skimage.util         import crop
from sklearn.ensemble     import RandomForestClassifier
from sklearn.neighbors    import _partition_nodes
from blob_extraction      import process_image, extract_blobs, get_blob_features
from matplotlib           import pyplot, patches, use

# i don't want matplotlib yelling at me for making too many figures
use("agg")

model_file  = "./trained_model.json"


# label titles & colors (used when outputing images)
label_titles = ["Noise (0)", "Shark Nose (1)", "Fish (2)", "Kelp (3)", "Seal (4)", "Other Shark (5)", "Sunspot (6)", "Rock (7)", "Bubble (8)", "Camera Edge (9)"]
label_colors = ["white", "lightgray", "blue", "green", "cyan", "teal", "orange", "saddlebrown", "lightcyan", "gray"]

# should be configurable
frame_step  = 6     # only looks at every nth frame

scale       = 0.5   # image scale multiplier
border_size = 25    # number of pixels
stop_prog = False   # did the user click the back button?

# https://stackoverflow.com/questions/57122622/how-to-include-json-in-executable-file-by-pyinstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main(root, progress_bar, video_file, enable_images, flip_video):

##### FILES & THINGS & WHATEVER ##########################################################

    # load the model
    try:
        rf = load(open(resource_path(model_file), "rb"))
    except:
        print("Error: Cannot find/load model, probably because the file", model_file, "does not exist. Try running build_classifier.py.")
        quit()

    # create/write to output file
    _, v = os.path.split(video_file)
    video_name, _ = v.rsplit('.', 1)
    output_file = f"{video_name}.csv"
    try:
        csv = open(output_file, 'w', newline="")
        csv_writer = writer(csv) 
        csv_writer.writerow(["Time", "Frame", "Kelp", "Fish", "Seal", "Shark", "", "Video Length (sec)", "FPS", "Width", "Height"])
        time = 0
    except:
        print("Error: Cannot open", output_file, ".")
        quit()

    # setup folder to hold frames
    dir_name = "Frames"
    if enable_images == 1 and not (os.path.exists(dir_name)):
        os.mkdir(dir_name)

    # video time
    print("Reading 1 in every", frame_step, "frames, predicting labels for all found objects, and exporting them as a gif.\nMight take a minute.\n")

    # read video
    video = get_reader(video_file, 'ffmpeg')
    num_frames = video.count_frames() # can take a few seconds on larger videos, but nice to know how long it will take
    metadata   = video.get_meta_data()
    fps        = metadata['fps']

    # Progress bar for loading the video files
    progress_bar['maximum'] = num_frames
    progress_bar['value'] = 0
    root.update_idletasks()

    # each every i frames
    for frame, image in enumerate(video):

        # wnd process if user went back to the main menu
        if(stop_prog):
            print("Process Terminated")
            return

        # update the progress bar
        progress_bar['value'] = frame
        root.update()

        # list to hold predictions for current frame
        predictions = [0 for i in range(10)]

        if frame % frame_step == 0:

            # create png title
            filename = f"Frames/{frame//frame_step}.png"

            if enable_images:
                # setup plots
                fig, ax = pyplot.subplots(1, 1, figsize=(5, 5))

##### IMAGE PROCESSING ###################################################################

            processed_images = process_image(image, bool(flip_video))

##### CLASSIFIER TIME ####################################################################

            # label objects in image
            blobs = extract_blobs(processed_images.final, processed_images.rescaled)
            not_fish_count, fish_count = 0, 0

            # get properties of each object
            for blob_num, props in enumerate(blobs):
                
                # end process if user went back to the main menu
                if(stop_prog):
                    print("Process Terminated")
                    return
                features, _ = get_blob_features(props, processed_images.grayscaled)
                feature_vector = [val for _, val in features.items()]

                # predict
                class_scores = rf.predict_proba([feature_vector])
                pred_class   = argmax(class_scores)
                pred_score   = max(class_scores)

                # overwrite if could be fish (temp measure)
                if (class_scores[0][2]) > 0.02:
                    pred_class = 2
                    pred_score = class_scores[0][2]

                # record scores
                predictions[pred_class] += 1

                # add box and title to figure
                if enable_images == 1:

                    # set color and title
                    color = label_colors[pred_class]
                    title = label_titles[pred_class]

                    # draw box
                    image_y_size, image_x_size, _ = image.shape
                    x, y = features["blob_x_coord"]*image_x_size, features["blob_y_coord"]*image_y_size
                    w, h = features["blob_width"]*image_x_size,   features["blob_height"]*image_y_size
                    box = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=color, facecolor="none")
                    ax.add_patch(box)

                    # add text
                    pyplot.text(x-1, y-8, title, color=color)
                    pyplot.text(x-1, y-44, str(int(pred_score*100))+"%", color=color)

            # build and write png
            if enable_images == 1:
                if bool(flip_video):
                    image = transform.rotate(image, 180)
                ax.set_title("Predicted")
                ax.imshow(image)
                ax.tick_params(left = False, bottom = False)
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)
                fig.tight_layout()
                pyplot.savefig(filename)  # create png
                pyplot.close("all")       # close the plot so matplotlib doesn't yell at me

##### OUTPUT RESULTS #####################################################################

            # create and write row to output
            row = [str(round(time, 1)), frame, predictions[3], predictions[2], predictions[4], predictions[5]]
            if (frame / frame_step == 0): row.extend(["", metadata['duration'], metadata['fps'], metadata['source_size'][0], metadata['source_size'][1]])
            csv_writer.writerow(row)

            # update timestamp
            time += (frame_step / floor(fps + 0.5))

    # Remove Progress bar upon completion
    progress_bar.forget()