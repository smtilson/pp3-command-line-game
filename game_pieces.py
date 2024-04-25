# This file contains the game pieces that need to be loaded to play the game
from random import choice, shuffle
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
    def __init__(self, name:str, sanity: int, stamina: int, items: list=None) -> None:
        # maybe these will be added to or removed
        # could have special dice
        # start with no items in example
        self.name = name
        if sanity <= 0 or stamina <= 0:
            raise ValueError(f"{sanity=} and {stamina=} are not a starting values.")
        self.starting_sanity = sanity
        self.sanity = sanity
        self.starting_stamina = stamina
        self.stamina = stamina
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
    def lose_sanity(self, damage: int) -> None:
        self.sanity -= damage
        if self.sanity < 0:
            self.sanity = 0
    
    def lose_stamina(self, damage: int) -> None:
        self.stamina -= damage
        if self.stamina < 0:
            self.stamina = 0
    
    
    def roll_dice(self) -> None:
        self.dice_pool.roll()

    def add_die(self, color: str) -> None:
        self.dice_pool.add_die(color)

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
    def __init__(self, character, great_old_one, task_card_deck) -> None:
        self.character = character
        self.great_old_one = great_old_one
        self.clock = Clock()
        # not yet fully implimented
        self.task_card_deck = task_card_deck #TaskCard.create_deck()
        self.current_task_cards = []
        self.refill_task_cards()
    
    def end_turn(self) -> str:
        self.clock.advance()
        self.apply_doom()
        self.character.reset()
        self.refill_task_cards()
        return self.end_condition
    
    def apply_doom(self) -> None:
        if self.clock.time == 12:
            print("Applying doom.")
            self.great_old_one.current_doom += 1
            print(f"There is {self.great_old_one.current_doom} out of {self.great_old_one.doom_threshold}.")

    @property
    def end_condition(self) -> str:
        if self.great_old_one.summoned:
            return "Summoned"
        elif self.great_old_one.banished:
            return "Banished"
        elif not self.character.alive:
            return "Died"
        else:
            return ""

#    commented out until the TaskCard.create_deck() function is written
    def refill_task_cards(self) -> None:
        # the number of active cards is also a parameter that can be messed with
        while len(self.current_task_cards) < 3:
            self.draw_task_card()
    
    def draw_task_card(self) -> None:
        task_card = self.task_card_deck.pop(0)
        self.current_task_cards.append(task_card)
   
    def discard_completed_task_card(self, task_card) -> None:
        self.task_card_deck.append(task_card)
    
    def shuffle(self) -> None:
        shuffle(self.task_card_deck)

class Clock:
    #This is where the difficulty setting could be, the number of turns in a day.
    def __init__(self):
        self.time = 0
    
    #how many hours are in the day
    def advance(self) -> None:
        self.time += 3
        if self.time == 12:
            print("It is midnight!")
        elif self.time == 15:
            self.time = 3
            
    def check_clock(self) -> None:
        print(f"It is currently {self.time} o'clock.")
        print(f"You have {(12-self.time)//3} turns until doom advances.")


def elder_sign(num:int, game:'Game') -> None:
    game.great_old_one.current_elder_signs += num
    
def damage_sanity(num:int, game:'Game') -> None:
    game.character.sanity -= num
    
def damage_stamina(num:int, game:'Game') -> None:
    game.character.stamina -= num

OUTCOMES = {"Elder Sign":elder_sign,
            "Sanity":damage_sanity,
            "Stamina":damage_stamina}

class Task:
    def __init__(self, pattern:dict) -> None:
        #needs validation that pattern is acceptable
        self.pattern = pattern
        self.remaining = pattern

    def __contains__(self, die) -> bool:
        return die.parse()[1] in self.remaining.keys()

    def __str__(self):
        if self.complete:
            return "This task is complete."
        return f"Remaining: {self.remaining}"
    
    #should this be different?
    def __repr__(self):
        return self.__str__()

    # is this still necessary?    
    def valid(self, dice_pool) -> bool:
        for die in dice_pool:
            if die in self:
                return True
        return False

    def assign_die(self, die:'Die') -> None:
        print(f"Assigning die with {str(die)} to {self.remaining}.")
        number, symbol = Die.parse(die)
        self.remaining[symbol] -= number
        if self.remaining[symbol] <= 0:
            del self.remaining[symbol]
    
    # def assign_die_from_pool(self, dice_pool) -> 'DicePool':

       
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
    SYMBOLS = {'Investigate: 1','Investigate: 2','Investigate: 3','Investigate: 4','Lore: 1','Lore: 2', 'Skull: 1', 'Tentacles: 1'}
    COLORS = {'green':['Investigate: 1','Investigate: 2','Investigate: 3','Lore: 1', 'Skull: 1', 'Tentacles: 1'], 
                'yellow':['Investigate: 1','Investigate: 2','Investigate: 3','Investigate: 4','Lore: 1', 'Skull: 1']}
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
        symbol, number = self.face.split(': ')
        number = int(number)
        return number, symbol

    def roll(self) -> None:
        # having a weird error where
        self.face = choice(self.faces)
    
    @classmethod
    def create_die_by_color(cls,color):
        if color not in cls.COLORS.keys():
            raise ValueError(f"{color} is not a valid color of die")
        return cls(color.capitalize(),*cls.COLORS[color])
# maybe add sorting function and ordering as well as color 
#to order the dice and then only pop from the front will be more appropriate
class DicePool:
    def __init__(self) -> None:
        self.dice = [Die.create_die_by_color('green') for _ in range(6)]
    
    # is this the correct thing? Anthony said it was fine
    def __iter__(self) -> 'iterator':
        return iter(self.dice)

    def __getitem__(self,index) -> 'Die':
        return self.dice[index]
    
    def __str__(self) -> str:
        # something other than : and , should be used, things blend in
        dice_strs = [f"{index+1} = {str(die)}" for index, die in enumerate(self.dice)]
        return 'Your roll: '+'; '.join(dice_strs)

    def __repr__(self) -> str:
        dice_reprs = [die.__repr__() for die in self.dice]
        print(dice_reprs)
        return ', '.join(dice_reprs)
    
    def __len__(self) -> int:
        return len(self.dice)

    def add_die(self, color:str) -> None:
        die = Die.create_die_by_color(color)
        self.dice.append(die)

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
