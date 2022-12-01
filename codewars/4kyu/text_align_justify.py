def pad(line, width):
    # Initialise output string
    padded_line = line[0]
    if len(line) != 1:
        # How long are all the words we have? No spaces
        word_length = sum(len(word) for word in line)
        # How many total spaces will we need
        total_spaces = width - word_length
        # Get the regular length of the spaces
        space_length = total_spaces // (len(line) - 1)
        # How many extra spaces needed
        if len(line) > 2:
            space_remaining = total_spaces % (len(line) - 1)
        else:
            space_length = total_spaces
            space_remaining = 0
        for word in line[1:]:
            # Add the base padding
            padded_line += " " * space_length
            # If we've got extra spaces then add one and remove 1 from counter
            if space_remaining != 0:
                padded_line += " "
                space_remaining -= 1
            padded_line += word

    return padded_line


def justify(text, width):
    output = []
    line = []
    words = text.split(' ')
    for i, word in enumerate(words):
        # If this isn't the last word
        if i != len(words) - 1:
            # Check if we can add more single spaced words
            if len(" ".join(line + [word])) <= width:
                line.append(word)
            # If we can't add another word, then pad the current line]
            # and restart with this word
            else:
                line_str = pad(line, width)
                output.append(line_str)
                line = [word]
        else:
            # If we are on the last word, then add it if you can and append to output
            if len(" ".join(line + [word])) <= width:
                line.append(word)
                output.append(" ".join(line))
            # If you can't add it, then add a new line
            else:
                line_str = pad(line, width)
                output.append(line_str)
                output.append(word)

    return "\n".join(output)
