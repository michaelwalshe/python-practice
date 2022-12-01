def solution(string,markers):
    new_string = []
    for line in string.split('\n'):
        new_line = []
        for letter in line:
            if not letter in markers:
                new_line.append(letter)
            else:
                break
        new_string.append((''.join(new_line)).rstrip())
    return '\n'.join(new_string)