import logging
import pathlib

import numpy as np
import datetime as dt

from src import paths


def load_images_file_list(experiment_name):
    # Load all the images
    experiment_path = pathlib.Path(paths.raw_data_path / experiment_name)
    pics_path = experiment_path

    if not experiment_path.exists():
        logging.error(f"Experiment {experiment_name} does not exist!\n Check dir: {experiment_path}")
        exit()

    pics_list = sorted(pics_path.glob('*.jpg'), key=lambda path: int(path.stem))

    if pics_list.__len__() == 0:
        logging.warning(f"No images found in experiment: {experiment_name}!")
        exit()

    return pics_list


def date_parser(s):
    return np.datetime64(dt.datetime.strptime(s, '%d/%m/%Y %H:%M:%S'))


def load_log_data(experiment_name):
    # return np.genfromtxt(paths.raw_data_path / experiment_name / 'ramp.txt', delimiter=' \t ', names=True)

    return np.genfromtxt(paths.raw_data_path / experiment_name / 'ramp.txt',
                         delimiter=' \t ',
                         encoding='iso-8859-1',
                         dtype=[('julian', '<f8'),
                                ('date', 'datetime64[s]'),
                                ('time', '<f8'),
                                ('Ramp_ON', 'bool'),
                                ('RampSetTemp_°C', '<f8'),
                                ('Bath_Temp_°C', '<f8')],
                         skip_header=1,
                         converters={1: date_parser})


def load_readme(experiment_name):
    return np.genfromtxt(paths.raw_data_path / experiment_name / 'README.md')
