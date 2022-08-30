from src import __version__

from src import paths
from src.circles import get_grayscales_evolution
from src.localdata import load_images_file_list
from src.prompts import input_crop_values, check_circles_position, dialog_fix_bright_jump

import click
import numpy as np

from src.reports import generate_reports

DEFAULT_BLURRINESS = 5
DEFAULT_PARAM1 = 200
DEFAULT_PARAM2 = 7
DEFAULT_MIN_DIST = 10

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
@click.option('--blurriness', type=int, default=DEFAULT_BLURRINESS, help="Blurriness to be applied before Hough transform")
@click.option('--hough_param1', type=int, default=DEFAULT_PARAM1, help='First method-specific parameter for Hough '
                                                                       'Gradient Method.')
@click.option('--hough_param2', type=int, default=DEFAULT_PARAM2, help='Second method-specific parameter for Hough '
                                                                       'Gradient Method.')
@click.option('--hough_min_distance', type=int, default=DEFAULT_MIN_DIST, help='Minimum distance between the centers of'
                                                                               ' the detected circles.')
@click.option('--fix-bright-jump', is_flag=True, default=False, help="Find the point where the bright changes and "
                                                                     "fix the brightness of all images after that "
                                                                     "point.")
@click.option('--out-path', type=click.Path(), default=None, help="Output path to save reports.")
def analyze(experiment_name, crop, crop_values, blurriness, hough_param1, hough_param2, hough_min_distance, fix_bright_jump, out_path):
    """Analyze all the images to detect the frozen fraction"""

    # Set default report path if None
    if out_path is None:
        out_path = paths.reports_path / experiment_name

    pics_list = load_images_file_list(experiment_name)

    # Set crop values
    if crop and crop_values is None:
        crop_values = input_crop_values(str(pics_list[0]))  # Use the first image to ask for input

    # Check if detected circles are correct
    circles_positions = check_circles_position(str(pics_list[0]), blurriness, hough_param1, hough_param2, hough_min_distance, crop_values)

    # Get the evolution of grayscale value for each circle
    grayscales_evolution, mean_grayscale_evolution = get_grayscales_evolution(pics_list, crop_values, circles_positions)

    if fix_bright_jump:
        grayscales_evolution = dialog_fix_bright_jump(grayscales_evolution, mean_grayscale_evolution)

    # Find the indexes where freezing occurs
    freezing_idxs = []

    for i in range(grayscales_evolution.shape[-1]):
        grayscales_diffs = [t - s for s, t in zip(grayscales_evolution[:, i], grayscales_evolution[1:, i])]
        freezing_idxs.append(np.argmax(grayscales_diffs) + 1)

    click.echo(freezing_idxs)

    generate_reports(experiment_name, pics_list, freezing_idxs, out_path)


if __name__ == '__main__':
    analyze(['--experiment-name', 'channel_0_b', '--crop', '--fix-bright-jump'])
