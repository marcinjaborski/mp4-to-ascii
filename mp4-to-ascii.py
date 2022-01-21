import cv2
import numpy as np
from curses import wrapper

luminance = ['.', ',', '-', '~', ':', ';', '=', '!', '*', '#', '$', '@']


def get_pixel(arr):
    return luminance[round(np.mean(arr) / 23)]


def main(stdscr):
    stdscr.clear()
    stdscr.refresh()

    vidcap = cv2.VideoCapture('sample2.mp4')
    fps = int(vidcap.get(cv2.CAP_PROP_FPS) / 3)
    frame_index = 0
    success, frame = vidcap.read()

    video_height, video_width, *_ = frame.shape
    console_height, console_width = stdscr.getmaxyx()
    pixel_width, pixel_height = int(video_width / console_width), int(video_height / console_height)

    while success:
        stdscr.clear()
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        for x in range(console_width - 1):
            for y in range(console_height):
                pixel = get_pixel(frame[y * pixel_height:y * pixel_height + pixel_height,
                                  x * pixel_width:x * pixel_width + pixel_width])
                stdscr.addch(y, x, pixel)
        stdscr.refresh()
        frame_index += fps
        success, frame = vidcap.read()


wrapper(main)
