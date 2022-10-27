import os

from src import __version__

from src import paths
from src.circles import get_grayscales_evolution, find_circles_position
from src.localdata import load_images_file_list
from src.prompts import input_crop_values, dialog_fix_bright_jump

import click
import numpy as np

from src.reports import save_processed_data

LOGO = rf"""
❄ Freezing Experiment Analizer ❄   
                                 v_{__version__}
"""


@click.group(context_settings=dict(help_option_names=["-h", "--help"]), name="BRR")
@click.version_option(__version__, "--version", "-V", help="Show version and exit")
def cli():
    """BRR is a CLI for working with freezing experiment data. For more
    information, type ``brr info``.
    """
    pass


@cli.command()
def info():
    """Get more information about brr."""
    click.secho(LOGO, fg="blue")
    click.echo(
        "\n"
    )


@cli.command()
@click.option('--experiment-name', type=str, default=None, required=True)
@click.option('--crop', is_flag=True, default=False, show_default=True, help="Crop the image. If crop_values are not "
                                                                             "passed as argument will ask to enter them"
                                                                             "manually")
@click.option('--crop-values', type=(int, int, int, int), default=None, help="Crop values")
@click.option('--n-cols', type=int, required=True, help="Number of columns of droplets in the experiment")
@click.option('--n-rows', type=int, required=True, help="Number of rows of droplets in the experiment")
@click.option('--blurriness', type=int, default=None, help="Blurriness to be applied before Hough transform")
@click.option('--hough-param1', type=int, default=None, help='First method-specific parameter for Hough '
                                                                       'Gradient Method.')
@click.option('--hough-param2', type=int, default=None, help='Second method-specific parameter for Hough '
                                                                       'Gradient Method.')
@click.option('--hough-min-distance', type=int, default=None, help='Minimum distance between the centers of'
                                                                               ' the detected circles.')
@click.option('--out-path', type=click.Path(), default=None, help="Output path to save reports.")
def analyze(experiment_name, crop_values, n_cols, n_rows, blurriness, hough_param1, hough_param2, hough_min_distance, out_path):
    """Analyze all the images to detect the frozen fraction"""

    # Set default report path if None
    if out_path is None:
        out_path = paths.processed_data_path / experiment_name

    pics_list = load_images_file_list(experiment_name)

    # Set crop values
    if crop_values is None:
        crop_values = input_crop_values(str(pics_list[0]))  # Use the first image to ask for input

    # Check if detected circles are correct
    circles_positions = find_circles_position(str(pics_list[0]), n_cols, n_rows, blurriness, hough_param1, hough_param2, hough_min_distance, crop_values)

    # Get the evolution of grayscale value for each circle
    grayscales_evolution = get_grayscales_evolution(pics_list, crop_values, circles_positions)

    # Find the indexes where freezing occurs
    freezing_idxs = []

    for i in range(grayscales_evolution.shape[-1]):
        grayscales_diffs = [t - s for s, t in zip(grayscales_evolution[:, i], grayscales_evolution[1:, i])]
        freezing_idxs.append(np.argmax(np.abs(grayscales_diffs)) + 1)

    save_processed_data(experiment_name, pics_list, circles_positions, freezing_idxs, out_path, crop_values)


if __name__ == '__main__':
    from src import paths

    # experiment = "221013_LVS46_0901_0640_660min_T95_001"
    # drincz_analysis(experiment, True, (280, 194, 826, 532), 12, 8, 7, 100, 10, 30)

    for experiment in os.listdir(paths.raw_data_path):
        if not experiment.startswith('.') and experiment.split('_')[1].startswith('BT') and experiment == '221025_BT17_0831_0757_T20_001':
            click.echo(f"Processing experiment {experiment}")
            # drincz_analysis(experiment, True, None, 12, 8, 7, 100, 10, 30)
            drincz_analysis(experiment, (280, 194, 826, 532), 12, 8, 7, 100, 10, 30)

