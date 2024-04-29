# This file is for utility functions used in multiple other files.
# It prevents circular dependencies.

from typing import Union, List, Tuple

# call needs to be paired with some other message to explain the extra options.
# extra_options maybe will be changed to a list to make it easier


def get_selection(num_choices: int, type_of_choice: str,
                  extra_options: set = set()) -> Union[int, str]:
    msg = f"Please select an option from 1-{num_choices} to choose "
    msg += f"{type_of_choice}.\n"
    if extra_options:
        msg += f"You may also select an option from {extra_options} "
        msg += ",\n"
    index = input(msg)
    # explain(extra_options)
    extra_options = {word.lower() for word in extra_options}
    valid_input = {str(num) for num in range(1, num_choices+1)}
    valid_input = valid_input.union(extra_options)
    while index not in valid_input:
        print(f"{index} is not a valid choice.")
        index = input(f"Please select an option from 1-{num_choices} to "
                      f"choose a {type_of_choice}.\n"
                      f"You may also select an option from "
                      f"{extra_options}.\n")
        index = index.lower()
    if index in extra_options:
        return index
    else:
        return int(index)-1


def ending_the_fix(string: str) -> str:
    if string.endswith(', The'):
        return 'The ' + string[:-5]
    return string


def print_dict(length: int, num: int, sample_dict: dict) -> str:
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


def fit_to_screen(string:str, separator: str=' ') -> str:
    """
    This returns a string with new lines added so that it fills the screen.
    """
    new_string = ''
    words = string.split(separator)
    lines = []
    while len(words) > 0:
        line, words = generate_line(words, separator)
        lines.append(line)
    return '\n'.join(lines)


def generate_line(words: List[str], separator: str= ' ') -> Tuple[str,List[str]]:
    """
    Generates a line of less than 80 characters and returns line and remaining 
    terms.
    """
    line = ''
    while len(line) < 80 and len(words) > 0:
        line += separator + words.pop(0)
    if len(words) == 0:
        return line.strip(), words
    return remove_last_word(line.strip(), words, separator)

def remove_last_word(line:str, words: List[str], separator: str= ' ') -> Tuple[str,List[str]]:
    line_words = line.split(separator)
    last_word = line_words.pop()
    words.insert(0,last_word)
    return separator.join(line_words), words
