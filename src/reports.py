import pathlib

import click
import numpy as np

from src import paths


def generate_reports(experiment_name, freezing_idxs, out_path):

    click.echo(f"Generating reports in path: {out_path}")

    pathlib.Path(out_path).mkdir(parents=True, exist_ok=True)
    data = np.genfromtxt(paths.raw_data_path / experiment_name / 'log_data.csv', delimiter=',', names=True)

    t = []
    ff = []

    with open(out_path / 'frozen_fraction_report.csv', 'w') as fo:
        for i, line in enumerate(data):
            t.append(line['TC_Temperature_°C'])
            ff.append((np.array(freezing_idxs) <= i).sum()/freezing_idxs.__len__())
            fo.write(f'{i},{t[-1]},{ff[-1]}\n')

    click.echo("Reports done!")
