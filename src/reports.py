import pathlib

import click
import numpy as np
import datetime as dt
import cv2

from src.localdata import load_log_data


def generate_reports(experiment_name, pics_list, circles_positions, freezing_idxs, out_path, crop_values):

    click.echo(f"Generating reports in path: {out_path}")

    pathlib.Path(out_path).mkdir(parents=True, exist_ok=True)

    data = load_log_data(experiment_name)

    t = []
    ff = []
    freezing_events_time = []

    # Create an array with the times when freezing occurs
    for idx in freezing_idxs:
        freezing_events_time.append(dt.datetime.strptime(str(pics_list[idx].stem), '%H_%M_%S').time())

    with open(out_path / 'frozen_fraction_report.csv', 'w') as fo:
        for record in data:
            i = 0
            for freezing_time in freezing_events_time:
                if record[1].astype(dt.datetime).time() >= freezing_time:
                    i += 1
            fo.write(f'{record[1]},{record[5]},{i / freezing_events_time.__len__()}\n')

    generate_video(pics_list, circles_positions, freezing_idxs, out_path, crop_values)

    click.echo("Reports done!")


def generate_video(pic_list, circles_positions, freezing_idxs, out_path, crop_values=None):
    circles = np.uint16(np.around(circles_positions))

    img_array = []
    for filename in pic_list:
        img = cv2.imread(str(filename))
        if crop_values is not None:
            img = img[crop_values[1]:crop_values[3], crop_values[0]:crop_values[2]]
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

        freezing_events_time = []
        for idx in freezing_idxs:
            freezing_events_time.append(dt.datetime.strptime(str(pic_list[idx].stem), '%H_%M_%S').time())

        for n, i in enumerate(circles):
            if dt.datetime.strptime(str(filename.stem), '%H_%M_%S').time() < freezing_events_time[n]:
                cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 2)
            else:
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)

    out = cv2.VideoWriter(str(out_path / 'video.avi'), cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()
