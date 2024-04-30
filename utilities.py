# This file is for utility functions used in multiple other files.
# It prevents circular dependencies.

from typing import Union, List, Tuple, Dict

# call needs to be paired with some other message to explain the extra options.
# extra_options maybe will be changed to a list to make it easier


def get_selection(num_choices: int, type_of_choice: str,
                  extra_options: dict = {}) -> Union[int, str]:
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
    string = ''
    for key, value in options.items():
        string += fit_to_screen(f"{key.capitalize()}:   {value}")+'\n'
    return string


def ending_the_fix(string: str) -> str:
    if string.endswith(', The'):
        return 'The ' + string[:-5]
    return string


def print_dict(length: int, num: int, sample_dict: dict[str, str]) -> str:
    """
    Prints simple dictionaries with key value pairs on separate lines. length
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
    This returns a string with new lines added so that it fills the screen.
    """
    words = string.split(separator)
    lines = []
    while len(words) > 0:
        line, words = generate_line(words, separator)
        lines.append(line)
    return '\n'.join(lines)


def generate_line(words: List[str],
                  separator: str = ' ') -> Tuple[str, List[str]]:
    """
    Generates a line of less than 80 characters and returns line and remaining
    terms.
    """
    line = ''
    while len(line) < 80 and len(words) > 0:
        line += separator + words.pop(0)
    if len(words) == 0:
        return line[len(separator):], words
    return remove_last_word(line.strip(), words, separator)


def remove_last_word(line: str, words: List[str],
                     separator: str = ' ') -> Tuple[str, List[str]]:
    line_words = line.split(separator)
    last_word = line_words.pop()
    words.insert(0, last_word)
    return separator.join(line_words), words


def norm(string: str) -> str:
    if string.endswith('s'):
        string = string[:-1]
    return string.lower()


def pause() -> None:
    input("\n                     Hit enter to continue.\n")
