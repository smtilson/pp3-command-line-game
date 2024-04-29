from typing import List, Optional, Tuple, Union
# the below import statement should eventually be changed
from game_pieces import *
from db_utilities import GameSelection, record
from utilities import get_selection

def pause() -> None:
    input("\n                     Hit enter to continue.\n")


def introduction() -> None:
    basic_idea1 = 'Welcome to "Chtulu Schmtulu," a dice rolling game heavily '\
    "based on Elder Sign\nfrom Fantasy Flight Games. In each game, you "\
    "attempt to Banish a Great Old\nOne before they are Summoned or before "\
    "you are Defeated. After selecting a\nGreat Old One to battle against, "\
    "you will select an Investigator to play as.\nThe Great Old Ones are "\
    "Summoned when they gain enough Doom. They are Banished\nwhen you collect"\
    " enough Elder Signs."
    tldr = "TL;DR: Go to Adventures, assign dice to complete tasks. Collect "\
    "Elder Signs\nbefore you are Defeated or the Great Old One gains enough "\
    "Doom."
    basic_idea2 = "You will collect Elder Signs by completing Adventures. Doom"\
    " is gained when the\nclock strikes midnight (the clock advances after "\
    "each of your turns) as well\nas through game effects. If your "\
    "Investigator has 0 Health or 0 Sanity, then\nyou are defeated. If you "\
    "are defeated or the Great Old One is Summoned, then\nyou have lost. If "\
    "you collect enough Elder Signs to Banish the Great Old One,\nthen you "\
    "have won!"
    adventures1 = "Each turn you will go to a Adventure. To complete a Adventure"\
    " you must complete\neach task at the Adventure. A task is completed by "\
    "assigning matching dice to\nthe task in order to fulfill the "\
    "requirements. Some tasks also have you suffer\na penalty by losing "\
    "Health or Sanity. If none of the symbols on your dice\nmatch a symbol on"\
    " the task, you may do a Pass."
    adventures2 = "A Pass rerolls all of your dice at the cost of forfeiting "\
    "one of them. You\nmay also use an Item (the Item selection menu also "\
    "contains a description of\nwhat each Item does). If you run out of dice,"\
    " you fail the Adventure and suffer\nassociated Penalty. If you complete a"\
    " Adventure, you receive the associated\nReward. Penalties can be losing "\
    "Health or Sanity, or the Great Old One gaining\nadditional Doom. Rewards"\
    " can be gaining an Item, Health, or Sanity."
    dice ="As the game revolves around rolling dice, here are the different "\
    "dice that \nare in the game:\nGreen =  Investigate: 1, Investigate: 2, "\
    "Investigate: 3, \n         Lore: 1, Skulls: 1, Tentacles: 1\nYellow = "\
    "Investigate: 1, Investigate: 2, Investigate: 3, Investigate: 4,\n     "\
    "    Lore: 1, Skulls: 1\nRed =    Investigate: 2, Investigate: 3, "\
    "Investigate: 4,\n         Lore: 1, Skulls: 1, Wild: 1\nSpell =  All "\
    "Wild: 1"
    losing_dice = "When you lose a die by passing, you will lose the earliest"\
    "die in your pool\naccording to the ordering:\n       Green < Yellow < "\
    "Red < Spell"
    difficulty = "Difficulty can be adjusted through the setting of two "\
    "different parameters.\nIncrement sets how much the clock advances after "\
    "each of your turns. The\nstandard setting is 6 hours, so Doom "\
    "accumulates every 4 turns. The second is\nthe starting dice pool. "\
    "Standard (which is quite a challenge) is 6 Green dice."
    items = "Each Investigator begins the game with different starting Items."\
    " Items\ncome in 4 varieties: Common, Unique, Clue, and Spell. Common "\
    "Items will\nusually give you a yellow die, Unique Items will usually "\
    "give you a red die (for\nthat Adventure). Clues allow you to reroll your "\
    "dice without penalty. Spells\nadd a Wild symbol to your dice pool. You "\
    "will also gain Items by\ncompleting Adventures."
    future = "In the future, we would like to implement more of the game, "\
    "such as abilities\nof Investigators as well as Great Old Ones. This is a"\
    " bit of a task though as\neach ability requires a separate function that"\
    " must be implemented which may\ntake effect at different points in game "\
    "play. There are other notable aspects\nof game play which we would also "\
    "like to implement in the future, such as\nfocusing, multiplayer mode, "\
    "and Monsters."
    more_help = "If you have further questions, please see the ReadMe for "\
    "this project at, it\ncontains examples of game play. It may also be "\
    'beneficial to view game play\nor a "how to play" video for Elder Sign on'\
    " YouTube."
    more_details = [basic_idea2, adventures1, adventures2, dice, losing_dice, 
                    difficulty, items, future, more_help]
    print(basic_idea1)
    pause()
    print(tldr)
    more_info = input("Would you like more details about the game? Y/n\n")
    if more_info.lower() == 'y' or more_info.lower() =='yes':
        print()
        for msg in more_details:
            print(msg)
            pause()

    else:
        print("Alright! Let's get started. That Great Old One isn't going to "\
              "banish itself.")


# I feel like this can be combined with the other report function to be more 
# streamlined?
def report_options(investigator, adventure):
    print(investigator.dice_pool)
    for index, task in enumerate(adventure):
        print(f"{index+1} = {str(task)}")


