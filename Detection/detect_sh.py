#!/usr/bin/python

import sys, os
from time import time
import fnmatch
import shutil
import subprocess

class DarknetWrapper:

    def __init__(self):
        self.found_frames = 0
        self.found_weights = 0

    def get_list_of_frames(self):
        file_paths = []
        for root, dirnames, filenames in os.walk('data'):
            for filename in fnmatch.filter(filenames, '*.jpg'):
                file_paths.append(os.path.join(root, filename))

        print "Found " + str(len(file_paths)) + " frames"
        self.found_frames = len(file_paths)
        return file_paths

    def get_list_of_weights(self):
        file_paths = []
        for root, dirnames, filenames in os.walk('backup'):
            for filename in fnmatch.filter(filenames, '*.weights'):
                file_paths.append(os.path.join(root, filename))

        print "Found " + str(len(file_paths)) + " weights"
        self.found_weights = len(file_paths)
        return file_paths

    def get_predicted_image(self):
        for file in os.listdir('.'):
            if file == 'predictions.png':
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

    def find_objects_on_image(self, frame, data=' cfg/coco.data', config=' yolo-obj.cfg',
                              weights=' backup/yolo.weights '):
        # frame = 'data/frames/1_frames/scene00776.jpg'
        command = './darknet detector test' + data + config + weights
        proc = subprocess.Popen(command + frame, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, error) = proc.communicate()
        print output, error

    def run(self):
        list_of_frames = self.get_list_of_frames()


cos = DarknetWrapper()
list_of_frames = cos.get_list_of_frames()
list_of_weights = cos.get_list_of_weights()


count_weights= 0

for weight in list_of_weights:
    count_frames = 0
    count_weights +=1
    for frame in list_of_frames:
        cos.find_objects_on_image(frame, data=' cfg/coco.data', config=' yolo-obj.cfg',
                              weights=' ' + weight + ' ')
        predicted_frame = cos.get_predicted_image()
        cos.move_predicted_image(frame, predicted_frame, weight)
        count_frames += 1
        print "\n\nWeight: " + str(count_weights) + "/" + str(cos.found_weights)
        print "\nPredicted: " + str(count_frames) + "/" + str(cos.found_frames) + " frames for weight " + weight + "\n\n\n"
