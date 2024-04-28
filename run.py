# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 investigators wide and 24 rows high
# Eventually classes should probably be changed to named tuples

from typing import List, Optional, Tuple, Union
# the below import statement should eventually be changed
from game_pieces import *
from db_utilities import GameSelection
from utilities import get_selection

def pause() -> None:
    input("\n                     Hit enter to continue.\n")

def introduction() -> None:
    basic_idea1 = '''    Welcome to "Chtulu Schmtulu," a dice rolling game heavily based on 
    Elder Sign from Fantasy Flight Games. In each game, you attempt 
    to Banish a Great Old One before they are Summoned or before you 
    are Defeated. After selecting a Great Old One to battle against, you 
    will select an Investigator to play as. The Great Old Ones are Summoned 
    when they gain enough Doom. They are Banished when you collect enough 
    Elder Signs.'''
    tldr = '''    TL;DR: Go to Locations, assign dice to complete tasks. Collect Elder Signs 
    before you are Defeated or the Great Old One gains enough Doom.'''
    basic_idea2 = '''    You will collect Elder Signs by completing locations. Doom is gained
    when the clock strikes midnight (the clock advances after each of your 
    turns) as well as through game effects. If your Investigator has 0 Health 
    or 0 Sanity, then you are defeated. If you are defeated or the Great Old 
    One is Summoned, then you have lost. If you collect enough Elder Signs to 
    Banish the Great Old One, then you have won!'''
    locations1 = '''    Each turn you will go to a location. To complete a location you must
    complete each task at the location. A task is completed by assigning 
    matching dice to the task in order to fulfill the requirements. Some 
    tasks also have you suffer a penalty by losing Health or Sanity. If 
    none of the symbols on your dice match a symbol on the task, you may 
    do a Pass.''' 
    locations2 = '''    A Pass rerolls all of your dice at the cost of forfeiting one of them.
    You may also use an Item (the Item selection menu also contains a 
    description of what each Item does). If you run out of dice, you fail
    the Location and suffer associated Penalty. If you complete a Location,
    you receive the associated Reward. Penalties can be losing Health or 
    Sanity, or the Great Old One gaining additional Doom. Rewards can be
    gaining an Item, Health, or Sanity.'''
    dice = '''    As the game revolves around rolling dice, here are the different dice 
    that are in the game:
    Green =  Investigate: 1, Investigate: 2, Investigate: 3, Lore: 1, 
             Skulls: 1, Tentacles: 1 
    Yellow = Investigate: 1, Investigate: 2, Investigate: 3, Investigate: 4, 
             Lore: 1, Skulls: 1
    Red =    Wild: 1, Investigate: 2, Investigate: 3, Investigate: 4, 
             Lore: 1, Skulls: 1
    Spell =  All Wild: 1'''
    losing_dice = '''    When you loss a die by passing, you will lose the earliest die in your 
    pool according to the ordering:
    Green < Yellow < Red < Spell'''
    difficulty = '''    Difficulty can be adjusted through the setting of two different parameters.
    Increment sets how much the clock advances after each of your turns. The 
    standard setting is 6 hours, so Doom accumulates every 4 turns. The second 
    is the starting dice pool. Standard (which is quite a challenge) is 6 Green 
    dice.'''
    items = '''    Each Investigator begins the game with different starting Items. Items come in
    4 varieties: Common, Unique, Clue, and Spell. Common Items will usually give you 
    a yellow die, Unique Items will usually give you a red die (for that location). 
    Clues allow you to reroll your dice without penalty. Spells add a Wild symbol 
    to your dice pool. You will also gain Items by completing Locations.'''
    future = '''    In the future, we would like to implement more of the game, such as abilities 
    of Investigators as well as Great Old Ones. This is a bit of a task though as 
    each ability requires a separate function that must be implemented which may take
    effect at different points in game play. There are other notable aspects of game 
    play which we would also like to implement in the future, such as focusing, 
    multiplayer mode, and Monsters.'''
    more_help = '''    If you have further questions, please see the ReadMe for this project at, 
    it contains examples of game play. It may also be beneficial to view geme play 
    or "how to play" videos for Elder Sign on YouTube.'''
    more_details = [basic_idea2, locations1, locations2, dice, difficulty, items, future, more_help]
    print(basic_idea1)
    pause()
    print(tldr)
    more_info = input("    Would you like more details about the game? Y/n\n")
    if more_info.lower() == 'y' or more_info.lower() =='yes':
        print()
        for msg in more_details:
            print(msg)
            pause()
    else:
        print("    Alright! Let's get started. That Great Old One isn't going to banish itself.")
    

