def do_rail_op(items, rails, rail_op, *args):
    """For given collections of items andof rails, do a given operation
    to each element of the collection and its assigned rail.

    Rails are assigned as the following:

    Collection = abcdefghijklm, number of rails = 3
    Rails:
        1: a   e   i   m
        2:  b d f h j l
        3:   c   g   k
    """
    rail = 0
    going_down = True
    for i, elem in enumerate(items):
        rail_op(elem, rails, rail, *args)

        if i != 0 and i % (len(rails) - 1) == 0:
            going_down = not going_down

        if going_down:
            rail += 1
        else:
            rail -= 1


def encode_rail_fence_cipher(string, n):
    """Encode a string using rail fence cipher

    https://en.wikipedia.org/wiki/Rail_fence_cipher
    """
    # Initally rails are empty lists
    rails = [[] for _ in range(n)]

    # Append an element to its assigned rail
    def append_to_rail(elem, rails, rail):
        rails[rail].append(elem)

    # Assign each element of string to a rail
    do_rail_op(string, rails, append_to_rail)

    # Join each rail internally, then join all rails together
    return "".join("".join(r) for r in rails)


def get_rail_lengths(items, n_rails):
    """Given a collection of items and how many rails there will be, calculate
    how many items will be on each rail"""
    rail_lengths = [0] * n_rails

    def add_to_rail(_, rails, rail):
        rails[rail] += 1

    do_rail_op(items, rail_lengths, add_to_rail)

    return rail_lengths


def decode_rail_fence_cipher(string, n):
    """Decode a string using rail fence cipher

    https://en.wikipedia.org/wiki/Rail_fence_cipher
    """
    rail_fence = list(string)
    rail_lengths = get_rail_lengths(string, n)  # How many items are on each rail

    # Split input string into constituent rails
    rails = []
    for length in rail_lengths:
        rail = rail_fence[0:length]
        rails.append(rail)
        del rail_fence[0:length]

    # Pull elements off rails in order, and append to a given list
    def pop_from_rails(_, rails, rail, output):
        c = rails[rail].pop(0)
        output.append(c)

    decoded = []
    do_rail_op(string, rails, pop_from_rails, decoded)

    return "".join(decoded)
