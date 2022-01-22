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
    video_aspect_ratio = video_width / video_height
    console_height, console_width = stdscr.getmaxyx()
    print(console_height, console_width)
    console_aspect_ratio = console_width / console_height / 2.25
    offset_x = offset_y = 0

    print(console_aspect_ratio, video_aspect_ratio)

    pixel_width, pixel_height = int(video_width / console_width), int(video_height / console_height)
    if video_aspect_ratio < console_aspect_ratio:
        pixel_width = int(video_aspect_ratio * pixel_height)
        offset_x = console_width
        console_width = int(console_height * video_aspect_ratio * 1.83)
        offset_x = int((offset_x - console_width) / 2)
    # else:
    #     pixel_height = int(video_aspect_ratio * pixel_width)
    #     offset_y = console_height
    #     console_height = int(console_width / video_aspect_ratio)
    #     offset_y = int((offset_y - console_height) / 2)

    while success:
        stdscr.clear()
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        for x in range(console_width - 1):
            for y in range(console_height):
                print(y, x)
                pixel = get_pixel(frame[y * pixel_height:y * pixel_height + pixel_height,
                                  x * pixel_width:x * pixel_width + pixel_width])
                print(offset_x, offset_y)
                stdscr.addch(y + offset_y, x + offset_x, pixel)
        stdscr.refresh()
        frame_index += fps
        success, frame = vidcap.read()


wrapper(main)
