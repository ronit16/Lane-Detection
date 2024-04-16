"""
Lane Lines Detection pipeline

Usage:
    main.py [--video] INPUT_PATH OUTPUT_PATH 

Options:

-h --help                               show this screen
--video                                 process video file instead of image
"""

import numpy as np
import matplotlib.image as mpimg
import cv2
from docopt import docopt
from IPython.display import HTML, Video
from moviepy.editor import VideoFileClip
from CameraCalibration import CameraCalibration
from Thresholding import *
from PerspectiveTransformation import *
from LaneLines import *

class FindLaneLines:
    """ This class is for parameter tunning.

    Attributes:
        ...
    """
    def __init__(self):
        """ Init Application"""
        self.calibration = CameraCalibration('camera_cal', 9, 6)
        self.thresholding = Thresholding()
        self.transform = PerspectiveTransformation()
        self.lanelines = LaneLines()

    def forward(self, img):
        out_img = np.copy(img)
        #plot the image img
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img = self.calibration.undistort(img)
        # cv2.imshow('undistort', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img = self.transform.forward(img)
        # cv2.imshow('transform', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img = self.thresholding.forward(img)
        # cv2.imshow('thresholding', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img = self.lanelines.forward(img)
        # cv2.imshow('lanelines', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img = self.transform.backward(img)
        # cv2.imshow('backward', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        out_img = cv2.addWeighted(out_img, 1, img, 0.6, 0)
        # cv2.imshow('out_img', out_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        out_img = self.lanelines.plot(out_img)
        # cv2.imshow('plot', out_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return out_img

    def process_image(self, input_path, output_path):
        img = mpimg.imread(input_path)
        img = cv2.resize(img, (1280, 720))
        out_img = self.forward(img)
        mpimg.imsave(output_path, out_img)

    def process_video(self, input_path, output_path):
        clip = VideoFileClip(input_path)
        out_clip = clip.fl_image(self.forward)
        out_clip.write_videofile(output_path, audio=False)

def main():
    args = docopt(__doc__)
    input = args['INPUT_PATH']
    output = args['OUTPUT_PATH']

    findLaneLines = FindLaneLines()
    if args['--video']:
        findLaneLines.process_video(input, output)
    else:
        findLaneLines.process_image(input, output)


if __name__ == "__main__":
    main()