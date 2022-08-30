import pathlib

import click
import numpy as np
import cv2

from src.localdata import load_log_data


def generate_reports(experiment_name, pics_list, circles_positions, freezing_idxs, out_path, crop_values):

    click.echo(f"Generating reports in path: {out_path}")

    pathlib.Path(out_path).mkdir(parents=True, exist_ok=True)

    data = load_log_data(experiment_name)

    t = []
    ff = []

    with open(out_path / 'frozen_fraction_report.csv', 'w') as fo:
        for i, line in enumerate(data):
            t.append(line['TC_Temperature_°C'])
            ff.append((np.array(freezing_idxs) <= i).sum()/freezing_idxs.__len__())
            fo.write(f'{i},{t[-1]},{ff[-1]}\n')

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

        for n, i in enumerate(circles):
            if int(filename.stem) < freezing_idxs[n]:
                cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 1)
            else:
                cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 1)

    out = cv2.VideoWriter(str(out_path / 'video.avi'), cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()
