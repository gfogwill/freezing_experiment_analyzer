import click
import cv2
import numpy as np

from matplotlib import pyplot as plt


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

