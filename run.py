# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Eventually classes should probably be changed to named tuples

from typing import List, Optional, Tuple
# the below import statement should eventually be changed
from game_pieces import *
import db_utilities as db

def pause() -> None:
    input("Hit enter to continue.")

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
    index = get_die_choice(len(dice_pool))
    if index == "pass":
        dice_pool = pass_move(dice_pool)
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

def attempt_task_card(character:'Character',task_card:'TaskCard') -> str:
    # do we roll here? I think so.
    dice_pool = character.dice_pool
    dice_pool.roll()
    #print(dice_pool)
    #for task in task_card:
     #   print(task)
    #I feel like I don't really need these conditions here
    #while not task_card.complete and len(dice_pool) > 0:
    # change this to a do while loop, like in the get choice function
    while not task_card.complete and len(dice_pool) > 0:
        report_options(dice_pool, task_card)
        task_index = get_task_choice(len(task_card.tasks))
        # Is this technically in the spirit of the game?
        if task_index == 'pass':
            dice_pool = pass_move(dice_pool)
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
        
# I don't like the reroll being part of this move, but I guess it is fine.
def pass_move(dice_pool) -> 'DicePool':
    """
    Removes a die from the dice pool and rerolls remaining dice.
    """
    print("Sacrificing a die.")
    dice_pool.pop()
    print("Rerolling your remaining dice.")
    # will roll throw an exception if there are no dice?
    dice_pool.roll()
    return dice_pool
    
# write valid input function.
def get_task_choice(num_tasks: int):
    condition = True
    valid_input = [str(num) for num in range(1,num_tasks+1)]
    valid_input.append("pass")
    index = input(f"\nPlease input numbers 1-{num_tasks} to select which task to attempt.\n")
    while index not in valid_input:
        print(f"{index} is invalid.")
        index = input(f"Please input numbers 1-{num_tasks} to select which task to attempt.\n")
    if index.lower() == "pass":
        return 'pass'
    else:
        return int(index)

def get_die_choice(num_dice: int): #return value for this is a bit complex
    # what about when num_dice = 0 or 1?
    # maybe refactor these get_choice functions into one function.
    valid_input = [str(num) for num in range(1,num_dice+1)]
    valid_input.append("pass")
    index = input(f"\nPlease input a selection from 1-{num_dice} to select which die to assign to the task.\n"
        f"Enter pass to sacrifice a die and reroll.\n")
    while index not in valid_input:
        print(f"\n{index} is invalid.\n")
        index = input(f"\nPlease input numbers 1-{num_dice} to select which die to assign to the task.\n"
        f"Enter pass to sacrifice a die and reroll.\n")
    if index.lower() == "pass":
        return index.lower()
    else:
        return int(index)
        
def apply_outcomes(outcomes, game):
    for key, value in outcomes.items():
        print(f"Applying outcome {key}: {value}.")
        OUTCOMES[key](value, game)

def start_game():
    """
    Initializes game state:
        - Create Great Old Ones
        - Create Characters
        - Create Task Cards
        - Create Items
    Select game state:
        - Select Great Old One
        - Select Character
    Begin Game:
        - Deal Task Cards
        - Begin Game (call main_gameplay_loop)
    """
    pass

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
        outcomes, task_card = attempt_task_card(game.character, task_card)
        game.discard_completed_task_card(task_card)
        print(f"{outcomes} received from card")
        apply_outcomes(outcomes, game)
        pause()
        print("End of turn.")
        end_condition = game.end_turn()
    # these messages could be refactored into a dict maybe?
    # or a method of the game object, like a property?
    if end_condition == "Banished":
        print(f"Congratulations! {game.character.name} has defeated {game.great_old_one.name} and successfully banished them to the dimension from which they came.")
    elif end_condition == "Died":
        print(f"Oh no! {game.character.name} has been defeated. Now nothing stands in the way of {game.great_old_one.name}.")
    elif end_condition == "Summoned":
        print(f"{game.character.name} was unable to prevent the inevitable. {game.great_old_one.name} has been summoned. The end of humanity is at hand.")

def create_task_card_deck():
    task_card_data = db.fetch_task_card_data()
    task_card_deck = [db.task_dict_to_task_card(card_dict) for card_dict in task_card_data if card_dict['Rewards']!={}]
    return task_card_deck


def create_simple_hard(doom, elder_signs, sanity, stamina, start_time):
    """
    This function creates basic instances of the above classes for the purpose of development.
    """
    bt1a = Task({'Investigate':2, 'Skull':1})
    bt1b = Task({'Investigate':2, 'Skull':1})
    bt2 = Task({'Investigate':1, 'Lore':2})
    ht3 = Task({"Investigate":6})
    basic_old_one = GreatOldOne("basic old one", doom, elder_signs, "+1 damage")
    basic_character = Character("joe shmoe",sanity, stamina)
    basic_card1 = TaskCard("basic task card1","no flavor", [bt1a, bt1b], {'Stamina': 1}, {"Stamina": -1})
    basic_card2 = TaskCard("basic task card2","no flavor", [bt1a,bt2], {"Elder Sign": 1}, {"Sanity": -1})
    hard_card1 = TaskCard("hard task card 1","no flavor", [bt1a,ht3], {"Elder Sign": 2}, {"Stamina": -1})
    hard_card2 = TaskCard("hard task card 2","no flavor", [bt2,ht3], {"Elder Sign": +2}, {"Sanity": -1})
    task_deck = []
    for _ in range(3):
        task_deck.append(basic_card1)
        task_deck.append(basic_card2)
        task_deck.append(hard_card1)
        task_deck.append(hard_card2)
    game1 = Game(basic_character,basic_old_one,start_time,task_deck)
    game2 = Game(basic_character,basic_old_one,start_time,create_task_card_deck())
    game1.shuffle()
    return game1, game2

    
# current_progress
game1, game2= create_simple_hard(2,2,5,5,0)

bt1 = Task({'Investigate':2, 'Skull':1})
bt2 = Task({'Investigate':1, 'Lore':2})
ht3 = Task({"Investigate":8})
