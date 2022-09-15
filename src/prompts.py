import click
import cv2
import numpy as np

from matplotlib import pyplot as plt

from src.circles import plot_detected_circles, get_circles

PARAM1_MIN, PARAM1_MAX = 70, 250
PARAM2_MIN, PARAM2_MAX = 4, 15
DEFAULT_MIN_DIST = 30
BLURRINESS_MIN, BLURRINESS_MAX = 0, 9

# Create point matrix get coordinates of mouse click on image
point_matrix = [[-1, -1], [-1, -1]]

counter = 0


def mousePoints(event, x, y, flags, params):
    global counter
    # Left button mouse click event opencv
    if event == cv2.EVENT_LBUTTONDOWN:
        click.echo(f"Coortinate X: {x}\nCoordinate Y: {y}\n")

        point_matrix[counter] = x, y
        counter = counter + 1


def input_crop_values(fi):
    img = cv2.imread(fi)

    click.echo("Click in the top-left corner you want to crop. Then click the bottom-right one.")

    while True:
        if counter == 2:
            starting_x = point_matrix[0][0]
            starting_y = point_matrix[0][1]

            ending_x = point_matrix[1][0]
            ending_y = point_matrix[1][1]
            # Draw rectangle for area of interest
            cv2.rectangle(img, (starting_x, starting_y), (ending_x, ending_y), (0, 255, 0), 3)

            # Cropping image
            img_cropped = img[starting_y:ending_y, starting_x:ending_x]

            cv2.destroyAllWindows()

            cv2.imshow("Cropped image", img_cropped)
            cv2.waitKey(100)

            if click.confirm('Happy with the result?', abort=True):
                cv2.destroyAllWindows()

                return starting_x, starting_y, ending_x, ending_y

        # Showing original image
        cv2.imshow("Original Image ", img)
        # Mouse click event on original image
        cv2.setMouseCallback("Original Image ", mousePoints)
        # Refreshing window all time
        cv2.waitKey(1)


def check_circles_position(fi, n_cols, n_rows, blurriness, param1, param2, min_distance, crop_values=None):
    circles_position = []

    img = cv2.imread(fi)

    n = n_rows * n_cols

    if crop_values is not None:
        img = img[crop_values[1]:crop_values[3], crop_values[0]:crop_values[2]]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if param1 is None:
        while circles_position.__len__() is not n:
            param1 = np.random.randint(PARAM1_MIN, PARAM1_MAX)
            param2 = np.random.randint(PARAM2_MIN, PARAM2_MAX)
            blurriness = np.random.randint(BLURRINESS_MIN, BLURRINESS_MAX)

            click.echo(f"Blurriness: {blurriness}")
            try:
                pic = cv2.medianBlur(gray, blurriness)
            except cv2.error:
                continue

            circles_position = get_circles(pic, n_cols, min_dist=DEFAULT_MIN_DIST, param1=param1, param2=param2)
            if circles_position.__len__() is not n: continue

            plot_detected_circles(pic, circles_position)

            if click.confirm("Are the circles in the correct position?"):
                cv2.destroyAllWindows()

                return circles_position
            else:
                circles_position = []
                continue

    else:
        pic = cv2.medianBlur(gray, blurriness)
        circles_position = get_circles(pic, n_cols, min_dist=min_distance, param1=param1, param2=param2)

        plot_detected_circles(pic, circles_position)

        if click.confirm("Are the circles in the correct position?", abort=True):
            cv2.destroyAllWindows()

            return circles_position


def dialog_fix_bright_jump(grayscales_evolution, mean_grayscale_evolution):
    grayscale_diffs = [t - s for s, t in zip(mean_grayscale_evolution, mean_grayscale_evolution[1:])]
    step_index = np.argmax(np.abs(grayscale_diffs)) + 1
    click.echo(f"Jump in brightness detected in image {step_index}")

    plt.plot(mean_grayscale_evolution)
    plt.axvline(step_index, color='r')
    plt.ion()
    plt.show(block=False)
    plt.pause(1)

    if click.confirm("Do you want to apply the correction?"):
        corr = mean_grayscale_evolution[step_index] - mean_grayscale_evolution[step_index + 1]
        grayscales_evolution[step_index + 1:, :] += corr

    plt.close('all')

    return grayscales_evolution

