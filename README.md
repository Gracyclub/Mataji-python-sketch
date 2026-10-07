# 🔱 Maa Durga Live Sketch Animation using Python Turtle

This creative coding project uses Python Turtle and OpenCV to trace contours from the `mataji.jpg` reference image, drawing the artwork progressively with a visible turtle cursor.

## Features

- **Live cursor sketching:** Turtle traces each detected contour in the drawing window.
- **Hierarchical contour tracing:** OpenCV's `RETR_TREE` mode finds outer contours and nested contours.
- **Black silhouettes and white cutouts:** The contour nesting depth determines whether a contour is filled black or white. The appearance depends on the source image and threshold; this raster-to-contour process does not guarantee an exact match to the reference.

## Setup and run

Use Python 3 and install the required package:

```sh
python -m pip install opencv-python numpy
python mataji.py
```

`mataji.jpg` must be in the same directory as `mataji.py`. The script locates the image relative to its own file, so it can be run from another working directory. If the image is missing, unreadable, or contains no usable contours, the script prints an error and exits without opening the Turtle window.
