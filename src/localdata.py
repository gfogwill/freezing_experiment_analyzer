import pathlib

import numpy as np

from src import paths


def load_images_file_list(experiment_name):
    # Load all the images
    files_path = pathlib.Path(paths.raw_data_path / experiment_name)
    files_list = sorted(pathlib.Path(files_path).glob('*.jpg'), key=lambda path: int(path.stem))
    return files_list


def load_log_data(experiment_name):
    return np.genfromtxt(paths.raw_data_path / experiment_name / 'log_data.csv', delimiter=',', names=True)
