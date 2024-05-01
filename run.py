# Main file. Contains functions that run the actual game.
from game_pieces import Game, Task, Adventure, OUTCOMES
from db_utilities import GameSelection, record
from utilities import pause, get_selection, print_dict, fit_to_screen

OTHER_MOVES = {'pass': 'Pass to lose a die and reroll the rest.', 'item': 'Go'
               ' to Item selection menu.'}


def report_options(game: 'Game', adventure: 'Adventure') -> None:
    print(game.dice_pool)
    for index, task in enumerate(adventure):
        print(f"Task {index+1} = {str(task)}")


def report_dice_n_task(game: 'Game', task: 'Task') -> None:
    print(game.dice_pool)
    print(f"Remaining: {str(task)}")


def use_item_procedure(game: 'Game') -> 'Game':
    items = game.investigator.items
    if len(items) == 0:
        print("You have no more items to use.\n")
        return game
    for index, item in enumerate(items):
        white_space = item.white_space+(3-len(str(index+1)))*' '
        print(f"{index+1}. {item.name}: {white_space}{item.effect}")
    index = get_selection(len(items), 'an item to use.', {'none': "Do not use"
                          " an Item"})
    if index == 'none':
        return game
    item = items[index]
    item.use(game)
    print(fit_to_screen(f'{game.investigator.name} used the {item.name} to '
          f'{item.effect.lower()}.\n'))
    return game


def assign_die_to_task(game: 'Game', task: 'Task') -> tuple['Game', 'Task']:
    """
    Assigns single die from dice pool to task. Gets index of die from user and
    assigns it, if possible. Allows for pass and item use. Returns game state
    and task.
    """
    report_dice_n_task(game, task)
    index = get_selection(game.num_dice, "a die to assign to this task",
                          OTHER_MOVES)
    if index == "pass":
        game.pass_move()
    elif index == "item":
        game = use_item_procedure(game)
    else:
        die = game.dice_pool[index]
        if die in task:
            task.assign_die(die)
            game.dice_pool.pop(index)
            pause()
        else:
            print(f"{str(die)} is not a valid choice for {task}.")
    return game, task


def attempt_task(game: 'Game', task: 'Task') -> tuple['Game', 'Task']:
    '''
    Attempts task by calling assign_die until dice_pool is empty or the task
    is complete. Handles penalty aspect of task. Returns  game state and task.
    '''
    task.suffer_penalty(game.investigator)
    while not task.complete and game.num_dice > 0:
        game, task = assign_die_to_task(game, task)
    if task.complete:
        print('You have completed this task!')
        game.dice_pool.roll()
    else:
        print("You are out of dice.")
    return game, task


def attempt_adventure(game: 'Game',
                      adventure: 'Adventure') -> tuple[dict[str, int],
                                                       'Adventure']:
    """
    Attempts adventure card by calling attempt_task until adventure is complete
    or dice pool is empty. Returns adventure and reward or penalty. Allows for
    pass or item use.
    """
    game.dice_pool.roll()
    while not adventure.complete and game.num_dice > 0:
        report_options(game, adventure)
        print()
        index = get_selection(len(adventure.tasks), "a task to attempt",
                              OTHER_MOVES)
        if index == 'pass':
            game.pass_move()
        elif index == "item":
            game = use_item_procedure(game)
        else:
            task = adventure[index]
            pause()
            if task.valid(game.dice_pool):
                game, task = attempt_task(game, task)
            elif task.complete:
                print('This task is already complete.')
            else:
                print("Your roll doesn't have any symbols for that task.")
    outcome = None
    if adventure.complete:
        print(f"You have completed {adventure.name}!")
        print(f"You receive {print_dict(12, 3, adventure.reward)}")
        outcome = adventure.reward
    elif game.num_dice == 0:
        print(f"You have failed, you suffer the penalty of "
              f"{print_dict(43, 2, adventure.penalty)}.")
        outcome = adventure.penalty
    return outcome, adventure


def apply_outcomes(outcomes, game: 'Game') -> None:
    """
    Applies Reward or Penalty to game state.
    """
    for key, value in outcomes.items():
        OUTCOMES[key](value, game)


