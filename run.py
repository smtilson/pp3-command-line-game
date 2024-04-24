# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Eventually classes should probably be changed to named tuples

import random
from typing import List, Optional, Tuple

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
        # self.dice = 6 # this val will be modified, reset it at the beginning of each turn or at the end of each turn.
        self.dice_pool = DicePool()

    def __str__(self):
        return f"{self.name} has {self.health} left."
        
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
        self.dice_pool.roll()
    
    @property
    def dice(self) -> int:
        return len(self.dice_pool)

    # advances clock, check alive and resets number of die
    def end_turn(self):
        # clock.advance()
        # print(f"Advancing clock. It is now {clock.time}")
        if self.alive:
            # This resets the dice pool and the face of each die to initial face
            print(f"{self.name} is still alive, dice pool is being reset.")
            self.dice_pool.reset()
        else:
            print(f"{self.name} has died a gruesome death, you have lost. The world has ended.")
    
# needs validation
# needs overflow check method maybe?

class Task:
    def __init__(self, pattern:dict) -> None:
        #needs validation that pattern is acceptable
        self.pattern = pattern
        self.slots = {key:0 for key in pattern.keys()}

    def __contains__(self, dice_pool) -> bool:
        symbols = {die.parse()[1] for die in dice_pool}
        for symbol in symbols:
            if symbol in self.pattern.keys():
                return True
        return False

    #should this be different?
    def __str__(self):
        return f"remaining: {self.remaining}"

    def assign_die(self, die_face:str) -> None:
        number, symbol = Die.parse(die_face)
        if symbol in self.pattern.keys():
            self.slots[symbol] += number
        else:
            # should this be an error
            raise ValueError(f"{symbol} is not contained in the pattern for this task.")
        # what should I do about exceeding the maximum error?
        # maybe that is a separate method
    
    # resets task for next attempt, if at all
    # eventually this will be removed
    def reset(self) -> None:
        self.slots = {key:0 for key in self.pattern.keys()}


    @property
    def remaining(self) -> dict:
        return {key:max(0,self.pattern[key]-self.slots[key]) for key in self.pattern.keys()}
    
    @property
    def complete(self):
        for val in self.remaining.values():
            if val > 0:
                return False
        return True

class TaskCard:
    """
    Create task object. The pattern is what is necessary to succeed at a task. The reward is what happens when you succeed, the penalty is what happens when you fail.
    """
    # reward/penalty are currently strings, but should be changed to something else.
    def __init__(self, name: str, tasks: List['Task'], reward: str, penalty: str) -> None:
        self.name = name
        self.tasks = tasks
        self.reward = reward
        self.penalty = penalty

    def __contains__(self, dice_pool) -> bool:
        symbols = {die.parse()[1] for die in dice_pool}
        for symbol in symbols:
            for task in self.tasks:
                if symbol in task:
                    return True
        return False

    def __str__(self):
        string = f"name: {self.name}\n"
        for task in self.tasks:
            string += f"task: {task.pattern}\n"
        string += f"reward: {self.reward}\n"
        string += f"penalty: {self.penalty}\n"
        return string

    def __iter__(self):
        return iter(self.tasks)

    @property
    def complete(self) -> bool:
        for task in tasks:
            if not task.complete:
                return False
        return True
    
    @property
    def status(self):
        if self.complete:
            print(f"{self.name} is complete!")
        else:
            print(f"{self.name} is not yet complete.")
            print("You still need to complete the following:")
            for index, task in enumerate(self.tasks):
                if not task.complete:
                    print(f"Task {index}: {task.pattern}")

class Die:
    SYMBOLS = {'1 x Investigate','2 x Investigate','3 x Investigate','4 x Investigate','1 x Scroll','2 x Scroll', '1 x Skull', '1 x Tentacles'}
    
    def __init__(self, *faces:str)-> None:
        for face in faces:
            if face in Die.SYMBOLS:
                continue
            else:
                raise ValueError(f"{face} is not a valid symbol. We can not create this die.")
        if len(faces) != 6: # maybe this should also be relaxed
            raise ValueError(f"{faces} does not have the correct number of sides to be a die (in this game).")
        self.faces = faces # tuple of elements of Die.SYMBOLS
        # Current face showing of die
        self.face = ''
    
    def __str__(self) -> str:
        return self.face
    
    # this is not ideal, but it addresses the printing dice_pool issue.
    def __repr__(self) -> str:
        return self.face

    def parse(self):
        """
        Parses the face of the die. Returns number of symbols as int and symbol as string.
        """
        # should this automatically roll the die if it hasn't been rolled yet?
        if not self.face:
            raise ValueError("This die has not yet been rolled.")
        number, symbol = self.face.split(' x ')
        number = int(number)
        return number, symbol

    def roll(self) -> None:
        self.face = random.choice(self.faces)
    
    @classmethod
    def green(cls):
        return cls('1 x Investigate','2 x Investigate','3 x Investigate','1 x Scroll', '1 x Skull', '1 x Tentacles')

