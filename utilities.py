# This file is for utility functions used in multiple other files.
# It prevents circular dependencies.

from typing import Union

# call needs to be paired with some other message to explain the extra options.
# extra_options maybe will be changed to a list to make it easier


def get_selection(num_choices: int, type_of_choice: str,
                  extra_options: dict[str, str] = {}) -> Union[int, str]:
    """
    Gets choice from user. Continues to ask until valid input is given.
    extra_options is a dict of key, value pairs where the key is the name of
    the option and the value is the description of the option.
    """
    msg = ''
    optional = ''
    if num_choices:
        msg += f"Please select an option from 1-{num_choices} to "\
               f"choose a {type_of_choice}.\n\n"
        optional = ' also'
    if extra_options.keys():
        msg += f"You may{optional} select an option from: \n"\
               f"{str(list_options(extra_options))}"
    index = input(msg)
    valid_input = {str(num) for num in range(1, num_choices+1)}
    options = {key.lower() for key in extra_options.keys()}
    valid_input = valid_input.union(options)
    while index not in valid_input:
        print(f"{index} is not a valid choice.")
        index = input(msg)
        index = index.lower()
    if index in options:
        return index
    else:
        return int(index)-1


def list_options(options: dict) -> str:
    """
    Displays options for get_selection.
    """
    string = ''
    for key, value in options.items():
        string += fit_to_screen(f"{key.capitalize()}:   {value}")+'\n'
    return string


def ending_the_fix(string: str) -> str:
    """
    Moves 'The' from end of string to beginning and removes comma.
    """
    if string.endswith(', The'):
        return 'The ' + string[:-5]
    return string


def print_dict(length: int, num: int, sample_dict: dict[str, str]) -> str:
    """
    Displays dictionaries with key value pairs on separate lines. length
    is how much white space to indent by. num is how many terms to print
    before a new line.
    """
    string = ''
    count = 0
    for key, value in sample_dict.items():
        if count == num:
            count = 0
            # new line with proper alignment
            string = string[:-2]
            string += '\n' + length*' '
        string += f"{value} {key}, "
        count += 1
    return string[:-2]


def fit_to_screen(string: str, separator: str = ' ') -> str:
    """
    Returns a string with new lines added so that no line is longer than 79
    characters the screen.
    """
    words = string.split(separator)
    lines = []
    while len(words) > 0:
        line, words = generate_line(words, separator)
        lines.append(line)
    return '\n'.join(lines)


def generate_line(words: list[str],
                  separator: str = ' ') -> tuple[str, list[str]]:
    """
    Generates a line of less than 80 characters. Returns line and remaining
    terms.
    """
    line = ''
    while len(line) < 80 and len(words) > 0:
        line += separator + words.pop(0)
    if len(words) == 0:
        return line[len(separator):], words
    return remove_last_word(line.strip(), words, separator)


def remove_last_word(line: str, words: list[str],
                     separator: str = ' ') -> tuple[str, list[str]]:
    """
    Removes last word of line and adds it back to the beginning of the words
    list. Used in the above.
    """
    line_words = line.split(separator)
    last_word = line_words.pop()
    words.insert(0, last_word)
    return separator.join(line_words), words


def norm(string: str) -> str:
    """
    Normalizes strings to make them lowercase and get rid of plurals."
    """
    if string.endswith('s'):
        string = string[:-1]
    return string.lower()


def pause() -> None:
    """
    Pause function to break up game flow.
    """
    input("\n                     Hit enter to continue.\n")
