# This file contains the game pieces that need to be loaded to play the game
from random import choice
from typing import List, Optional, Tuple

#add some validation to this class
class GreatOldOne:
    """
    Creates Great Old One enemy.
    """
    def __init__(self, name:str, doom:int, elder_signs:int,attack:str) -> None:
        self.name = name
        self.doom_threshold = doom
        self.current_doom = 0
        self.elder_sign_threshold = elder_signs
        self.current_elder_signs = 0
        self.attack = attack # this should be replaced by something later, I now, a custom function will be stored here.
    
    # Win condition
    @property
    def banished(self) -> bool:
        if self.current_elder_signs >= self.elder_sign_threshold:
            print(f"You have defeated the terrifying {self.name}. The world is forever in your debt.")
            return True
        else:
            # should there be a message here
            return False
    
    # Loss condition
    @property
    def summoned(self) -> bool:
        if self.current_doom >= self.doom_threshold:
            print(f"The terrifying {self.name} has been summoned and devours the world.")
            return True
        else:
            # should there be a message here
            return False
    
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
        
    # Loss condition
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

    def add_green(self) -> None:
        self.dice_pool.add_green()

    def add_yellow(self) -> None:
        self.dice_pool.add_yellow()

    @property
    def dice(self) -> int:
        return len(self.dice_pool)

    # advances clock, check alive and resets number of die
    def end_turn(self):
        # This resets the dice pool and the face of each die to initial face
        print(f"{self.name} is still alive, dice pool is being reset.")
        self.dice_pool.reset()
        
# needs validation
# needs overflow check method maybe? <- wtf does this mean

class Game:
    def __init__(self, character, great_old_one) -> None:
        self.character = character
        self.great_old_one = great_old_one
        # not yet implimented
        # self.clock = Clock()
        # self.task_card_deck = TaskCard.create_deck()
    # def end_turn
    
    @property
    def end_condition(self):
        pass

class Clock:
    #This is where the difficulty setting could be, the number of turns in a day.
    def __init__(self):
        self.time = 0
    
    #how many hours are in the day
    def advance_clock(self) -> None:
        self.time += 3
        if self.time == 12:
            print("It is midnight!")
        elif self.time == 15:
            self.time = 3
            
    def check_clock(self) -> None:
        print(f"It is currently {self.time} o'clock.")
        print(f"You have {(12-self.time)//3} turns until doom advances.")



class Task:
    def __init__(self, pattern:dict) -> None:
        #needs validation that pattern is acceptable
        self.pattern = pattern
        self.remaining = pattern

    def __contains__(self, die) -> bool:
        return die.parse()[1] in self.remaining.keys()

    def valid(self, dice_pool) -> bool:
        for die in dice_pool:
            if die in self:
                return True
        return False

    
    def __str__(self):
        return f"Remaining: {self.remaining}"
    
    #should this be different?
    def __repr__(self):
        return self.__str__()

    def assign_die(self, die:'Die') -> None:
        print(f"Assigning die with {str(die)} to {self.remaining}.")
        number, symbol = Die.parse(die)
        self.remaining[symbol] -= number
        if self.remaining[symbol] <= 0:
            del self.remaining[symbol]
       
    # resets task for next attempt, if at all
    # eventually this will be removed
    def reset(self) -> None:
        self.remaining = self.pattern 
    
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

    def __str__(self):
        string = f"name: {self.name}\n"
        for task in self.tasks:
            string += f"task: {task.pattern}\n"
        string += f"reward: {self.reward}\n"
        string += f"penalty: {self.penalty}\n"
        return string

    def __iter__(self):
        return iter(self.tasks)

    def __getitem__(self, index) -> 'Task':
        return self.tasks[index]

    def valid(self, dice_pool) -> bool:
        for task in self:
            if task.valid(dice_pool):
                return True
        return False

    @property
    def complete(self) -> bool:
        for task in self.tasks:
            if not task.complete:
                return False
        return True

    @property
    def remaining(self) -> list:
        return [task for task in self if not task.complete]

    
    @property
    def status(self):
        if self.complete:
            print(f"{self.name} is complete!")
        else:
            print(f"{self.name} is not yet complete.")
            print("You still need to complete the following:")
            for index, task in enumerate(self.remaining):
                print(f"Task {index}: {task.pattern}")

    def reset(self) -> None:
        for task in self:
            task.reset()

# add color for this and then change the repn methodto show color and die face
class Die:
    SYMBOLS = {'1 x Investigate','2 x Investigate','3 x Investigate','4 x Investigate','1 x Lore','2 x Lore', '1 x Skull', '1 x Tentacles'}
    COLORS = {'green', 'yellow'}
    def __init__(self, color, *faces:str)-> None:
        # this should be put into a validate color method
        self.color = color 
        # this should be put into a validate faces method
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
    
    def __repr__(self) -> str:
        return self.color+': '+self.face

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
        # having a weird error where
        self.face = choice(self.faces)
    
    @classmethod
    def green(cls):
        return cls('Green','1 x Investigate','2 x Investigate','3 x Investigate','1 x Lore', '1 x Skull', '1 x Tentacles')

    @classmethod
    def yellow(cls):
        return cls('Yellow','1 x Investigate','2 x Investigate','3 x Investigate', '4 x Investigate','1 x Lore', '1 x Skull')

# maybe add sorting function and ordering as well as color 
#to order the dice and then only pop from the front will be more appropriate
class DicePool:
    def __init__(self) -> None:
        self.dice = [Die.green() for _ in range(6)]
    
    # is this the correct thing? Anthony said it was fine
    def __iter__(self) -> 'iterator':
        return iter(self.dice)

    def __getitem__(self,index) -> 'Die':
        return self.dice[index]
    
    def __str__(self) -> str:
        # something other than : and , should be used, things blend in
        dice_strs = [f"{index+1} = {str(die)}" for index, die in enumerate(self.dice)]
        return '; '.join(dice_strs)

    def __repr__(self) -> str:
        dice_reprs = [die.__repr__() for die in self.dice]
        print(dice_reprs)
        return ', '.join(dice_reprs)
    
    def __len__(self) -> int:
        return len(self.dice)

    def add_green(self) -> None:
        self.dice.append(Die.green())

    def add_yellow(self) -> None:
        self.dice.append(Die.yellow())

    def roll(self) -> None:
        for die in self.dice:
            die.roll()
    
    def pop(self, index:int=0) -> 'Die':
        # defaults to removing first die
        # this is because yellow and red dice will be appended and we 
        # probably don't want to remove those by default
        return self.dice.pop(index)
    

    def reset(self) -> None:
        self.dice = [Die.green() for _ in range(6)]
    
    # adding red dice
    # this requires figuring out wild first.
