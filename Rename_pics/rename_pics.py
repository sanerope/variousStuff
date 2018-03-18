import os


i = 0
for filename in os.listdir("."):
    if filename.startswith("scene"):
        os.rename(filename, "7_frame_pos" + str(i) + ".jpg")
        i +=1