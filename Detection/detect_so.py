#!/usr/bin/python

import sys, os
from time import time
import fnmatch
import shutil
import subprocess
import darknet as dn

dn.set_gpu(0)
net = dn.load_net("cfg/yolo.cfg", "yolo.weights", 0)
meta = dn.load_meta("data/yolo-obj.data")

class DarknetWrapper:

    def __init__(self):
        self.found_files = 0

    def get_list_of_frames(self):
        file_paths = []
        for root, dirnames, filenames in os.walk('data/img'):
            for filename in fnmatch.filter(filenames, '*.jpg'):
                file_paths.append(os.path.join(root, filename))

        print "Found " + str(len(file_paths)) + " frames"
        self.found_files = len(file_paths)
        return file_paths

    def get_list_of_weights(self):
        file_paths = []
        for root, dirnames, filenames in os.walk('backup'):
            for filename in fnmatch.filter(filenames, '*.weights'):
                file_paths.append(os.path.join(root, filename))

        print "Found " + str(len(file_paths)) + " weights"
        self.found_files = len(file_paths)
        return file_paths

    def get_predicted_image(self):
        for file in os.listdir('.'):
            if file == 'predictions.png':
                return file
            if file == 'predictions.jpg':
                return file

    def move_predicted_image(self, original_file, predicted_file, weight):
        predicted_folder = '/predicted_' + weight + '/'
        drive, path_to_original_file = os.path.splitdrive(original_file)
        path, org_file = os.path.split(path_to_original_file)
        new_name = 'predicted_' + org_file.split('.')[0] + '.png'
        new_path = path + predicted_folder
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        shutil.move(predicted_file, new_path + new_name)

    def find_objects_on_image(self, net, meta, frame):
        # frame = 'data/frames/1_frames/scene00776.jpg
        dn.detect(net, meta, frame)
        # print r


cos = DarknetWrapper()
list_of_frames = cos.get_list_of_frames()
count = 0
list_of_weights = cos.get_list_of_weights()

for weight in list_of_weights:
    net = dn.load_net("yolo-obj.cfg", "backup/" + weight, 0)

    for frame in list_of_frames:
        cos.find_objects_on_image(net, meta, frame)
        predicted_frame = cos.get_predicted_image()
        cos.move_predicted_image(frame, predicted_frame, weight)
        count += 1
        print "\n\n\nPredicted: " + str(count) + "/" + str(cos.found_files) + " frames for weight " + weight + "\n\n\n"
