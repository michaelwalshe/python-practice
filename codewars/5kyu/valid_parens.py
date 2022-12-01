def valid_parentheses(string):
    #your code here
    paren = 0
    for char in string:
        if char == "(":
            paren += 1
        elif char == ")":
            if paren > 0:
                paren -=1
            else:
                return False
    if paren == 0:
        return True
    else:
        return False