def introduction() -> None:
    """
    Displays instructions. Either short summary or more details.
    """
    basic_idea1 = 'Welcome to "Chtulu Schmtulu." As you explore a museum, try'\
        " to collect Elder Signs before the Great Old One is Summoned or you "\
        "perish."
    tldr = "TL;DR: Go on Adventures, match dice to complete tasks. Use items "\
        "to aid in the completion of tasks. Collect enough Elder Signs before"\
        " the Great Old One gains too much Doom."
    adventures = "Complete Adventures by completing all of their tasks. "\
        "Complete a task by matching your dice with the symbols the task "\
        "requires (for example, 5 Investigate requires dice showing "\
        "Investigate whose numbers sum to 5). Pass to lose a die and reroll "\
        "the rest of your dice. Use an Item to gain a die or get a free "\
        "reroll. If you run out of dice, you fail the adventure and suffer a "\
        "Penalty. Get a Reward for completing an the Adventure. Every 3 "\
        "turns, Doom increases. Too much Doom, you lose. 0 Health or 0 "\
        "Sanity, then you lose. Enough Elder Signs (from completing "\
        "Adventures) and you win."
    dice = "Here are the dice that are in the game:"\
        "\nGreen =  1 Investigate, 2 Investigate, 3 Investigate, "\
        "\n         1 Lore, 1 Skulls, 1 Tentacles"\
        "\nYellow = 1 Investigate, 2 Investigate, 3 Investigate, 4 "\
        "Investigate,"\
        "\n         1 Lore, 1 Skulls"\
        "\nRed =    2 Investigate, 3 Investigate, 4 Investigate,"\
        "\n         1 Lore, 1 Skulls, 1 Wild"\
        "\nSpell =  All 1 Wild\n"
    dice += fit_to_screen("When you lose a die, you first lose Greens, then "
                          "Yellows, then Reds, and then Spells. At the end of "
                          "each turn, your dice pool is reset to 6 Green "
                          "dice.")
    more_help = "If you have further questions, please see the ReadMe for "\
        "this project at https://github.com/smtilson/pp3-command-line-game/, "\
        "it contains more details and examples."
    print(fit_to_screen(basic_idea1))
    print()
    print(fit_to_screen(tldr))
    yes_no = {'Y': "I would like to hear more details about the game.",
              'N': "Let's go already!"}
    more_info = get_selection(0, '', yes_no)
    if more_info == 'y':
        print()
        for msg in [adventures, more_help]:
            print(fit_to_screen(msg))
        yes_no = {'Y': "I would like to hear about the dice in the game.",
                  'N': "Let's go already!"}
        dice_info = get_selection(0, '', yes_no)
        if dice_info == 'y':
            print(dice)
    print("Alright! Let's get started. That Great Old One isn't going to "
          "banish itself.")


def start_game(start_time: int = 0) -> 'Game':
    """
    Initializes game state by loading data. User selects aspects of game state.
    Constructs game object. Returns game state.
    """
    print()
    name = input('Please enter your name.\n')
    while name.strip() == '':
        name = input('Please enter something other than blank space.\n')
    game_data = GameSelection()
    great_old_one = game_data.select_great_old_one()
    print('\n' + fit_to_screen(f"You have selected {great_old_one.name}."))
    print(fit_to_screen(f"Good luck getting {great_old_one.elder_signs} Elder"
                        f" Signs before they collect {great_old_one.doom} "
                        "Doom!" + "\n"))
    pause()
    investigator = game_data.select_investigator()
    print('\n' + fit_to_screen(f"You have selected {investigator.name}, "
                               f"{investigator.profession}."))
    pause()
    game = Game(name, investigator, great_old_one, game_data.adventure_deck,
                game_data.item_deck)
    print(great_old_one)
    print(investigator)
    pause()
    return game


def main_gameplay_loop(game) -> None:
    """
    Main game play loop: attempts adventure cards, applies results, ends turn,
    checks end_condition. Repeats if end condition hasn't been met. Prints
    results when end condition is met and records results to spreadsheet.
    """
    while not game.end_condition:
        adventure = game.adventure_deck.pop(0)
        # print("card selected")
        print(adventure)
        outcomes, adventure = attempt_adventure(game, adventure)
        game.discard_adventure(adventure)
        # print(f"{outcomes} received from card")
        apply_outcomes(outcomes, game)
        pause()
        print("End of turn.")
        game.end_turn()
    # these messages could be refactored into a dict maybe?
    # or a method of the game object, like a property?
    if game.end_condition == "Banished":
        print(fit_to_screen(f"Congratulations! {game.investigator.name} has "
                            f"defeated {game.great_old_one.name} and "
                            "successfully banished them to the dimension from "
                            "which they came."))
    elif game.end_condition == "Died":
        print(fit_to_screen(f"Oh no! {game.investigator.name} has been "
                            "defeated. Now nothing stands in the way of "
                            f"{game.great_old_one.name}."))
    elif game.end_condition == "Summoned":
        print(fit_to_screen(f"{game.investigator.name} was unable to prevent "
                            f"the inevitable. {game.great_old_one.name} has "
                            "been summoned. The end of humanity is at hand."))
    record(game)


def main():
    introduction()
    game = start_game()
    main_gameplay_loop(game)


if __name__ == "__main__":
    main()
