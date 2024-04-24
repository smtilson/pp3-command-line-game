# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Eventually classes should probably be changed to named tuples

from typing import List, Optional, Tuple
# the below import statement should eventually be changed
from game_pieces import *

def pause() -> None:
    input("Hit enter to continue.")

# this function feels sloppy and not very streamlined/clean
def assign_dice_to_task(dice_pool, task):
    """
    Assigns dice from dice pool to a task. Takes index of dice to 
    assign and assigns it, if possible. If a pass is submitted, pass_move is called.
    This pops a die from the dice pool and rerolls the dice.
    Then, we rReturn the task and remaining dice.
    """
    #I am removing the control flow which checks for the thing being valid.
    # I will just include it in the message for get 
    #This is still a bit messy with where the rolling and print statements happen being logically correct but slightly convoluted.
    while not task.complete:
        if len(dice_pool) == 0:
            return dice_pool, task
        print(f"Your roll: {dice_pool}.")
        print(f"Remaining: {task.remaining}")
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
        
def attempt_task(dice_pool, task):
    # move this validation elsewhere
    while not task.complete:
        dice_pool, task = assign_dice_to_task(dice_pool, task)
        if len(dice_pool) == 0:
            print("You are out of dice.")
            return dice_pool, task
    print('You have completed this task!')
    return dice_pool, task    

def attempt_task_card(character:'Character',task_card:'TaskCard'):
    # do we roll here? I think so.
    character.roll_dice()
    dice_pool = character.dice_pool
    print(dice_pool)
    for task in task_card:
        print(task)
    while not task_card.complete and len(dice_pool) > 0:
        task_index = get_task_choice(len(task_card.tasks))
        if task_index == 'pass':
        task = task_card[task_index-1]
        # should this part of the validation be done elsewhere?
        if task.valid(dice_pool):
            dice_pool, task = attempt_task(dice_pool, task)
        else:
            continue
        if task.complete:
            if task.card.complete:
                print(f"You have completed {task_card.name}!")
                print(f"You receive {task_card.reward}")
        else:
            print(f"You have failed, you suffer the penalty of {task_card.penalty}.")

        
# I don't like the reroll being part of this move, but I guess it is fine.
def pass_move(dice_pool) -> 'DicePool':
    print("Sacrificing a die.")
            dice_pool.pop()
            print("Rerolling your remaining dice.")
            # will roll throw an exception if there are no dice?
            dice_pool.roll()
            return dice_pool
# write valid input function.
def get_task_choice(num_tasks: int):
    index = ""
    valid_input = [str(num) for num in range(1,num_tasks+1)]
    valid_input.append("pass")
    while not index:
        index = input(f"\nPlease input numbers 1-{num_tasks} to select which task to attempt.\n")
        if index not in valid_input:
            print(f"\n\n{index} is invalid.\n")
            index = ""
    if index.lower() == "pass":
        return index.lower()
    else:
        return int(index)
    

def get_die_choice(num_dice: int): #return value for this is a bit complex
    # what about when num_dice = 0 or 1?
    index = ""
    valid_input = [str(num) for num in range(1,num_dice+1)]
    valid_input.append("pass")
    while not index:
        index = input(f"\nPlease input numbers 1-{num_dice} to select which die to assign to the task.\n"
        f"Enter pass to sacrifice a die and reroll.\n")
        if index not in valid_input:
            print(f"\n{index} is invalid.\n")
            index = ""
    if index.lower() == "pass":
        return index.lower()
    else:
        return int(index)
        

def create_generic():
    """
    This function creates basic instances of the above classes for the purpose of development.
    """
    bt1 = Task({'Investigate':2, 'Skull':1})
    bt2 = Task({'Investigate':1, 'Scroll':2})
    basic_old_one = GreatOldOne("basic old one", 10, 10, "+2 damage")
    basic_character = Character("joe shmoe",6)
    basic_card = TaskCard("basic task card", [bt1,bt2], "+1 damage", "-1 health")
    return basic_old_one, basic_character, basic_card


def start_game():
    """
    Initializes game state:
        - Creates Great Old One
        - Creates Die
        - Creates player
    """
    pass

# current_progress
old_one, joe, sample_task_card= create_generic()
c3 = Task({"Investigate":9})
joe.roll_dice()
