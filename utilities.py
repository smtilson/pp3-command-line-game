# This file is for utility functions used in multiple other files.
# It prevents circular dependencies.

from typing import Union

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
