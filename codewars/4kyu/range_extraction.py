def solution(args):
    # your code here
    output = []
    range = []
    for i, num in enumerate(args):
        if i == 0:
            prev_cond = False
            next_cond = num + 1 == args[i + 1]
        elif i == len(args) - 1:
            prev_cond = num - 1 == args[i - 1]
            next_cond = False
        else:
            prev_cond = num - 1 == args[i - 1]
            next_cond = num + 1 == args[i + 1]

        if prev_cond and next_cond:
            range.append(str(num))
        elif next_cond:
            range = []
            range.append(str(num))
        elif prev_cond:
            range.append(str(num))
            if len(range) > 2:
                output.append(f"{range[0]}-{num}")
                range = []
            else:
                output.extend(range)
        else:
            output.append(str(num))
    return ",".join(output)