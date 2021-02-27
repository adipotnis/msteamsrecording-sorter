# checks video and uploads it to corresponding folder
import re
import cv2
import os
import pytesseract
from pytesseract import Output
import sys
import shutil
#print('Argument List:', str(sys.argv))_______________________________________________________________

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# filename to be accessed
filename = str(sys.argv[1])


#convert video beginning to image______________________________________________________________________

# Read the video from specified path
cam = cv2.VideoCapture(filename)

try:
    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

# if not created then raise error
except OSError:
    print ('Error Creating directory')

frame = 26

# reading from frame
ret,frame = cam.read()

if ret:

    name = 'stillimage.png'
    # writing the extracted images
    cv2.imwrite(name, frame)

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()

# get image and scan to find init text to sort__________________________________________________________

img = cv2.imread('stillimage.png')
custom_config = r'--oem 3 --psm 6'
pytesseract.image_to_string(img, config=custom_config)

gray = get_grayscale(img)
resized = cv2.resize(gray, (600,300), interpolation = cv2.INTER_AREA)

d = pytesseract.image_to_data(gray, output_type=Output.DICT)
textlist = d['text']
textstr = ''.join(textlist)
#print(textlist)

subject_dict ={'dictionary of professor and subject'} # Type for required code. Replace with reading text file

prof_list = ['List of professor names']# Name of professor related to subject. Replace with text file.
val = 0
for i in prof_list:
    for val, j in enumerate(textlist):
        if j == 'UTC':
            date_ind = val -2
            break
        else:
            date_ind = -3


    if (i in textstr) or (date_ind == -3):
        dest_folder = "$Enter Folder directory$" + subject_dict[i]+"/" + subject_dict[i] + textlist[date_ind]+'.mp4'
    else:
        est_folder = "$Enter Folder directory$" + subject_dict[i]+"/" + subject_dict[i] + +'.mp4'
        
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

        shutil.move(filename, dest_folder)

        print('{} is present'.format(i))
        break
