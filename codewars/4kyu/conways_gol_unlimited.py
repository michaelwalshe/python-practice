import numpy as np


def get_neighbours(i, j, cells: np.array):
    """Find the indices of surrounding edges and sum neighbours in
    that section.
    """
    rows, cols = cells.shape
    top = max(i - 1, 0)
    bottom = min(i + 1 + 1, rows)
    left = max(j - 1, 0)
    right = min(j + 1 + 1, cols)

    section = cells[top:bottom, left:right]

    neighbours = section.sum() - cells[i, j]
    return neighbours


def get_generation(cells, generations):
    """Calculate final board of GOL after X generations"""
    print(f"Running with {generations} generation(s) and starting board \n {np.array(cells)}")
    for gen in range(generations):
        # Add border of zeros for new cells
        cells = np.pad(
            np.array(cells), [(1, 1), (1, 1)], mode="constant", constant_values=0
        )
        # Create next generation array
        new_cells = np.zeros_like(cells)
        for pos, cell in np.ndenumerate(cells):
            # Get number of neighbours for each cell
            i, j = pos
            n = get_neighbours(i, j, cells)
            # Does this cell live or die?
            if cell == 0 and n == 3:
                cell = 1
            elif n not in (2, 3):
                cell = 0
            # Update new cell
            new_cells[i, j] = cell
        # Crop to just living cells
        coords = np.argwhere(new_cells)
        x_min, y_min = coords.min(axis=0)
        x_max, y_max = coords.max(axis=0)
        cells = new_cells[x_min : x_max + 1, y_min : y_max + 1]
        print(f"At generation {gen}, board is\n {np.array(cells)}")
    return np.array(cells).tolist()