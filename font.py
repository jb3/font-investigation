import matplotlib.pyplot as plt

from ttfquery import describe
from ttfquery import glyphquery
import ttfquery.glyph as glyph

import numpy as np
from scipy.interpolate import splprep, splev

import sys


if len(sys.argv) == 1:
    print("usage: python font.py [character]")
    exit(1)

# Open the character given as command line argument
g = glyph.Glyph(sys.argv[1])

# Open our font file
font = describe.openFont("LiberationSans.ttf")

# Get the curves on the font, each contour is an "island" on the glyph
# For example, i has the main stem and the dot on top, which are separate
# contours.
contours = g.calculateContours(font)

for contour in contours:
    x = []
    y = []
    flags = []

    # For each point in the contour add to lists
    for point, flag in contour:
        x.append(point[0])
        y.append(point[1])
        flags.append(flag)

    # Plot an overall dot-to-dot of the points
    plt.plot(x, y, '-o')

    # Used for curve calculation
    temp_points = []

    # Put all point data into one list
    points = list(zip(x, y, flags))

    for i, (x, y, flag) in enumerate(points):
        if flag == 0 and len(temp_points) == 0:
            # First point on a curve
            temp_points = [points[i-1], points[i]]
            plt.scatter(x, y, color='black' if flag
                        == 0 else 'red', zorder=10)

        elif flag == 0:
            # Point on an existing curve
            temp_points.append(points[i])

            plt.scatter(x, y, color='black' if flag
                        == 0 else 'red', zorder=10)
        else:
            if len(temp_points) != 0:
                # End of a curve
                if points[i] not in temp_points:
                    temp_points.append(points[i])

                # Create a list of x and y
                x = [p[0] for p in temp_points]
                y = [p[1] for p in temp_points]

                # Prepare the spline:
                #   [x, y] - Our points on the spline
                #   k=2 - Specify it is a quadratic spline
                #   s=7 - Set smoothing to 7
                tck, u = splprep([x, y], k=2, s=0)

                # Increase the amount of points we are provided with to 100
                u_new = np.linspace(u.min(), u.max(), 1000)

                # Evaluate the spline
                x_new, y_new = splev(u_new, tck)

                # Plot the spline in black on the graph
                plt.scatter(x_new, y_new, color="black", zorder=0)

                # Reset temp_points for the next spline
                temp_points = []

                plt.scatter(x, y, color='black' if flag
                            == 0 else 'red', zorder=10)

            else:
                # Straight line
                plt.scatter(x, y, color='black' if flag
                            == 0 else 'red', zorder=10)

# Display the glyph in pyplot
plt.show()
