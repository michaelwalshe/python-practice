# Define class point to ensure we set all internal values as int
class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


def expand_code(code):
    """Expand an RS1 code into the full instruction set"""
    code = list(code)

    new_code = ""
    while code:
        c = code.pop(0)
        val = ""
        while code and code[0].isnumeric():
            val += code.pop(0)
        mult = int(val) if val else 1
        new_code += c * mult

    return new_code


def execute(code):
    # Expand repeated instructions
    code = expand_code(code)

    # Initially start at 0, 0 heading right
    positions = [Point(0, 0)]
    dxdy = 1 + 0j

    # Get all positions robot occupies
    for c in code:
        if c == "F":
            # If forward then add dxdy to last position
            lastpos = positions[-1]
            newpos = Point(lastpos.x + dxdy.real, lastpos.y + dxdy.imag)
            positions.append(newpos)
        else:
            # If L or R then rotate dxdy
            rotation = -1j if c == "L" else +1j
            dxdy *= rotation

    # Offset all positions so x and y start at 0
    minx = abs(min(positions, key=lambda p: p.x).x)
    miny = abs(min(positions, key=lambda p: p.y).y)
    maxx = max(positions, key=lambda p: p.x).x + minx
    maxy = max(positions, key=lambda p: p.y).y + miny
    positions = [Point(p.x + minx, p.y + miny) for p in positions]

    # Create grid and draw all points on
    grid = [[" " for _ in range(maxx + 1)] for _ in range(maxy + 1)]
    for p in positions:
        grid[p.y][p.x] = "*"

    # Join list grid into strings sep by newlines
    return "\r\n".join("".join(r) for r in grid)
