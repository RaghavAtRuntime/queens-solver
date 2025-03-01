import numpy as np

def merge_nearest_lines(lines, image, threshold=50):
    """Merges nearby lines to detect the board grid."""
    horizontal_lines = []
    vertical_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y1 - y2) < 10:  # Horizontal line
            horizontal_lines.append(y1)
        elif abs(x1 - x2) < 10:  # Vertical line
            vertical_lines.append(x1)

    horizontal_lines = sorted(set(horizontal_lines))
    vertical_lines = sorted(set(vertical_lines))

    def merge_lines(line_positions, threshold):
        merged_lines = []
        current_line = line_positions[0]

        for line in line_positions[1:]:
            if line - current_line <= threshold:
                continue
            else:
                merged_lines.append(current_line)
                current_line = line

        merged_lines.append(current_line)
        return merged_lines

    merged_horizontal_lines = merge_lines(horizontal_lines, threshold)
    merged_vertical_lines = merge_lines(vertical_lines, threshold)

    return image, merged_horizontal_lines, merged_vertical_lines
