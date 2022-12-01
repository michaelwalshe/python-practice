def josephus(items,k):
    #your code here
    k -= 1
    pos = k % len(items) if len(items) > 0 else k
    res = []
    while len(items) > 1:
        res.append(items.pop(pos))
        pos = (pos + k) % len(items)
    res.extend(items)
    return res