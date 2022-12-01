import re


# Define class point to ensure we set all internal values as int
class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


def expand_code(code):
    """Expand an RS2 code into the full instruction set"""
    # Code to find only the innermost levels of parenthese
    paren_rexp = re.compile(r"\(([^\(^\)]+)\)(\d*)")

    # Function to calc the inside of parens, return expression with these subbed
    def repl(m):
        g = m.groups()
        mult = 1 if g[1] == "" else int(g[1])
        return g[0] * mult

    # While we still have some parentheses
    while re.search(paren_rexp, code):
        # Replace inside of innermost parens with result of expansion
        code = re.sub(paren_rexp, repl, code)

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
    # Compile functions
    func_prx = re.compile(r"p(\d+)([^q]+)q")
    fcts = {}
    for n, func in re.findall(func_prx, code):
        name = 'P' + n
        if name in fcts:
            raise SyntaxError
        else:
            fcts['P' + n] = func

    # Expand functions
    code = re.sub(func_prx, "", code)
    n = 0
    while "P" in code:
        n += 1
        func = re.search("P\d+", code).group(0)
        if func not in fcts:
            raise SyntaxError
        else:
            code = re.sub(f"{func}(?!\d)", fcts[func], code)
            code.replace(func, fcts[func])
        if n > 100:
            raise RuntimeError

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

code = "(P999)17p999F3R2F6L3FFFRFq(P999)1024P99973"

print(execute(code))