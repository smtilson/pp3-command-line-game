# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 investigators wide and 24 rows high
# Eventually classes should probably be changed to named tuples

from typing import List, Optional, Tuple, Union
# the below import statement should eventually be changed
from game_pieces import *
import db_utilities as db

def pause() -> None:
    input("Hit enter to continue.\n")

#I feel like this can be combined with the other report function to be more streamlined?
def report_options(dice_pool, task_card):
    print(dice_pool)
    for index, task in enumerate(task_card):
        print(f"{index+1} = {str(task)}")

def report_dice_n_task(dice_pool, task):    
    print(dice_pool)
    print(task)    


# I think this should be refactored into two functions, one a method of the Task class.
def assign_die_to_task(dice_pool, task): #'DicePool','Task':
    """
    Assigns single die from dice pool to task. Gets index of die from user and assigns it,
     if possible. If a pass is submitted, pass_move is called. This pops a die from 
     the dice pool and rerolls the remaining dice.
    """
    report_dice_n_task(dice_pool, task)
    # would a get die function be better?, I guess decoupling the dice pool and the task 
    # would mean that you wouldn't see what the task is anymore...
    index = get_selection(len(dice_pool),"a die to assign to this task", {'pass'})
    if index == "pass":
        dice_pool.pass_move()
        return dice_pool, task
    die = dice_pool[index-1]
    if die in task:
        task.assign_die(die)
        dice_pool.pop(index-1)
        pause()
    else:
        print(f"{str(die)} is not a valid choice for {task}.")
    return dice_pool, task

# this function feels sloppy and not very streamlined/clean
def assign_dice_to_task(dice_pool, task):
    """
    Assigns dice from dice pool to a task until dice_pool is empty or the task is complete.
    Then returns the task and remaining dice.
    """
    # This is still a bit messy with where the rolling and print statements happen being logically correct but slightly convoluted.
    # is the above still true?
    # change to a do while loop, but how?
    dice_pool, task = assign_die_to_task(dice_pool, task)
    while not task.complete and len(dice_pool) > 0:
        # should this catch be at the beginning?
        dice_pool, task = assign_die_to_task(dice_pool, task)
    return dice_pool, task
        
def attempt_task(dice_pool, task):
    '''
    Attmepts to complete task by assigning dice, and doing a pass move (lose die and reroll).
    Returns dice pool and task if dice_pool is empty or task is complete.
    '''
    dice_pool, task = assign_dice_to_task(dice_pool, task)
    while not task.complete and len(dice_pool) > 0:
        dice_pool, task = assign_dice_to_task(dice_pool, task)
    if task.complete:
        print('You have completed this task!')
        dice_pool.roll()
        return dice_pool, task
    print("You are out of dice.")
    return dice_pool, task

def attempt_task_card(investigator:'Investigator',task_card:'TaskCard') -> str:
    # do we roll here? I think so.
    dice_pool = investigator.dice_pool
    dice_pool.roll()
    #print(dice_pool)
    #for task in task_card:
     #   print(task)
    #I feel like I don't really need these conditions here
    #while not task_card.complete and len(dice_pool) > 0:
    # change this to a do while loop, like in the get choice function
    while not task_card.complete and len(dice_pool) > 0:
        report_options(dice_pool, task_card)
        task_index = get_selection(len(task_card.tasks),"a task to attempt",{'pass'})
        # Is this technically in the spirit of the game?
        if task_index == 'pass':
            dice_pool.pass_move()
            continue
        task = task_card[task_index-1]
        # should this part of the validation be done elsewhere?
        if task.valid(dice_pool):
            dice_pool, task = attempt_task(dice_pool, task)
            # should I pop the task here if it is complete?
            # selecting the same task gives a free reroll.
        else:
            print("Your roll doesn't have any symbols for that task.")
            continue
    if task_card.complete:
            print(f"You have completed {task_card.name}!")
            print(f"You receive {task_card.reward}")
            return task_card.reward, task_card
    elif len(dice_pool) == 0:
        print(f"You have failed, you suffer the penalty of {task_card.penalty}.")
        return task_card.penalty, task_card
        
#call needs to be paired with some other message to explain the extra options.
# extra_options maybe will be changed to a list to make it easier
def get_selection(num_choices:int, type_of_choice:str, extra_options:set=set()) -> Union[int,str]:
    index = input(f"Please select an option from 1-{num_choices} to choose {type_of_choice}.\n"
                    f"You may also select an option from {extra_options}.")
    # explain(extra_options)
    extra_options = {word.lower() for word in extra_options}
    valid_input = {str(num) for num in range(1,num_choices+1)}.union(extra_options)
    while index not in valid_input:
        print(f"{index} is not a valid choice.")
        index = input(f"Please select an option from 1-{num_choices} to choose a {type_of_choice}.\n"
                    f"You may also select an option from {extra_options}.")
        index = index.lower()
    if index in extra_options:
        return index
    else:
        return int(index)

def apply_outcomes(outcomes, game):
    for key, value in outcomes.items():
        print(f"Applying outcome {key}: {value}.")
        OUTCOMES[key](value, game)

def setup_game():
    # Initialize game data
    task_card_deck = db.fetch_task_cards()
    great_old_ones = db.fetch_great_old_ones()
    investigators = db.fetch_investigators()
    #print(investigators)
    #pause()
    item_deck = db.fetch_items()
    for great_old_one in great_old_ones:
        great_old_one.selection()
    index = get_selection(len(great_old_ones),'a Great Old One to battle')
    great_old_one = [demon for demon in great_old_ones if demon.index == index][0]
    for investigator in investigators:
        print(investigator.index)
        print(investigator)
    index = get_selection(len(investigators),"an investigator to play as")
    investigator = [inv for inv in investigators if inv.index == index][0]
    start_time = 0
    game = Game(investigator,great_old_one,start_time,task_card_deck, item_deck)
    #print(game)
    print(great_old_one)
    print(investigator)
    pause()
    return game
    
def start_game(start_time=0):
    """
    Initializes game state:
        - Create Great Old Ones
        - Create investigators
        - Create Task Cards
        - Create Items
    Select game state:
        - Select Great Old One
        - Select investigator
    Begin Game:
        - Deal Task Cards
        - Begin Game (call main_gameplay_loop)
    """
    game = setup_game()
    return game

def select_task_card(game):
    return game.current_task_cards.pop(0)

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
game = start_game()
main_gameplay_loop(game)