class DicePool:
    def __init__(self) -> None:
        # implement the dunder method for this later
        #for die in dice:
        #    if type(die) != Die:
        #        raise ValueError(f"Can not make a dice pool containing {die} since it is not a Die.")
        self.dice = [Die.green() for _ in range(6)]
    
    # is this the correct thing
    def __iter__(self) -> 'iterator':
        return iter(self.dice)

    #def __next__(self) -> 'Die':

    def __getitem__(self,index) -> 'Die':
        return self.dice[index]

    def roll(self) -> None:
        for die in self.dice:
            die.roll()
    
    def pop(self, index:int=0) -> 'Die':
        # defaults to removing first die
        # this is because yellow and red dice will be appended and we 
        # probably don't want to remove those by default
        return self.dice.pop(index)
    
    def __str__(self) -> str:
        return str(self.dice)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return len(self.dice)

    def reset(self) -> None:
        self.dice = [Die.green() for _ in range(6)]

    

    
    # need methods for adding yellow and red dice

def pause() -> None:
    input("Hit enter to continue.")

def assign_dice_from_pool_to_task(pool, task):
    """
    Assigns dice from pool to fixed task as long as it is possible.
    Returns task. Should it also return the remaining dice? Yes.
    """
    # current pool is fixed
    if not pool in task:
        print(pool)
        print(task)
        print("None of the symbols of this roll are in this task.")
        pause()
        pool.pop()
        return pool, task
    while not task.complete and pool in task:
        print()
        print(pool)
        print(task.remaining)
        index = get_die_choice(len(pool))
        #maybe eventually replace this with something automated that checks for containment?
        #but then again, we shouldn't force a player to like assign a 1 investigate die to a task that  
        # has 8 investiagte symbols.
        if index == "pass":
            print("Not attempting to assign any dice from this roll.")
            print("Removing one die form the beginning of your dice pool.")
            pool.pop(0)
            return pool, task
        die = pool[index-1]
        print(f"{index=} and {die=}.")
        try:
            print(f"attempting to assign {die} to {task.remaining}.")
            task.assign_die(die)
        except ValueError as e:
            print(e)
            pause
            continue
        else:
            pool.pop(index-1)
            print(f"{die} was successfully assigned.")
    if task.complete:
        return pool, task
    else:
        print("There are no longer any symbols you can use in this roll for this task.")
        print(pool)
        print("Removing one die form the beginning of your dice pool.")
        if len(pool)>0:
            pool.pop(0)
        return pool, task

def attempt_task(dice_pool, task):
    print(f"Attempting: {task}")
    print(f"with {dice_pool}")
    
    #print("starting while loop in attempt task")
    while len(dice_pool) > 0 and not task.complete:
        print("calling assign dice from pool to task function")
        dice_pool, task = assign_dice_from_pool_to_task(dice_pool, task)
        if not task.complete:
            print("rerolling dice in pool")
            dice_pool.roll()
            print(f"You rolled {dice_pool}")
            print(f"{task.remaining} is still remaining.")
    if task.complete:
        print(f'You have completed this task!')
        #print(f"You get a {task.reward}.")
        return task
    else:
        print(f"You have failed, you die a tragic death")# the penalty of {task.penalty}.")
        task.reset()

def attempt_task_card(character:'Character',task_card:'TaskCard'):
    # do we roll here? I think so.
    character.roll_dice()
    pool = character.dice_pool
    print(pool)
    for task in task_card:
        print(task)
    task_index = get_task_choice(len(task_card.tasks))


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
        f"If none of your dice will work, enter pass.\n")
        if index not in valid_input:
            print(f"\n\n{index} is invalid.\n")
            index = ""
    if index.lower() == "pass":
        return index.lower()
    else:
        return int(index)
        

def create_generic():
    """
    This function creates basic instances of the above classes for the purpose of development.
    """
    basic_task1 = Task(pattern={'Investigate':2, 'Skull':1})#, reward="+1 damage", penalty="-1 health")
    basic_task2 = Task(pattern={'Investigate':1, 'Scroll':2})#, reward="+2 health", penalty="-1 health")
    basic_old_one = GreatOldOne("basic old one", 10, (basic_task1, basic_task2), "+2 damage")
    basic_character = Character("joe shmoe",6)
    basic_card = TaskCard("basic task card", [basic_task1,basic_task2], "+1 damage", "-1 health")
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
c1, c2 = old_one.tasks
c3 = Task({"Investigate":9})
joe.roll_dice()
