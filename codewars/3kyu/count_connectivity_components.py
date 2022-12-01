from collections import Counter
from dataclasses import dataclass
import itertools
import re


@dataclass
class Cell:
    x: int
    y: int
    neighbours: tuple[bool, bool, bool, bool]  # (up, down, left, right)


def check_wall(x, y, grid):
    if x < 0 or y < 0 or x > len(grid[0]) or y > len(grid):
        raise ValueError("Checking out of bounds!")
    return grid[y][x] != "W"


def components(grid):
    # Split grid into list of strings with W for all walls and C for
    # cell centre markers
    rows = []
    for r in grid.split("\n"):
        r = r.replace("--", "W").replace("|", "W")
        r = re.sub(r"(\s{2})([\sW+])", r"C\2", r)
        rows.append(r)

    # Count number of cells we should have
    ncols = rows[0].count("+") - 1
    nrows = (len(rows) - 1) // 2

    # Convert each cell into Cell object, with info about whether
    # it has a wall on each side
    cell_grid = []
    for j in range(nrows):
        row = []
        for i in range(ncols):
            i2, j2 = i * 2 + 1, j * 2 + 1
            up = check_wall(i2, j2 - 1, rows)
            down = check_wall(i2, j2 + 1, rows)
            left = check_wall(i2 - 1, j2, rows)
            right = check_wall(i2 + 1, j2, rows)
            row.append(Cell(i, j, (up, down, left, right)))
        cell_grid.append(row)

    # Crawl across joined up cells, adding the size of each to a list
    # when there are no more directions to go in
    to_visit = list(itertools.product(range(ncols), range(nrows)))
    visited = []
    comp_sizes = []
    while to_visit:
        start = to_visit.pop(0)
        queue = [start]
        size = 0
        while queue:
            i, j = queue.pop(0)
            if (i, j) in visited:
                continue
            visited.append((i, j))
            cell = cell_grid[j][i]
            size += 1
            for direction, dxdy in enumerate(((0, -1), (0, 1), (-1, 0), (1, 0))):
                if cell.neighbours[direction]:
                    new_point = (i + dxdy[0], j + dxdy[1])
                    if new_point in visited:
                        continue
                    queue.append((i + dxdy[0], j + dxdy[1]))
        to_visit = [p for p in to_visit if p not in visited]
        comp_sizes.append(size)

    return [(s, n) for s, n in Counter(sorted(comp_sizes, reverse=True)).items()]
