#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.1.0
#
# USAGE
#   To run the /dev/video camera  -  python3 videostream_test.py
#   To run the Raspberry Pi camera  -  python3 videostream_test.py -p
#
# SOURCE
#   "Unifying picamera and cv2.VideoCapture into a single class with OpenCV"
#   https://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/


# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import datetime
import argparse
import imutils
import time
import cv2
import sys


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera",
                help="the Raspberry Pi Camera should be used",
                action='store_true')
args = vars(ap.parse_args())

# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"]).start()
print("Camera warming up ...")
time.sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 600 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=600)

    # draw the timestamp on the frame
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A, %B %d, %Y - %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame in a pop-up window
    cv2.imshow("Frame", frame)

    # update the frame count
    fps.update()

    # if the `q` or esc key was pressed, break from the loop
    key = cv2.waitKey(1)
    if chr(key & 255) == 'q' or key == 27:
        print("Camera stopped by user ...")
        break

# stop the timer and display FPS information
fps.stop()
print("\telasped time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# cleanup by closing the window and stop video streaming
cv2.destroyAllWindows()
vs.stop()
