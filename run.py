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
    input("Hit enter to continue.\n")

#I feel like this can be combined with the other report function to be more streamlined?
def report_options(investigator, task_card):
    print(investigator.dice_pool)
    for index, task in enumerate(task_card):
        print(f"{index+1} = {str(task)}")

#thise should be made to be nicer
def report_dice_n_task(investigator, task):    
    print(investigator.dice_pool)
    print(task)    


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
    index = get_selection(len(investigator),"a die to assign to this task", {'pass'})
    if index == "pass":
        investigator.pass_move()
        return investigator, task
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
    #task.suffer_penalty(investigator)
    investigator, task = assign_dice_to_task(investigator, task)
    while not task.complete and len(investigator) > 0:
        investigator, task = assign_dice_to_task(investigator, task)
    if task.complete:
        print('You have completed this task!')
        investigator.roll()
        return investigator, task
    print("You are out of dice.")
    return investigator, task

def attempt_task_card(investigator:'Investigator',task_card:'TaskCard') -> str:
    # do we roll here? I think so.
    investigator.roll()
    #print(dice_pool)
    #for task in task_card:
     #   print(task)
    #I feel like I don't really need these conditions here
    while not task_card.complete and len(investigator) > 0:
        report_options(investigator, task_card)
        task_index = get_selection(len(task_card.tasks),"a task to attempt",{'pass'})
        # Is this technically in the spirit of the game?
        if task_index == 'pass':
            investigator.pass_move()
            continue
        task = task_card[task_index-1]
        # should this part of the validation be done elsewhere?
        if task.valid(investigator.dice_pool):
            investigator, task = attempt_task(investigator, task)
            # should I pop the task here if it is complete?
            # selecting the same task gives a free reroll.
        else:
            print("Your roll doesn't have any symbols for that task.")
            continue
    if task_card.complete:
            print(f"You have completed {task_card.name}!")
            print(f"You receive {task_card.reward}")
            return task_card.reward, task_card
    elif len(investigator) == 0:
        print(f"You have failed, you suffer the penalty of {task_card.penalty}.")
        return task_card.penalty, task_card
        

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
    game_data = GameSelection()
    great_old_one = game_data.select_great_old_one()
    investigator = game_data.select_investigator()
    start_time = 0
    game = Game(investigator,great_old_one,start_time,game_data.task_card_deck,
                game_data.item_deck)
    #print(game)
    print(great_old_one)
    print(investigator)
    pause()
    # main_gameplay_loop(game)
    return game

def select_task_card(game):
    return game.current_task_cards.pop(14)

def test_gameplay():
    game_data = GameSelection()
    great_old_one = game_data.great_old_ones[0]
    investigator = game_data.investigators[0]
    start_time = 0
    game = Game(investigator,great_old_one,start_time,game_data.task_card_deck,
                game_data.item_deck)
    main_gameplay_loop(game)

def main_gameplay_loop(game) -> None:
    """
    Main gameplay loop which runs the game.
    """
    # this is all meta code essentially
    end_condition = False
    while not end_condition:
        task_card = select_task_card(game)
        print("card selected")
        print(task_card)
        outcomes, task_card = attempt_task_card(game.investigator, task_card)
        game.discard_completed_task_card(task_card)
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



