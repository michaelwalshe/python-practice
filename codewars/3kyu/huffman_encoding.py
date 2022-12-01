from collections import Counter


# takes: str; returns: [ (str, int) ] (Strings in return value are single characters)
def frequencies(s):
    return [(k, v) for k, v in Counter(s).items()]


# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs: list[tuple[str, int]], s: str):
    if len(freqs) <= 1:
        return None

    # Convert the frequencies into a huffman tree
    tree = construct_huffman_tree(freqs)

    # Consume binary tree, convert into mapping from chars to bits
    mapping = binary_repr(tree)

    # Conver chars to bits and return
    return "".join(mapping[c] for c in s)


# takes [ [str, int] ], str (with "0" and "1"); returns: str
def decode(freqs, bits):
    if len(freqs) <= 1:
        return None

    # Convert the frequencies into a huffman tree
    tree = construct_huffman_tree(freqs)

    # Consume binary tree, convert into mapping from chars to bits
    mapping = {v: k for k, v in binary_repr(tree).items()}

    s = ""
    c = ""
    bits = list(bits)[::-1]
    while bits:
        c += bits.pop()
        if c in mapping:
            s += mapping[c]
            c = ""

    return s


class Node(object):
    """Basic binary tree implementation"""
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None

    # Include repr for debugging
    def __repr__(self):
        repr = f"{{val: {self.val}, "
        if self.left is None:
            repr += "L: None, "
        if self.right is None:
            repr += "R: None}"
        if self.left is not None:
            repr += f"L: {self.left}, "
        if self.right is not None:
            repr += f"R: {self.right}}}"

        return repr + "}"


def binary_repr(tree):
    """Consume a binary huffman tree, returning a dictionary of values
    to binary representations.

    Given a binary huffman tree of the form:
          .
         / \
        a   .
           / \
           b  c
    Iterates through to each leaf, calculating the binary representation of the path
    to that leaf (0 -> left, 1 -> right), deleting each leaf as it is counted.

    """
    # Get binary value of each leaf of tree
    binary_mapping = {}
    while True:
        rep, val = _binary_repr(tree)
        if val is not None:
            binary_mapping[val] = rep
        if not is_values_in_tree(tree):
            break

    return binary_mapping


def is_values_in_tree(tree):
    if tree.val is not None:
        return True

    if tree.left is not None:
        if tree.left.val is not None:
            left = True
        else:
            left = is_values_in_tree(tree.left)
    else:
        left = False
    if tree.right is not None:
        if tree.right.val is not None:
            right = True
        else:
            right = is_values_in_tree(tree.right)
    else:
        right = False

    return right or left


def _binary_repr(tree, rep=""):
    """Inner function for binary_repr

    Calculates binary representation of a single leaf, and deletes.
    """
    val = None

    if tree.left is not None:
        if not is_values_in_tree(tree.left):
            # If there are no values on the branch, delete
            tree.left = None
        elif tree.left.val is not None:
            # If next value on branch is leaf, add to binary rep,
            # get the letter value, and delete leaf
            rep += "0"
            val = tree.left.val
            tree.left = None
            return rep, val
        else:
            # If next value is branch, add to rep and recurse
            rep += "0"
            rep, val = _binary_repr(tree.left, rep)
    elif tree.right is not None:
        if not is_values_in_tree(tree.right):
            tree.right = None
        elif tree.right.val is not None:
            # If next value on branch is leaf, add to binary rep,
            # get the letter value, and delete leaf
            rep += "1"
            val = tree.right.val
            tree.right = None
            return rep, val
        else:
            # If next value is branch, add to rep and recurse
            rep += "1"
            rep, val = _binary_repr(tree.right, rep)
    else:
        # Else this is a leaf
        val = tree.val
        return rep, val

    return rep, val


def construct_huffman_tree(freqs):
    """Given a list of value counts, constructs a tree where the most
    frequently used letters are closer to the root

    """
    # Convert (value, freq) tuples into (Node(value), freq) tuples for tree
    freqs = [(Node(f[0]), f[1]) for f in freqs]

    while len(freqs) > 1:
        # TODO: Only sort once?
        freqs = sorted(freqs, key=lambda x: x[1], reverse=True)

        # Get lowest two frequencies
        f0 = freqs.pop()
        f1 = freqs.pop()

        # Construct new frequency node from two lowest
        frequency = f0[1] + f1[1]
        node = Node()
        # To pass tests need to add the nodes back in alphabetical order
        fs = [f0[0], f1[0]]
        if isinstance(f0[0].val, str) and isinstance(f1[0].val, str):
            node.left = min(fs, key=lambda x: x.val)
            node.right = max(fs, key=lambda x: x.val)
        else:
            node.left = f1[0]
            node.right = f0[0]

        freqs.append((node, frequency))
    return freqs[0][0]

test = "aabbbccccddddd"

fs = frequencies(test)

tree = construct_huffman_tree(fs)

binary_repr(tree)
# encode(fs, test)