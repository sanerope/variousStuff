#!/usr/bin/python
# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care

import sys, os
from time import time
import fnmatch
import shutil

sys.path.append(os.path.join(os.getcwd(),'python/'))

# import darknet as dn
# import pdb
import subprocess

# dn.set_gpu(0)
# net = dn.load_net("cfg/yolo.cfg", "yolo.weights", 0)
# meta = dn.load_meta("cfg/coco.data")


class DarknetWrapper:

    def __init__(self):
        self.found_files = 0

    def get_list_of_frames(self):
        file_paths = []
        for root, dirnames, filenames in os.walk('data/frames'):
            for filename in fnmatch.filter(filenames, '*.jpg'):
                file_paths.append(os.path.join(root, filename))

        print "Found " + str(len(file_paths)) + " frames"
        self.found_files = len(file_paths)
        return file_paths

    def get_predicted_image(self):
        for file in os.listdir('.'):
            if file == 'predictions.png':
                return file

    def move_predicted_image(self, original_file, predicted_file):
        predicted_folder = '/predicted/'
        drive, path_to_original_file = os.path.splitdrive(original_file)
        path, org_file = os.path.split(path_to_original_file)
        new_name = 'predicted_' + org_file.split('.')[0] + '.png'
        new_path = path + predicted_folder
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        shutil.move(predicted_file, new_path + new_name)

    def find_objects_on_image(self, frame, config=' cfg/yolo.cfg', weights=' yolo.weights '):
        # frame = 'data/frames/1_frames/scene00776.jpg'
        command = './darknet detect' + config + weights
        proc = subprocess.Popen(command + frame, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, error) = proc.communicate()
        print output, error

    def run(self):
        list_of_frames = self.get_list_of_frames()



cos = DarknetWrapper()
list_of_frames = cos.get_list_of_frames()
count = 0
for frame in list_of_frames:
    cos.find_objects_on_image(frame)
    predicted_frame = cos.get_predicted_image()
    cos.move_predicted_image(frame, predicted_frame)
    count += 1
    print "\n\n\nPredicted: " + str(count) + "/" + str(cos.found_files) + " frames\n\n\n"


#SPOSOB NA WYWWOANIE TEGO Z METOD A JA ROBIE PO PROSTU Z EXE
# print time()
# r = dn.detect(net, meta, frame)
# print r
# print time()