# this should be made to be nicer
def report_dice_n_task(investigator, task):
    print(investigator.dice_pool)
    print(task)    


# needs a better name
def use_item_procedure(investigator: 'Investigator') -> 'Investigator':
    items = investigator.items
    for index, item in enumerate(items):
        white_space = item.white_space+(3-len(str(index+1)))*' '
        print(f"{index+1}. {item.name}: {white_space}{item.effect}")
    index = get_selection(len(items), 'an item to use.', {'none'})
    if index == 'none':
        return investigator
    item = items[index]
    item.use(investigator)
    print(f'{investigator.name} used the {item.name} to '\
          f'{item.effect.lower()}.')
    return investigator


# I think this should be refactored into two functions, 
# one a method of the Task class.
def assign_die_to_task(investigator, task): #'DicePool','Task':
    """
    Assigns single die from dice pool to task. Gets index of die from user and 
    assigns it, if possible. If a pass is submitted, pass_move is called. This 
    pops a die from the dice pool and rerolls the remaining dice.
    """
    report_dice_n_task(investigator, task)
    # would a get die function be better?, I guess decoupling the dice pool and
    # the task would mean that you wouldn't see what the task is anymore...
    index = get_selection(len(investigator),"a die to assign to this task", 
                          {'pass','item'})
    if index == "pass":
        investigator.pass_move()
        return investigator, task
    elif index == "item":
        return use_item_procedure(investigator), task
    die = investigator.dice_pool[index]
    if die in task:
        task.assign_die(die)
        investigator.dice_pool.pop(index)
        pause()
    else:
        print(f"{str(die)} is not a valid choice for {task}.")
    return investigator, task


def assign_dice_to_task(investigator, task):
    """
    Assigns dice from dice pool to a task until dice_pool is empty or the task
    is complete. Then returns the task and remaining dice.
    """
    investigator, task = assign_die_to_task(investigator, task)
    while not task.complete and len(investigator) > 0:
        # should this catch be at the beginning?
        investigator, task = assign_die_to_task(investigator, task)
    return investigator, task
        
def attempt_task(investigator, task):
    '''
    Attempts to complete task by assigning dice, doing passing (lose die and reroll), 
    and potentially suffering a penalty. Returns investigator and task if dice_pool is 
    empty, or task is complete.
    '''
    task.suffer_penalty(investigator)
    investigator, task = assign_dice_to_task(investigator, task)
    while not task.complete and len(investigator) > 0:
        investigator, task = assign_dice_to_task(investigator, task)
    if task.complete:
        print('You have completed this task!')
        investigator.roll()
        return investigator, task
    print("You are out of dice.")
    return investigator, task

def attempt_adventure(investigator:'Investigator',adventure:'Adventure') -> str:
    # do we roll here? I think so.
    investigator.roll()
    #print(dice_pool)
    #for task in adventure:
     #   print(task)
    #I feel like I don't really need these conditions here
    while not adventure.complete and len(investigator) > 0:
        report_options(investigator, adventure)
        index = get_selection(len(adventure.tasks),"a task to attempt",{'pass','item'})
        # Is this technically in the spirit of the game?
        if index == 'pass':
            investigator.pass_move()
            continue
        elif index == "item":
            investigator = use_item_procedure(investigator)
            continue
        task = adventure[index]
        # should this part of the validation be done elsewhere?
        if task.valid(investigator.dice_pool):
            investigator, task = attempt_task(investigator, task)
            # should I pop the task here if it is complete?
            # selecting the same task gives a free reroll.
        else:
            print("Your roll doesn't have any symbols for that task.")
            continue
    if adventure.complete:
            print(f"You have completed {adventure.name}!")
            print(f"You receive {adventure.reward}")
            return adventure.reward, adventure
    elif len(investigator) == 0:
        print(f"You have failed, you suffer the penalty of {adventure.penalty}.")
        return adventure.penalty, adventure
        

def apply_outcomes(outcomes, game):
    for key, value in outcomes.items():
        print(f"Applying outcome {key}: {value}.")
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
    investigator = game_data.select_investigator()
    #set difficulty function.
    increment = 12
    game = Game(name,investigator,great_old_one,game_data.adventure_deck,
                game_data.item_deck, increment)
    #print(game)
    print(great_old_one)
    print(investigator)
    pause()
    # main_gameplay_loop(game)
    return game

def select_adventure(game):
    return game.current_adventures.pop(0)

def test_gameplay():
    game_data = GameSelection()
    great_old_one = game_data.great_old_ones[0]
    investigator = game_data.investigators[0]
    start_time = 0
    game = Game(investigator,great_old_one,start_time,game_data.adventure_deck,
                game_data.item_deck)
    main_gameplay_loop(game)

def main_gameplay_loop(game) -> None:
    """
    Main gameplay loop which runs the game.
    """
    # this is all meta code essentially
    end_condition = False
    while not end_condition:
        adventure = select_adventure(game)
        print("card selected")
        print(adventure)
        outcomes, adventure = attempt_adventure(game.investigator, adventure)
        game.discard_completed_adventure(adventure)
        print(f"{outcomes} received from card")
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


# current_progress

introduction()
game = start_game()
main_gameplay_loop(game)
