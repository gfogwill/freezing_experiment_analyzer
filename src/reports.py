import pathlib

import click
import numpy as np
import cv2

from src.localdata import load_log_data


def generate_reports(experiment_name, pics_list, freezing_idxs, out_path):

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

    generate_video(pics_list, out_path)

    click.echo("Reports done!")


def generate_video(pic_list, out_path):
    img_array = []
    for filename in pic_list:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(out_path / 'video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
