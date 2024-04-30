from typing import List, Optional, Tuple, Union
# the below import statement should eventually be changed
from game_pieces import Game, Task, Adventure, OUTCOMES
from db_utilities import GameSelection, record
from utilities import pause, get_selection, print_dict, fit_to_screen

OTHER_MOVES = {'pass': 'Pass to lose a die and reroll the rest.', 'item': 'Go'
               ' to Item selection menu.'}


def introduction() -> None:
    basic_idea1 = 'Welcome to "Chtulu Schmtulu." Try to collect Elder Signs '\
        "before the Great Old One is Summoned or you perish."
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
    print("Alright! Let's get started. That Great Old One isn't going to "\
          "banish itself.")


def report_options(game: 'Game', adventure):
    print(game.dice_pool)
    for index, task in enumerate(adventure):
        print(f"Task {index+1} = {str(task)}")


def report_dice_n_task(game, task):
    print(game.dice_pool)
    print(f"Remaining: {str(task)}")


# needs a better name
def use_item_procedure(game: 'Game') -> 'Game':
    items = game.investigator.items
    for index, item in enumerate(items):
        white_space = item.white_space+(3-len(str(index+1)))*' '
        print(f"{index+1}. {item.name}: {white_space}{item.effect}")
    index = get_selection(len(items), 'an item to use.', {'none': "Do not use"
                          " an Item"})
    if index == 'none':
        return game
    item = items[index]
    item.use(game)
    print(f'{game.investigator.name} used the {item.name} to '
          f'{item.effect.lower()}.')
    return game


# I think this should be refactored into two functions, one a method of the
# Task class.
def assign_die_to_task(game: 'Game', task: 'Task'):
    """
    Assigns single die from dice pool to task. Gets index of die from user and
    assigns it, if possible. If a pass is submitted, pass_move is called. This
    pops a die from the dice pool and rerolls the remaining dice.
    """
    report_dice_n_task(game, task)
    # would a get die function be better?, I guess decoupling the dice pool and
    # the task would mean that you wouldn't see what the task is anymore...
    index = get_selection(game.num_dice, "a die to assign to this task",
                          OTHER_MOVES)
    if index == "pass":
        game.pass_move()
        return game, task
    elif index == "item":
        return use_item_procedure(game), task
    die = game.dice_pool[index]
    if die in task:
        task.assign_die(die)
        game.dice_pool.pop(index)
        pause()
    else:
        print(f"{str(die)} is not a valid choice for {task}.")
    return game, task


def assign_dice_to_task(game, task):
    """
    Assigns dice from dice pool to a task until dice_pool is empty or the task
    is complete. Then returns the task and remaining dice.
    """
    game, task = assign_die_to_task(game, task)
    while not task.complete and game.num_dice > 0:
        # should this catch be at the beginning?
        game, task = assign_die_to_task(game, task)
    return game, task


def attempt_task(game, task):
    '''
    Attempts to complete task by assigning dice, doing passing (lose die and
    reroll),and potentially suffering a penalty. Returns investigator and task
    if dice_pool is empty, or task is complete.
    '''
    task.suffer_penalty(game.investigator)
    # game, task = assign_dice_to_task(game, task)
    while not task.complete and game.num_dice > 0:
        game, task = assign_dice_to_task(game, task)
    if task.complete:
        print('You have completed this task!')
        game.dice_pool.roll()
        return game, task
    print("You are out of dice.")
    return game, task


def attempt_adventure(game: 'Game',
                      adventure: 'Adventure') -> Tuple[dict, 'Adventure']:
    game.dice_pool.roll()
    while not adventure.complete and game.num_dice > 0:
        report_options(game, adventure)
        index = get_selection(len(adventure.tasks), "a task to attempt",
                              OTHER_MOVES)
        if index == 'pass':
            game.pass_move()
            continue
        elif index == "item":
            game = use_item_procedure(game)
            continue
        task = adventure[index]
        # should this part of the validation be done elsewhere?
        if task.valid(game.dice_pool):
            game, task = attempt_task(game, task)
            # should I pop the task here if it is complete?
            # selecting the same task gives a free reroll.
        elif task.complete:
            print('This task is already complete.')
            continue
        else:
            print("Your roll doesn't have any symbols for that task.")
            continue
    if adventure.complete:
        print(f"You have completed {adventure.name}!")
        print(f"You receive {print_dict(12, 3, adventure.reward)}")
        return adventure.reward, adventure
    elif game.num_dice == 0:
        print(f"You have failed, you suffer the penalty of "
              f"{print_dict(43, 2, adventure.penalty)}.")
        return adventure.penalty, adventure


def apply_outcomes(outcomes, game: 'Game'):
    for key, value in outcomes.items():
        # print(f"Applying outcome {key}: {value}.")
        OUTCOMES[key](value, game)


def start_game(start_time=0):
    """
    Initializes game state by loading data.
    Selects game state by getting input from user.
    Begins game by dealing task cards and initializing main gameplay loop.
    """
    name = input('Please enter your name.\n')
    while name.strip() == '':
        name = input('Please enter something other than blank space.\n')
    game_data = GameSelection()
    great_old_one = game_data.select_great_old_one()
    print(f"You have selected {great_old_one.name}.")
    print(f"Good luck getting {great_old_one.elder_signs} Elder Signs before "
          f"they collect {great_old_one.doom} Doom!")
    investigator = game_data.select_investigator()
    print(f"You have selected {investigator.name} {investigator.profession}.")
    game = Game(name, investigator, great_old_one, game_data.adventure_deck,
                game_data.item_deck)
    print(great_old_one)
    print(investigator)
    pause()
    return game


def main_gameplay_loop(game) -> None:
    """
    Main gameplay loop which runs the game.
    """
    # this is all meta code essentially
    end_condition = False
    while not end_condition:
        adventure = game.adventure_deck.pop(0)
        # print("card selected")
        print(adventure)
        outcomes, adventure = attempt_adventure(game, adventure)
        game.discard_adventure(adventure)
        # print(f"{outcomes} received from card")
        apply_outcomes(outcomes, game)
        pause()
        print("End of turn.")
        end_condition = game.end_turn()
    # these messages could be refactored into a dict maybe?
    # or a method of the game object, like a property?
    if end_condition == "Banished":
        print(f"Congratulations! {game.investigator.name} has defeated "
              f"{game.great_old_one.name} and successfully banished them to "
              f"the dimension from which they came.")
    elif end_condition == "Died":
        print(f"Oh no! {game.investigator.name} has been defeated. Now nothing"
              f" stands in the way of {game.great_old_one.name}.")
    elif end_condition == "Summoned":
        print(f"{game.investigator.name} was unable to prevent the inevitable."
              f" {game.great_old_one.name} has been summoned. The end of "
              f"humanity is at hand.")
    record(game)


def main():
    introduction()
    game = start_game()
    main_gameplay_loop(game)


if __name__ == "__main__":
    main()
