from pathlib import Path
import sys
import turtle

import cv2


IMAGE_PATH = Path(__file__).resolve().with_name("mataji.jpg")
TARGET_WIDTH = 750
THRESHOLD = 180
MIN_CONTOUR_AREA = 4


def contour_depth(index, hierarchy):
    """Return the number of parent contours enclosing this contour."""
    depth = 0
    parent = hierarchy[index][3]
    while parent != -1:
        depth += 1
        parent = hierarchy[parent][3]
    return depth


def to_turtle_coords(x, y, width, height):
    return x - width / 2, height / 2 - y


def draw_contour(pen, contour, fill_color, width, height):
    first_point = contour[0][0]
    pen.penup()
    pen.goto(*to_turtle_coords(first_point[0], first_point[1], width, height))
    pen.pendown()
    pen.color(fill_color, fill_color)
    pen.begin_fill()

    step = 2 if len(contour) > 80 else 1
    for point in contour[1::step]:
        pen.goto(*to_turtle_coords(point[0][0], point[0][1], width, height))

    pen.goto(*to_turtle_coords(first_point[0], first_point[1], width, height))
    pen.end_fill()


def main():
    image = cv2.imread(str(IMAGE_PATH), cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(
            f"Error: Could not read '{IMAGE_PATH.name}'. "
            "Place a readable mataji.jpg beside mataji.py and try again.",
            file=sys.stderr,
        )
        return 1

    height, original_width = image.shape
    target_height = max(1, round(TARGET_WIDTH * height / original_width))
    resized = cv2.resize(
        image,
        (TARGET_WIDTH, target_height),
        interpolation=cv2.INTER_AREA,
    )
    _, binary = cv2.threshold(resized, THRESHOLD, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )

    if hierarchy is None or not contours:
        print(
            "Error: No contours were found. Check that mataji.jpg contains "
            "visible artwork with sufficient contrast.",
            file=sys.stderr,
        )
        return 1

    hierarchy = hierarchy[0]
    drawable_contours = [
        (contour_depth(index, hierarchy), contour)
        for index, contour in enumerate(contours)
        if cv2.contourArea(contour) >= MIN_CONTOUR_AREA
    ]
    if not drawable_contours:
        print(
            "Error: No contours large enough to draw were found in mataji.jpg.",
            file=sys.stderr,
        )
        return 1

    screen = turtle.Screen()
    screen.setup(width=TARGET_WIDTH + 60, height=target_height + 60)
    screen.title("Live Drawing - Maa Durga and Lion")
    screen.bgcolor("white")
    screen.tracer(5, 0)

    pen = turtle.Turtle()
    pen.speed(0)
    pen.pensize(1)
    pen.shape("classic")

    print("Drawing in progress... Watch the cursor trace the contours.")
    for depth, contour in sorted(drawable_contours, key=lambda item: item[0]):
        # Each child contour reverses its parent's fill: white creates cutouts.
        fill_color = "black" if depth % 2 == 0 else "white"
        draw_contour(pen, contour, fill_color, TARGET_WIDTH, target_height)

    pen.hideturtle()
    screen.update()
    print("Drawing complete. Close the Turtle window to exit.")
    screen.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())