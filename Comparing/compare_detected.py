import os
import re
from os import walk, getcwd
import csv


"""-------------------------------------------------------------------"""

""" Configure Paths"""
valid_txt_path = 'img_handshake_oznaczone/'
detected_txt_path = 'img_handshake_wyliczone/'
outpath = "CSV_dic/"


""" Get input text file list """
txt_name_list = []

for root, dirnames, filenames in os.walk(detected_txt_path):
    for dirname in dirnames:
        try:
            os.makedirs(outpath)
        except OSError:
            if not os.path.isdir(outpath):
                raise
        for root2, dirnames2, filenames2 in os.walk(detected_txt_path + dirname):
            txt_name_list.extend(map(lambda filename: dirname + '/' + filename, filenames2))


print "Found " + str(len(txt_name_list)) + " files"
# print(txt_name_list)

""" Process """
for txt_name in txt_name_list:
    # txt_file =  open("Labels/stop_sign/001.txt", "r")
    raw_txt_name = os.path.split(txt_name)[1]
    raw_txt_name = re.sub("predicted_", "", raw_txt_name)

    """ Open detected text files """
    full_detected_txt_path = detected_txt_path + txt_name
    print("Detected:" + full_detected_txt_path)
    detected_txt_file = open(full_detected_txt_path, "r")
    detected_lines = detected_txt_file.read().split('\n')  # for ubuntu, use "\r\n" instead of "\n"

    # txt_name = re.sub("predicted_", "", txt_name)

    """ Open valid text files """
    full_valid_txt_path = valid_txt_path + raw_txt_name
    print("Valid:" + full_valid_txt_path)
    valid_txt_file = open(full_valid_txt_path, "r")
    valid_lines = valid_txt_file.read().split('\n')  # for ubuntu, use "\r\n" instead of "\n"


    total = 0

    with open(full_valid_txt_path) as f:
        for i, line in enumerate(f):
            if line:
                total +=1

    weight_number = str(re.findall(r'\d+', os.path.split(full_detected_txt_path)[0])[0])

    """ Compare data """
    total_detected = 0
    match = 0
    false_positive = 0

    with open(full_detected_txt_path) as f_d:
        for i_d, line_d in enumerate(f_d):
            if line_d:
                total_detected +=1

    if total == 0 and total_detected != 0:
        match = 0
        false_positive = total_detected
        csv_row = [raw_txt_name, total, match, false_positive]
        print weight_number + ": CSV row: "
        print csv_row

        with open('CSV_dic/' + weight_number + '.csv', 'ab') as csv_File:
            csv_FileWriter = csv.writer(csv_File)
            if csv_row:
                csv_FileWriter.writerow(csv_row)

    if total_detected == 0:
        match = 0
        false_positive = 0
        csv_row = [raw_txt_name, total, match, false_positive]
        print weight_number + ": CSV row: "
        print csv_row

        with open('CSV_dic/' + weight_number + '.csv', 'ab') as csv_File:
            csv_FileWriter = csv.writer(csv_File)
            if csv_row:
                csv_FileWriter.writerow(csv_row)

    ct = 0
    for valid_line in valid_lines:

        if (len(valid_line) >= 2):

            match = 0
            false_positive = 0
            ct = ct + 1
            # print(valid_line + "\n")
            valid_elems = valid_line.split(' ')
            print(valid_elems)
            xmin_valid = float(valid_elems[1])
            xmax_valid = float(valid_elems[3])
            ymin_valid = float(valid_elems[2])
            ymax_valid = float(valid_elems[4])

            xmin_match = False
            xmax_match = False
            ymin_match = False
            ymax_match = False


            for detected_line in detected_lines:
                if (len(detected_line) >= 2):
                    detected_elems = detected_line.split(' ')
                    print(valid_elems)
                    xmin_detected = float(detected_elems[1])
                    xmax_detected = float(detected_elems[3])
                    ymin_detected = float(detected_elems[2])
                    ymax_detected = float(detected_elems[4])

                    xmin_match = False
                    xmax_match = False
                    ymin_match = False
                    ymax_match = False
                    # variance 35%
                    variance = float(0.45)
                    if (xmin_detected <= xmin_valid*(1 + variance) and xmin_detected >= xmin_valid*(1 - variance) ):
                        xmin_match = True

                    if (xmax_detected <= xmax_valid*(1 + variance) and xmax_detected >= xmax_valid*(1 - variance)):
                        xmax_match = True

                    if (ymin_detected <= ymin_valid*(1 + variance) and ymin_detected >= ymin_valid*(1 - variance)):
                        ymin_match = True

                    if (ymax_detected <= ymax_valid*(1 + variance) and ymax_detected >= ymax_valid*(1 - variance) ):
                        ymax_match = True

                    if (xmax_match and xmin_match and ymin_match and ymax_match):
                        match += 1


    if total >= 1 and total_detected >= 1:
        false_positive = total_detected - match
        csv_row = [raw_txt_name, total, match, false_positive]
        print weight_number + ": CSV row: "
        print csv_row

        with open('CSV_dic/' + weight_number +'.csv', 'ab') as csv_File:
            csv_FileWriter = csv.writer(csv_File)
            if csv_row:
                csv_FileWriter.writerow(csv_row)
