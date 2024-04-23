# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Eventually classes should probably be changed to named tuples

import random

#add some validation to this class
class GreatOldOne:
    """
    Creates Great Old One enemy.
    """
    def __init__(self, name:str, health:int, tasks:tuple, attack:str) -> None:
        self.name = name
        if health <=0:
            raise ValueError(f"{health} is not a valid starting health value.")
        self.starting_health = health
        self.health = health
        self.tasks = tasks
        self.attack = attack # this should be replaced by something later
    
    # Current win condition
    @property
    def alive(self) -> bool:
        if self.health<=0:
            return False
        else:
            print(f"You have defeated the terrifying {self.name}. The world is forever in your debt.")
            return True
    
    # Adjust health accordingly
    def take_damage(self, damage: int) -> None:
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    # should this be check tasks?
    def check_task(self, task, die_sequence):
        pass

class Character:
    def __init__(self, name:str, health: int, items: list=None) -> None:
        # maybe these will be added to or removed
        # could have special dice
        # start with no items in example
        self.name = name
        if health <= 0:
            raise ValueError(f"{health} is not a valid starting health value.")
        self.starting_health = health
        self.health = health
        if items:
            self.items = items
        else:
            self.items = []
        self.dice = 6 # this val will be modified, reset it at the beginning of each turn or at the end of each turn.
        self.current_roll = ['' for _ in range(self.dice)]

    # Current loss condition
    @property
    def alive(self) -> bool:
        if self.health<=0:
            return False
        else:
            return True

    # Adjust health accordingly
    def take_damage(self, damage: int) -> None:
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def roll_dice(self) -> None:
        self.current_roll = [green_die.roll() for _ in range(self.dice)]

    # should there be an undo feature?
    def assign_die_to_task(self, index:int, task):
        """
        Assigns die in current_roll at position index to a slot in the task.
        Note: the range for index is 1-len(self.current_roll).
        """
        # validate index
        index = index-1
        die = self.current_roll.pop(index)
        try:
            task.add_die(die)
        except ValueError as e:
            print(e)
            self.current_roll.append(die)
            print("Select a different die.")
        return task

    # check alive and resets number of die
    def end_turn():
        if self.alive:
            self.dice = 6
            self.current_roll = ['' for _ in range(self.dice)]
        else:
            print(f"{self.name} has died a gruesome death, you have lost. The world has ended.")
        



    
# needs validation
# needs overflow check method maybe?
class Task:
    """
    Create task object. The pattern is what is necessary to succeed at a task. The reward is what happens when you succeed, the penalty is what happens when you fail.
    """
    # reward/penalty are currently strings, but should be changed to something else.
    def __init__(self, name: str, pattern: dict, reward: str, penalty: str) -> None:
        self.name = name
        self.pattern = pattern
        self.reward = reward
        self.penalty = penalty
        self.slots = {key:0 for key in pattern.keys()}

    def assign_die(self, die_face:str) -> None:
        number, symbol = die_face.split(' x ')
        number = int(number)
        if symbol in self.pattern.keys():
            self.slots[symbol] += number
        else:
            # should this be an error
            raise ValueError(f"""{die_face} is not 
            contained in the pattern for this task.""")
        # what should I do about exceeding the maximum error?
        # maybe that is a separate method

    def __contains__(self, current_roll) -> bool:
        symbols = {die.split(' x ')[1] for die in current_roll}
        for symbol in symbols:
            if symbol in self.pattern.keys():
                return True
        return False

    @property
    def remaining(self) -> dict:
        return {key:self.pattern[key]-self.slots[key] for key in self.pattern.keys()}

    # add __str__ method for task
    @property
    def complete(self):
        for key in self.pattern.keys():
            if self.pattern[key]> self.slots[key]:
                print(f"The task is not yet complete, you still need {self.pattern[key] - self.slots[key]} {key}'s.")
                return False
        return True

class Die:
    SYMBOLS = {'1 x Investigate','2 x Investigate','3 x Investigate','4 x Investigate','1 x Scroll','2 x Scroll', '1 x Skull', '1 x Tentacles'}
    def __init__(self, faces:tuple)-> None:
        for face in faces:
            if face in Die.SYMBOLS:
                continue
            else:
                raise ValueError(f"{face} is not a valid symbol. We can not create this die.")
        if len(faces) != 6: # maybe this should also be relaxed
            raise ValueError(f"{faces} has too many sides to be a die.")
        self.faces = faces # tuple of elements of Symbols
    
    def roll(self) -> str:
        return random.choice(self.faces)

green_die = Die(('1 x Investigate','2 x Investigate','3 x Investigate','1 x Scroll', '1 x Skull', '1 x Tentacles'))
    

def assign_dice_to_task(current_roll, task):
    """
    Assigns dice from current roll to fixed task as long as it is possible.
    Returns task. Should it also return the remaining dice? Yes.
    """
    # current roll is fixed
    if not current_roll in task:
        print("None of the symbols of this role are in this task.")
        return current_roll, task
    while not task.complete and current_roll in task:
        print(current_roll)
        print(task.remaining)
        index = get_die_choice(len(current_roll))
        task.assign_die(current_roll.pop(index-1))
    if task.complete:
        return [], task
    else:
        print("There are no longer any symbols you can use in this roll for this task.")
        return current_roll, task

def attempt_task(character, task):
    character.roll_dice()
    while character.dice > 0 and not task.complete:
        character.current_roll, task = assign_dice_to_task(character.current_roll, task)
        character.dice = len(character.current_roll)-1
        character.roll_dice()
   
    if task.complete:
        print(f'You have completed the task: {task.name}!')
        print(f"You get a {task.reward}.")
        return task
    else:
        print(f"You have failed, you suffer the penalty of {task.penalty}.")
    
    

def get_die_choice(num_dice: int): #return value for this is a bit complex
    # what about when num_dice = 0 or 1?
    index = ""
    valid_input = [str(num) for num in range(1,num_dice+1)]
    valid_input.append("pass")
    while index not in valid_input:
        index = input(f"""Please input numbers 1-{num_dice} to select which die to assign to the task.\n
                    If none of your dice will work, enter pass.\n""")
    if index.lower() == "pass":
        return -1
    else:
        return int(index)
        

def create_generic():
    """
    This function creates basic instances of the above classes for the purpose of development.
    """
    basic_task1 = Task(name='basic_attack',pattern={'Investigate':2, 'Skull':1}, reward="+1 damage", penalty="-1 health")
    basic_task2 = Task(name='basic_heal',pattern={'Investigate':1, 'Scroll':2}, reward="+2 health", penalty="-1 health")
    basic_old_one = GreatOldOne("basic old one", 10, (basic_task1, basic_task2), "+2 damage")
    basic_character = Character("joe shmoe",6)
    return basic_old_one, basic_character


def start_game():
    """
    Initializes game state:
        - Creates Great Old One
        - Creates Die
        - Creates player
    """
    pass

# current_progress
old_one, joe = create_generic()
c1, c2 = old_one.tasks

