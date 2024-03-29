import logging
import pathlib

import numpy as np

from brr import paths


def load_images_file_list(experiment_name):
    # Load all the images
    experiment_path = pathlib.Path(paths.raw_data_path / experiment_name)
    pics_path = experiment_path / 'pics'

    if not experiment_path.exists():
        logging.error(f"Experiment {experiment_name} does not exist!\n Check dir: {experiment_path}")
        exit()

    pics_list = sorted(pics_path.glob('*.png'), key=lambda path: int(path.stem))

    if pics_list.__len__() == 0:
        logging.error("No images found!")
        exit()

    return pics_list


def load_log_data(experiment_name):
    return np.genfromtxt(paths.raw_data_path / experiment_name / 'log_data.csv', delimiter=',', names=True)


def load_readme(experiment_name):
    return np.genfromtxt(paths.raw_data_path / experiment_name / 'README.md')
