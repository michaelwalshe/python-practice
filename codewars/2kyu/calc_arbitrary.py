import re


operators = {
    "*": lambda x, y: x * y,
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "/": lambda x, y: x / y,
}

precedence = {
    "*": 1,
    "+": 0,
    "-": 0,
    "/": 1,
}


def replace_unary(expression):
    """Replace all unary minuses with custom operator"""
    expression = expression.replace(" ", "")
    expr_list = list(expression)

    for i in range(len(expr_list) - 1):
        if i >= 1:
            c_l = expr_list[i - 1]
        else:
            c_l = None
        c = expr_list[i]
        c_r = expr_list[i + 1]

        replace = False
        if c == "-":
            if c_l is None:
                replace = True
            elif c_l in "(+-*/~":
                replace = True

        if replace:
            expr_list[i] = "~"

    return "".join(expr_list)


def calc(expression):
    # Check for unary minus, replace with custom operator: ~
    expr = replace_unary(expression)

    # Parentheses calculation ==================================================
    # RegExp to get the contents of parentheses
    paren_rexp = re.compile(r"(.*)\((?:\(??([^\(]*?))\)(.*)")

    # Function to calc the inside of parens, return expression with these subbed
    def repl(m):
        g = m.groups()
        return g[0] + str(calc(g[-2])) + g[-1]

    # While we still have some parentheses
    while re.search(paren_rexp, expr):
        # Replace inside of parens with result of calculation
        expr = re.sub(paren_rexp, repl, expr)

    # Final unary check if re.sub() added them back in:
    expr = replace_unary(expr)

    # Main loop ================================================================
    # Create stacks for operators and values
    ops = []
    vals = []
    # Unary flag, multiplies value
    unary = 1
    # Track place in string
    i = 0
    while i < len(expr):
        c = expr[i]
        if c == "~":
            # Handle unary operator, don't include in ops
            unary = -unary
        elif c in operators:
            # Check if should do an operation, do we have operators to use and
            # should we do stored operator before the current one?
            while ops and precedence[ops[-1]] >= precedence[c]:
                op = ops.pop()
                v2 = vals.pop()
                v1 = vals.pop()
                vals.append(operators[op](v1, v2))

            ops.append(c)
        # If not in operators, then this is numeric
        else:
            # Find entire value, creep along string getting numbers/dots
            val = ""
            while i < len(expr) and expr[i] in ("0123456789."):
                val += expr[i]
                i += 1
            val = float(val)
            # Correct for misaligned i
            i -= 1

            # Multiply by unary flag - account for e.g. (2*-1)
            vals.append(unary * val)
            unary = 1
        i += 1

    while ops:
        op = ops.pop()
        v2 = vals.pop()
        v1 = vals.pop()
        vals.append(operators[op](v1, v2))

    return vals[-1]