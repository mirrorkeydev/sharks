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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# i don't want matplotlib yelling at me for making too many figures
use("agg")

model_file  = "./trained_model.json"

# label titles & colors (used when outputing images)
label_titles = ["Noise (0)", "Shark Nose (1)", "Fish (2)", "Kelp (3)", "Seal (4)", "Other Shark (5)", "Sunspot (6)", "Rock (7)", "Bubble (8)", "Camera Edge (9)"]
label_colors = ["white", "lightgray", "blue", "green", "cyan", "teal", "orange", "saddlebrown", "lightcyan", "gray"]

scale       = 0.5   # image scale multiplier
border_size = 25    # number of pixels

stop_prog   = False # did the user click the back button?
image_freq  = 40    # how often frames are sent back to ui (one frame is sent every [frame skip * image freq] frames)

# find right path to data
# modified from: https://stackoverflow.com/questions/57122622/how-to-include-json-in-executable-file-by-pyinstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# displays a one-frame preview of the video selected, so that the 
# user can adjust the program options as necessary (e.g. flip video)
def show_video_preview(tk_frame, video_file):
    try:
        video = get_reader(video_file, 'ffmpeg')
    except Exception as e:
        print("Error with", video_file, ":", e)
        return

    first_frame = next(iter(video))

    fps = video.get_meta_data()['fps']

    # delete previous image from canvas
    for w in tk_frame.winfo_children():
        w.destroy()

    # place new image on canvas
    fig, ax = pyplot.subplots(1, 1, figsize=(5, 5))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.tick_params(left = False, bottom = False)
    ax.title.set_text(f"Preview of file(s) selected. {fps} fps.")

    ax.imshow(first_frame)

    canvas = FigureCanvasTkAgg(fig, master=tk_frame)
    canvas.get_tk_widget().pack(fill="both")

# main loop
def main(tk_frame, info_label, progress_bar, video_file, enable_images, flip_video, frame_step, fish_threshold, sampling_rate):

    # clear the image displayed on image_frame
    def clear_frame():
        for w in tk_frame.winfo_children():
            w.destroy()

##### FILES & THINGS & WHATEVER ##########################################################

    # load model
    try:
        rf = load(open(resource_path(model_file), "rb"))
    except:
        print("Error: Cannot find/load model, probably because the file", model_file, "does not exist. Try running build_classifier.py.")
        quit()

    # load video
    try:
        video = get_reader(video_file, 'ffmpeg')
    except:
        print("Error:", video_file, "is not a readable video file.")
        return

    # video time
    print("Reading 1 in every", frame_step, "frames, predicting labels for all found objects, and exporting them as a gif.\nMight take a minute.\n")

    # create/write to output file
    _, v = os.path.split(video_file)
    video_name, _ = v.rsplit('.', 1)
    output_file = f"{video_name}.csv"
    try:
        csv = open(output_file, 'w', newline="")
        csv_writer = writer(csv) 
        csv_writer.writerow(["Time", "Frame", "Kelp", "Kelp_Binary", "Fish", "Fish_Binary", "Rocks_Binary", "", "Video Length (sec)", "FPS", "Width", "Height"])
    except:
        print("Error: Cannot open", output_file, ".")
        quit()

    # setup folder to hold frames
    dir_name = f"{video_name}_labeled_frames"
    if enable_images == 1 and not (os.path.exists(dir_name)):
        os.mkdir(dir_name)

    # capture metadata
    num_frames = video.count_frames()    # can take a few seconds on larger videos
    metadata   = video.get_meta_data()
    fps        = metadata['fps']

    # progress bar for loading the video files
    progress_bar['maximum'] = num_frames
    progress_bar['value'] = 0

##### READ VIDEO #########################################################################

    sampling_step_rate = 1/sampling_rate
    video_step_rate = 1/fps
    effective_video_step_rate = video_step_rate * frame_step
    csv_time = 0
    video_time = 0

    while(True):
        # We work in CSV blocks, and figure out which CSV timestamps correspond to
        # the next "available" video frame. Here, "barrier" refers to the end of the 
        # CSV block.
        times_in_this_block = []
        next_barrier = csv_time + effective_video_step_rate
        while csv_time < next_barrier:
            times_in_this_block.append(csv_time)
            csv_time += sampling_step_rate

        # All times within the CSV block (calculated above) will receive the same frame
        # calculation values. This ensures we're not doing the classification step redundantly.

        frame = int(video_time * fps)
        try:
            image = video.get_data(frame)
        except:
            # This probably happened cause we went out of bounds on the video,
            # which means we're done.
            break

        # should this frame be sent to ui? 
        send_image = frame % (frame_step * image_freq) == 0

        # end process if user went back to the main menu
        if(stop_prog):
            print("Process Terminated")
            return

        # update the progress bar and info label
        info_label['text']    = f"Processing {output_file}, frame {frame} of {num_frames} [{(frame/num_frames*100):>2.1f}%]..."
        progress_bar['value'] = frame
        tk_frame.update()
    
        # list to hold predictions for current frame
        predictions = [0 for i in range(10)]

        # create png title
        if enable_images: filename = f"{dir_name}/{frame//frame_step}.png"

        # setup figure
        if enable_images or send_image:
            fig, ax = pyplot.subplots(1, 1, figsize=(5, 5))
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            ax.tick_params(left = False, bottom = False)

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

            # make prediction
            class_scores = rf.predict_proba([feature_vector])
            pred_class   = argmax(class_scores)
            pred_score   = max(class_scores)

            # fish override
            if (class_scores[0][2]) > fish_threshold/100:
                pred_class = 2
                pred_score = class_scores[0][2]

            # record scores
            predictions[pred_class] += 1

##### IMAGE OUTPUT #######################################################################

            # configure figure
            if enable_images or send_image:

                # set color and title
                color = label_colors[pred_class]
                title = label_titles[pred_class]

                # draw box
                image_y_size, image_x_size, _ = processed_images.rescaled.shape
                x, y = features["blob_x_coord"]*image_x_size-border_size, features["blob_y_coord"]*image_y_size-border_size
                w, h = features["blob_width"]*image_x_size, features["blob_height"]*image_y_size
                box = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=color, facecolor="none")
                ax.add_patch(box)

        # send image to ui
        if enable_images or send_image:

            # delete previous image from canvas
            clear_frame()

            # place new image on canvas
            ax.imshow(processed_images.rescaled, cmap="gray")
            canvas = FigureCanvasTkAgg(fig, master=tk_frame)
            canvas.get_tk_widget().pack(fill="both")

        # export .png
        if enable_images:
            pyplot.savefig(filename, bbox_inches="tight")

        # close the figure so matplotlib doesn't yell at me
        pyplot.close("all")

##### LOG OUTPUT #########################################################################

        for csv_time in times_in_this_block:
            # create and write row to output
            row = [str(round(csv_time, 3)), frame, predictions[3], 1 if predictions[3] > 0 else 0, predictions[2], 1 if predictions[2] > 0 else 0, 1 if predictions[7] > 0 else 0]
            if (csv_time == 0): row.extend(["", metadata['duration'], metadata['fps'], metadata['source_size'][0], metadata['source_size'][1]])
            csv_writer.writerow(row)

        # if our next barrier is past the end of the video, then we're done.
        if next_barrier > (num_frames / fps):
            break

        # update timestamp
        video_time = next_barrier
        csv_time += sampling_step_rate

    # remove progress bar and image upon completion
    progress_bar.forget()
