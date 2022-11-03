import logging
import pathlib

import click
import numpy as np
import datetime as dt
import cv2

from src.localdata import load_log_data
from src import paths
import matplotlib.pyplot as plt


def reconstruct_bath_temp(data):
    corrs = np.genfromtxt(paths.interim_data_path / 'temp_corrections.csv',
                          delimiter=',',
                          dtype=[('Setpoint_Temp_°C', '<f8'),
                                 ('T_mean_°C', '<f8')])

    t_reconstructed = []

    for i, line in enumerate(data):
        corr = corrs[corrs['Setpoint_Temp_°C'] == line['RampSetTemp_°C'].round(1)]['T_mean_°C'][0]
        t_reconstructed.append(line['RampSetTemp_°C'] - corr)

    d = data.copy()
    d['Bath_Temp_°C'] = t_reconstructed

    return d


def save_processed_data(experiment_name, pics_list, circles_positions, freezing_idxs, out_path, crop_values):

    logging.debug(f"Generating reports in path: {out_path}")

    pathlib.Path(out_path).mkdir(parents=True, exist_ok=True)

    data = load_log_data(experiment_name)

    data = data[data['Ramp_ON']]

    # Check if `Bath Temp` was recorded. If not, reconstruct the curve from the `Set Point`
    if data['Bath_Temp_°C'].sum() == 0:
        logging.warning(f"Reconstructing Bath Temperature for experiment: {experiment_name}")
        data = reconstruct_bath_temp(data)

    data['Bath_Temp_°C'] = data['Bath_Temp_°C'] * 0.917 + 1.3

    t = []
    ff = []
    freezing_events_time = []

    # Create an array with the times when freezing occurs
    for idx in freezing_idxs:
        freezing_events_time.append(dt.datetime.strptime(str(pics_list[idx].stem), '%H_%M_%S').time())

    with open(out_path / 'frozen_fraction_report.csv', 'w') as fo:
        fo.write("Date,SetpointTemp,BathTemp,FF\n")
        for record in data:
            i = 0
            for freezing_time in freezing_events_time:
                if record[1].astype(dt.datetime).time() >= freezing_time:
                    i += 1
            if record[3]:  # if RAMP ON
                fo.write(f'{record[1]},{record[4]},{record[5]},{i/freezing_events_time.__len__()}\n')

    generate_plots(out_path, experiment_name)
    generate_video(pics_list, circles_positions, freezing_idxs, out_path, crop_values)

    logging.debug("Reports done!")


def generate_plots(out_path, experiment):
    results = np.genfromtxt(out_path / 'frozen_fraction_report.csv',
                            delimiter=',',
                            dtype=[('index', 'int'), ('setpoint', '<f8'), ('bath_temp', '<f8'), ('ff', '<f8')])

    plt.figure()
    plt.plot(results['bath_temp'], results['ff'])

    plt.xlabel('Bath temp [°C]')
    plt.ylabel('FF')

    plt.grid()
    plt.title(f'{experiment}')
    plt.xlim((-30, 0))

    plt.savefig(out_path / 'frozen_fraction.jpg')
    # plt.show()


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

        # cv2.putText(img, f'Bath temp: {}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

    out = cv2.VideoWriter(str(out_path / 'video.avi'), cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()


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
