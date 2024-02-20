#!/usr/bin/env python
# python-fu-batch-convert-gif-to-webp
# Created by ChatGPT
# Copyright (C) ChatGPT, 2024

import os
import sys
import json
from gimpfu import *

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# Construct the relative path to config.json
CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, "config.json")

def save_last_used_folders(input_folder, output_folder):
    if not input_folder or not output_folder:
        # Don't save if input_folder or output_folder is empty
        return
    try:
        config = {'input_folder': input_folder, 'output_folder': output_folder}
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            json.dump(config, configfile, indent=4)
    except Exception as e:
        gimp.message("Error saving config: {}".format(str(e)))

def load_last_used_folders():
    input_folder = ""
    output_folder = ""
    try:
        with open(CONFIG_FILE_PATH, 'r') as configfile:
            config = json.load(configfile)
            input_folder = config.get('input_folder', '')
            output_folder = config.get('output_folder', '')
    except Exception as e:
        gimp.message("Error loading config: {}".format(str(e)))
    return input_folder, output_folder

def batch_convert_gif_to_webp(input_dir, output_dir, preset, lossless, quality, alpha, animation, animation_loop, minimize_size, kf_distance, exif, iptc, xmp, delay, force_delay):
    
    try:    
        # Ensure input and output folders exist
        if not os.path.exists(input_dir):
            gimp.message("Input directory does not exist: {}" . format(input_dir))
            return
        if not os.path.exists(output_dir):
            gimp.message("Output directory does not exist: {}" . format(output_dir))
            return
                
        # Loop through each file in the input directory, make sure it read in Unicode
        for root, dirs, files in os.walk(unicode(input_dir)):
            for filename in files:
                if filename.endswith(".gif"):
                    input_file = os.path.join(root, filename)
                    relative_path = os.path.relpath(input_file, input_dir)
                    output_file = os.path.join(output_dir, relative_path[:-4] + ".webp")
                    
                    # Create directories if they don't exist
                    output_subdir = os.path.dirname(output_file)
                    if not os.path.exists(output_subdir):
                        os.makedirs(output_subdir)
                        
                    # Load the GIF image
                    image = pdb.file_gif_load(input_file, input_file)

                    # Save the image as WebP        
                    pdb.file_webp_save(image, image.active_layer, output_file, output_file, preset, lossless, quality, alpha, animation, animation_loop, minimize_size, kf_distance, exif, iptc, xmp, delay, force_delay)

                    # Close the image without saving changes
                    pdb.gimp_image_delete(image)
    except Exception as e:
        gimp.message("An error occurred during batch conversion: {}" . format(str(e)))
                
    # Save the last used input and output directories
    save_last_used_folders(input_dir, output_dir)

# Register the plugin
register(
    "python-fu-batch-convert-gif-to-webp",
    "Batch convert GIF files to WebP format",
	"Batch convert GIF files to WebP format written by ChatGPT",
    "ChatGPT",
    "Copyright (C) ChatGPT, 2024",
    "2024",
    "_Batch GIF to WebP...",
    "*",
    [
        (PF_DIRNAME, "input_dir", "Input folder", load_last_used_folders()[0]),
        (PF_DIRNAME, "output_dir", "Output folder", load_last_used_folders()[1]),
        (PF_OPTION, "preset", "Source type", 0, ["Default", "Picture", "Photo", "Drawing", "Icon", "Text"]),
        (PF_TOGGLE, "lossless", "Lossless", 0),
        (PF_SLIDER, "quality", "Image Quality", 80, (0, 100, -1)),
        (PF_SLIDER, "alpha", "Alpha Quality", 100, (0, 100, -1)),
        (PF_TOGGLE, "animation", "Animation", 1),
        (PF_TOGGLE, "animation_loop", "Loop forever", 1),
        (PF_TOGGLE, "minimize_size", "Minimize output size", 1),
        (PF_SPINNER, "kf_distance", "Max distance between key-frames", 50, (0, 10000, 1)),
        (PF_TOGGLE, "exif", "Save Exif data", 1),
        (PF_TOGGLE, "iptc", "Save IPTC", 1),
        (PF_TOGGLE, "xmp", "Save XMP data", 1),
        (PF_SPINNER, "delay", "Delay between frames", 200, (1, 10000, 1)),
        (PF_TOGGLE, "force_delay", "Force delay", 0)
    ],
    [],
    batch_convert_gif_to_webp,
    menu="<Toolbox>/Plugins"
)

# Create a GIMP menu entry
main()