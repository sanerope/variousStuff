#!/usr/bin/python
# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care
import re
import sys, os
from time import time
import fnmatch
import shutil

sys.path.append(os.path.join(os.getcwd(),'python/'))

import darknet as dn
# import pdb
import subprocess

dn.set_gpu(1)
# net = dn.load_net("cfg/yolo.cfg", "yolo.weights", 0)
meta = dn.load_meta("data/obj.data")


class DarknetWrapper:

    def __init__(self):
        self.found_frames = 0
        self.found_weights = 0

    def get_list_of_frames(self):
        file_paths = []
        for root, dirnames, filenames in os.walk('data/img'):
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

    def find_objects_on_image(self, frame, data=' data/obj.data', config=' yolo-obj.cfg',
                              weights=' backup/yolo.weights '):
        # frame = 'data/frames/1_frames/scene00776.jpg'
        command = './darknet.exe detector test' + data + config + weights
        proc = subprocess.Popen(command + frame, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, error) = proc.communicate()
        print output, error

    def find_objects_on_image_lib(self, net, meta, frame):
        # frame = 'data/frames/1_frames/scene00776.jpg
        return dn.detect(net, meta, frame)
        # print r

    def run(self):
        list_of_frames = self.get_list_of_frames()

    def write_to_file(self, frame, weight, text_to_write):
        predicted_folder = '/predicted_' + weight + '/'
        drive, path_to_original_file = os.path.splitdrive(frame)
        path, org_file = os.path.split(path_to_original_file)
        new_name = 'predicted_' + org_file.split('.')[0] + '.txt'
        new_path = path + predicted_folder
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        text_to_write = text_to_write.split('\n')
        file = open(new_path + new_name, 'w')
        for line in text_to_write:
            file.write(line + '\n')

        file.close()


cos = DarknetWrapper()
list_of_frames = cos.get_list_of_frames()
list_of_weights = cos.get_list_of_weights()

count_weights = 0

for weight in list_of_weights:
    net = dn.load_net("yolo-obj.cfg", weight, 0)
    count_frames = 0
    count_weights += 1
    for frame in list_of_frames:
        r, text_to_write = cos.find_objects_on_image_lib(net, meta, frame)
        cos.write_to_file(frame, weight, text_to_write)
        count_frames += 1
        print "\n\nWeight: " + str(count_weights) + "/" + str(cos.found_weights)
        print "\nPredicted: " + str(count_frames) + "/" + str(
            cos.found_frames) + " frames for weight " + weight + "\n\n\n"