#I feel like this can be combined with the other report function to be more streamlined?
def report_options(investigator, location):
    print(investigator.dice_pool)
    for index, task in enumerate(location):
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
    index = get_selection(len(items),'an item to use.',{'none'})
    if index == 'none':
        return investigator
    item = items[index-1]
    item.use(investigator)
    print(f'{investigator.name} used the {item.name} to {item.effect.lower()}.')
    return investigator
# I think this should be refactored into two functions, one a method of the Task class.
def assign_die_to_task(investigator, task): #'DicePool','Task':
    """
    Assigns single die from dice pool to task. Gets index of die from user and assigns it,
     if possible. If a pass is submitted, pass_move is called. This pops a die from 
     the dice pool and rerolls the remaining dice.
    """
    report_dice_n_task(investigator, task)
    # would a get die function be better?, I guess decoupling the dice pool and the task 
    # would mean that you wouldn't see what the task is anymore...
    index = get_selection(len(investigator),"a die to assign to this task", {'pass','item'})
    if index == "pass":
        investigator.pass_move()
        return investigator, task
    elif index == "item":
        return use_item_procedure(investigator), task
    die = investigator.dice_pool[index-1]
    if die in task:
        task.assign_die(die)
        investigator.dice_pool.pop(index-1)
        pause()
    else:
        print(f"{str(die)} is not a valid choice for {task}.")
    return investigator, task

# this function feels sloppy and not very streamlined/clean
def assign_dice_to_task(investigator, task):
    """
    Assigns dice from dice pool to a task until dice_pool is empty or the task is complete.
    Then returns the task and remaining dice.
    """
    # This is still a bit messy with where the rolling and print statements happen being logically correct but slightly convoluted.
    # is the above still true?
    # change to a do while loop, but how?
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

def attempt_location(investigator:'Investigator',location:'Location') -> str:
    # do we roll here? I think so.
    investigator.roll()
    #print(dice_pool)
    #for task in location:
     #   print(task)
    #I feel like I don't really need these conditions here
    while not location.complete and len(investigator) > 0:
        report_options(investigator, location)
        task_index = get_selection(len(location.tasks),"a task to attempt",{'pass','item'})
        # Is this technically in the spirit of the game?
        if task_index == 'pass':
            investigator.pass_move()
            continue
        elif task_index == "item":
            investigator = use_item_procedure(investigator)
            continue
        task = location[task_index-1]
        # should this part of the validation be done elsewhere?
        if task.valid(investigator.dice_pool):
            investigator, task = attempt_task(investigator, task)
            # should I pop the task here if it is complete?
            # selecting the same task gives a free reroll.
        else:
            print("Your roll doesn't have any symbols for that task.")
            continue
    if location.complete:
            print(f"You have completed {location.name}!")
            print(f"You receive {location.reward}")
            return location.reward, location
    elif len(investigator) == 0:
        print(f"You have failed, you suffer the penalty of {location.penalty}.")
        return location.penalty, location
        

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
    introduction()
    game_data = GameSelection()
    great_old_one = game_data.select_great_old_one()
    investigator = game_data.select_investigator()
    start_time = 0
    increment = 12
    game = Game(investigator,great_old_one,game_data.location_deck,
                game_data.item_deck,start_time, increment)
    #print(game)
    print(great_old_one)
    print(investigator)
    pause()
    # main_gameplay_loop(game)
    return game

def select_location(game):
    return game.current_locations.pop(0)

def test_gameplay():
    game_data = GameSelection()
    great_old_one = game_data.great_old_ones[0]
    investigator = game_data.investigators[0]
    start_time = 0
    game = Game(investigator,great_old_one,start_time,game_data.location_deck,
                game_data.item_deck)
    main_gameplay_loop(game)

def main_gameplay_loop(game) -> None:
    """
    Main gameplay loop which runs the game.
    """
    # this is all meta code essentially
    end_condition = False
    while not end_condition:
        location = select_location(game)
        print("card selected")
        print(location)
        outcomes, location = attempt_location(game.investigator, location)
        game.discard_completed_location(location)
        print(f"{outcomes} received from card")
        apply_outcomes(outcomes, game)
        pause()
        print("End of turn.")
        end_condition = game.end_turn()
    # these messages could be refactored into a dict maybe?
    # or a method of the game object, like a property?
    if end_condition == "Banished":
        print(f"Congratulations! {game.investigator.name} has defeated {game.great_old_one.name} and successfully banished them to the dimension from which they came.")
    elif end_condition == "Died":
        print(f"Oh no! {game.investigator.name} has been defeated. Now nothing stands in the way of {game.great_old_one.name}.")
    elif end_condition == "Summoned":
        print(f"{game.investigator.name} was unable to prevent the inevitable. {game.great_old_one.name} has been summoned. The end of humanity is at hand.")
    
# current_progress

game = start_game()
#main_gameplay_loop(game)
