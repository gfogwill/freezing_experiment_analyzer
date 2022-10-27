import logging

import click
import cv2
import numpy as np
import pathlib
import os

from src.prompts import PARAM1_MIN, PARAM1_MAX, PARAM2_MIN, PARAM2_MAX, BLURRINESS_MIN, BLURRINESS_MAX, DEFAULT_MIN_DIST


def sort_circles(circles, n_cols):
    # https://stackoverflow.com/questions/61741434/opencv-sorting-array-of-circles
    circles = np.round(circles).astype("int")
    circles = sorted(circles, key=lambda v: [v[1], v[0]])

    sorted_rows = []
    for k in range(0, len(circles), n_cols):
        row = circles[k:k + n_cols]
        sorted_rows.extend(sorted(row, key=lambda v: v[0]))

    return sorted_rows


def plot_detected_circles(img, circles):
    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for n, i in enumerate(circles):
            # outer circle
            # cv2.circle(image, center_coordinates, radius, color, thickness)
            cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 1)

            # inner circle
            cv2.circle(img, (i[0], i[1]), 1, (0, 0, 255), 2)

            cv2.putText(img, "{}".format(n + 1), (i[0], i[1]), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 1)

    cv2.imshow('Image', img)
    cv2.waitKey(100)


def get_grayscales(image, circles, mask=True):
    grayscales = []

    for circle in circles:
        x = circle[0]
        y = circle[1]
        r = circle[2]

        img = image[y - r:y + r, x - r:x + r]

        if mask:
            # create a mask
            # https://stackoverflow.com/questions/50697179/opencv-and-python-how-croped-circle-area-only

            m = np.full((img.shape[0], img.shape[1]), 0, dtype=np.uint8)

            # create circle mask, center, radius, fill color, size of the border
            cv2.circle(m, (r, r), r, (255, 255, 255), -1)
            # get only the inside pixels
            fg = cv2.bitwise_or(img, img, mask=m)

            m = cv2.bitwise_not(m)
            background = np.full(img.shape, 255, dtype=np.uint8)
            bk = cv2.bitwise_or(background, background, mask=m)
            img = cv2.bitwise_or(fg, bk)

        grayscales.append(img.mean())

    return grayscales


def get_circles(img, n_cols, min_dist=20, param1=60, param2=10, min_radius=15, max_radius=20, sort=True, plot=True):
    logging.debug(f"Parameters used for circle Hough Transform:\n"
                  f"\tParameter 1: {param1}\n"
                  f"\tParameter 2: {param2}\n"
                  f"\tMin. distance: {min_dist}")

    # https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
    circles = cv2.HoughCircles(img,
                               cv2.HOUGH_GRADIENT,
                               1,
                               minDist=min_dist,
                               param1=param1,
                               param2=param2,
                               minRadius=min_radius,
                               maxRadius=max_radius
                               )[0]

    if sort:
        circles = sort_circles(circles, n_cols)

    if plot:
        plot_detected_circles(img, circles)

    return circles


def get_grayscales_evolution(
        files_list: list, crop_values: tuple[int, int, int, int], circles_positions: list) -> np.ndarray:
    """
    Given a set of images and the positions of each aliquote
    returns the grayscale evolution of each sample.

    Parameters
    ----------
    files_list : array_like
        list with pictures. The list must be sorted chronologically.
    crop_values : (int, int, int, int)
        tuple with the values to be used to crop the image.
            (start_col, start_row, end_col:end_row)
    circles_positions : array_like
        array with a tuple for each of the circles.
        [(200, 90, 11), ..., (400, 91, 11)]

        Each tuple: (row, col, radius)

    Returns
    -------
    grayscales_evolution : ndarray
        array of dimension N by 96. Where N is the number of pictures in the experiment
    """

    grayscales_evolution = []

    logging.debug('Analyzing images...')

    for fi in files_list:
        img = cv2.imread(str(fi))
        if crop_values is not None:
            img = img[crop_values[1]:crop_values[3], crop_values[0]:crop_values[2]]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(gray, 5)

        try:
            grayscales_evolution.append(get_grayscales(img_blur, circles_positions))
        except AttributeError:
            logging.error(f"Error in file {fi}")

    grayscales_evolution = np.array(grayscales_evolution)

    logging.debug('Finished analyzing!')

    return grayscales_evolution


def find_circles_position(fi, n_cols, n_rows, blurriness, param1, param2, min_distance, crop_values=None):
    circles_position = []

    img = cv2.imread(fi)

    n = n_rows * n_cols

    if crop_values is not None:
        img = img[crop_values[1]:crop_values[3], crop_values[0]:crop_values[2]]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if param1 is None:
        while circles_position.__len__() is not n:
            param1 = np.random.randint(PARAM1_MIN, PARAM1_MAX)
            param2 = np.random.randint(PARAM2_MIN, PARAM2_MAX)
            blurriness = np.random.randint(BLURRINESS_MIN, BLURRINESS_MAX)
            click.echo(f"Blurriness: {blurriness}")

            try:
                pic = cv2.medianBlur(gray, blurriness)
            except cv2.error:
                continue

            circles_position = get_circles(pic, n_cols, min_dist=DEFAULT_MIN_DIST, param1=param1, param2=param2)

            if circles_position.__len__() is not n:
                continue

            plot_detected_circles(pic, circles_position)

            return circles_position

    else:
        pic = cv2.medianBlur(gray, blurriness)
        circles_position = get_circles(pic, n_cols, min_dist=min_distance, param1=param1, param2=param2)

        plot_detected_circles(pic, circles_position)

        return circles_position
