import cv2
import numpy as np
from utils import merge_nearest_lines

class ImageProcessor:
    def process_image(self, image_path):
        """Processes the image to detect the board and regions."""
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Failed to load the image.")

        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect edges
        edges = self.detect_edges(gray_image)

        # Detect lines
        lines = self.detect_lines(edges)

        # Merge lines and detect the board
        _, merged_horizontal_lines, merged_vertical_lines = merge_nearest_lines(lines, image)

        # Calculate the board size (NxN)
        n = len(merged_horizontal_lines) - 1

        # Detect regions based on color shades
        board, regions = self.detect_regions(image, merged_horizontal_lines, merged_vertical_lines)

        return board, n, regions

    def detect_edges(self, gray_image, threshold1=50, threshold2=150):
        """Detects edges in the grayscale image."""
        edges = cv2.Canny(gray_image, threshold1, threshold2, apertureSize=3)
        return edges

    def detect_lines(self, edges, threshold=100, min_line_length=100, max_line_gap=10):
        """Detects lines in the edge-detected image."""
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)
        return lines

    def detect_regions(self, image, horizontal_lines, vertical_lines):
        """Detects regions based on color shades by sampling the middle of each cell."""
        n = len(horizontal_lines) - 1
        board = [[None for _ in range(n)] for _ in range(n)]
        regions = {}

        # Iterate through each cell in the grid
        for i in range(n):
            for j in range(n):
                # Define the cell boundaries
                x1 = vertical_lines[j]
                y1 = horizontal_lines[i]
                x2 = vertical_lines[j + 1]
                y2 = horizontal_lines[i + 1]

                # Calculate the middle of the cell
                middle_x = (x1 + x2) // 2
                middle_y = (y1 + y2) // 2

                # Sample the color from the middle of the cell
                middle_color = image[middle_y, middle_x]

                # Assign a region based on the sampled color
                region_id = tuple(map(int, middle_color))
                board[i][j] = region_id

                if region_id not in regions:
                    regions[region_id] = []
                regions[region_id].append((i, j))

        return board, regions
