import click
import cv2

from src.images.circles import plot_detected_circles, get_circles

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


def check_circles_position(fi, param1, param2, min_distance, crop_values=None):
    img = cv2.imread(fi)

    if crop_values is not None:
        img = img[crop_values[1]:crop_values[3], crop_values[0]:crop_values[2]]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray, 5)

    circles = get_circles(img, param1=param1, param2=param2, min_dist=min_distance)

    plot_detected_circles(img, circles)

    if click.confirm("Are the circles in the correct position?", abort=True):
        cv2.destroyAllWindows()

        return circles
