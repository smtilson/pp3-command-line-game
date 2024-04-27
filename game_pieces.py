# This file contains the game pieces that need to be loaded to play the game
from random import choice, shuffle
from typing import List, Optional, Tuple

#add some validation to this class
class GreatOldOne:
    """
    Creates Great Old One enemy.
    """
    def __init__(self, index:str, name:str, elder_signs:int, doom:int,ability:str) -> None:
        self.index = index
        self.name = name
        self.doom = doom
        self.elder_signs = elder_signs
        self.ability = ability # this should be replaced by something later, I now, a custom function will be stored here.

    #should this be a display mehtod instead?
    def __str__(self):
        msg = f"{self.name}: {self.doom} Doom needed to Awaken\n"
        # this length should eventually be replaced by max name length for the class.
        msg += (len(self.name)+2-self.extra)*' '+f'{self.elder_signs} Elder Signs needed to Banish'
        return msg
    
    @property
    def extra(self):
        doom = str(self.doom)
        elder_signs = str(self.elder_signs)
        length = len(elder_signs)-len(doom)
        #print(doom, len(doom))
        #print(elder_signs, len(elder_signs))
        #print(length, length*' ')
        return length

    def selection(self):
        lines = str(self).split('\n')
        white_space = (14-len(self.name)+self.extra)*' '
        print(str(self.index)+'. '+lines[0].replace(': ',': '+white_space))
        # 19 =14 from name +2+3
        print(19*' '+lines[1].strip())
    
class Investigator:
    def __init__(self, index:str, name:str, profession: str, sanity: int, health: int, ability: str, items: list=None) -> None:
        # maybe these will be added to or removed
        # could have special dice
        # start with no items in example
        self.index = index
        self.name = name
        if sanity <= 0 or health <= 0:
            raise ValueError(f"{sanity=} and {health=} are not a starting values.")
        self.starting_sanity = sanity
        self.sanity = sanity
        self.starting_health = health
        self.health = health
        # setting up the items for the character is maybe an issue.
        # that method is part of the game class.
        # is this still necessary?
        if items:
            self.items = items
        else:
            self.items = []
        # self.dice = 6 # this val will be modified, reset it at the beginning of each turn or at the end of each turn.
        self.dice_pool = DicePool()
    # modify this later for selection etc
    def __str__(self):
        return f"{self.name}: {self.sanity} Sanity, {self.health} Health"
    
    def __len__(self):
        return len(self.dice_pool)

    def selection(self):
        white_space = (18-len(self.name)-len(str(self.index)))*' '
        print(str(self.index)+'. '+str(self).replace(': ',': '+white_space))
    
    # Loss condition
    @property
    def alive(self) -> bool:
        if self.sanity <= 0 or self.health <= 0:
            return False
        else:
            return True

    # Adjust health accordingly
    def lose_sanity(self, damage: int) -> None:
        self.sanity -= damage
        if self.sanity < 0:
            self.sanity = 0
    
    def lose_health(self, damage: int) -> None:
        self.health -= damage
        if self.health < 0:
            self.health = 0
    # there should maybe be a more detailed version of this
    # or an inspect item to see what the item does
    def list_items(self) -> None:
        for index,item in enumerate(self.items):
            print(index+1, item.name, item.effect)
    
    def roll(self) -> None:
        self.dice_pool.roll()

    def add_die(self, color: str) -> None:
        self.dice_pool.add_die(color)

    def pass_move(self) -> None:
        """
        Removes a die from the dice pool and rerolls remaining dice.
        """
        print("Sacrificing a die.")
        self.dice_pool.pop()
        print("Rerolling your remaining dice.")
        # will roll throw an exception if there are no dice?
        self.roll()


    # advances clock, check alive and resets number of die
    def reset(self):
        # This resets the dice pool and the face of each die to initial face
        print(f"{self.name} is still alive.")
        self.dice_pool.reset()

    # should the Item effect dictionary be here?
    # how relevant is this?
    # this seems convoluted and not streamlined.
    # moving the item effect dictionary would help that, I think.
    def use_item(self, index) -> None:
        item = self.items.pop(index)
        item.use(self)

        
# needs validation
# needs overflow check method maybe? <- wtf does this mean



class Game:
    def __init__(self, investigator, great_old_one, start_time, task_card_deck, item_deck) -> None:
        self.investigator = investigator
        self.great_old_one = great_old_one
        self.current_doom = 0
        self.doom_max = great_old_one.doom
        self.current_elder_signs = 0
        self.elder_sign_max = great_old_one.elder_signs
        self.clock = Clock(start_time)
        # not yet fully implimented
        self.task_card_deck = task_card_deck #TaskCard.create_deck()
        self.current_task_cards = []
        self.refill_task_cards()
        self.item_deck = item_deck
        self.starting_items()
    
    # should this be __str__?
    def status(self) -> str:
        print(f"{self.great_old_one.name} only needs {-self.current_doom + self.doom_max} more Doom to awaken.")
        print(f"You only need {-self.current_elder_signs + self.elder_sign_max} more Elder Signs.")
        print(f"The time is {self.clock.time} o'clock.")

    def end_turn(self) -> str:
        self.clock.advance()
        if self.clock.time == 12:
            self.apply_doom(1)
        self.investigator.reset()
        self.refill_task_cards()
        self.status()
        return self.end_condition
    
    def apply_doom(self, num:int) -> None:
        self.current_doom += num
        print(f"There is {self.current_doom}/{self.doom_max} Doom.")

    # Loss condition
    @property
    def great_old_one_summoned(self) -> bool:
        if self.current_doom >= self.doom_max:
            print(f"The terrifying {self.great_old_one.name} has been summoned and devours the world.")
            return True
        else:
            # should there be a message here
            return False
    
        # Win condition
    @property
    def great_old_one_banished(self) -> bool:
        if self.current_elder_signs >= self.elder_sign_max:
            print(f"You have defeated the terrifying {self.great_old_one.name}. The world is forever in your debt.")
            return True
        else:
            # should there be a message here
            return False

    @property
    def end_condition(self) -> str:
        if self.great_old_one_summoned:
            return "Summoned"
        elif self.great_old_one_banished:
            return "Banished"
        elif not self.investigator.alive:
            return "Died"
        else:
            return ""

#    commented out until the TaskCard.create_deck() function is written
    def refill_task_cards(self) -> None:
        # the number of active cards is also a parameter that can be messed with
        #print("refill called")
        #print(len(self.current_task_cards))
        while len(self.current_task_cards) < 3:
            self.draw_task_card()
        #print("Task cards replenished.")
        #print(len(self.current_task_cards))
    
    def draw_task_card(self) -> None:
        task_card = self.task_card_deck.pop(0)
        self.current_task_cards.append(task_card)
   
    def discard_completed_task_card(self, task_card) -> None:
        task_card.reset()
        self.task_card_deck.append(task_card)
    
    def shuffle(self) -> None:
        shuffle(self.task_card_deck)
        shuffle(self.item_deck)
    
    def draw_item(self, item_type) -> None:
        #self.shuffle()
        for item in self.item_deck:
            if item.item_type == item_type:
                break
        self.item_deck.remove(item)
        self.investigator.items.append(item)
    
    def starting_items(self) -> None:
        starting_list = [term for term in self.investigator.items]
        self.investigator.items = []
        for term in starting_list:
            num, item_type = term.split()
            for _ in range(int(num)):
                self.draw_item(item_type)
        
        
class Clock:
    #This is where the difficulty setting could be, the number of turns in a day.
    def __init__(self, start_time):
        self.time = start_time
    
    #how many hours are in the day
    def advance(self) -> None:
        self.time += 3
        if self.time == 12:
            print("It is midnight!")
        elif self.time == 15:
            self.time = 3
        print(f'The time is now {self.time}.')
            
    def check_clock(self) -> None:
        print(f"It is currently {self.time} o'clock.")
        print(f"You have {(12-self.time)//3} turns until doom advances.")

def add_yellow(investigator:'Investigator') -> None:
    investigator.add_die('yellow')

def add_red(investigator:'Investigator') -> None:
    investigator.add_die('red')

def add_yellow_n_red(investigator:'Investigator') -> None:
    investigator.add_die('yellow')
    investigator.add_die('red')

def gain_health(investigator:'Investigator') -> None:
    investigator.health += 1

def gain_sanity(investigator:'Investigator') -> None:
    investigator.sanity += 1

# a clue behaves like an item but it isn't in the item deck.
# or just make clue a item_type
#maybe same with spell, but make it assign a wild die.
# I guess when I write the gain_clue reward function I will just make an item in that function and add it to the inventory.
class Item:
    ITEM_EFFECT = {'Adds yellow die':add_yellow, 'Adds red die':add_red, 'Gain 1 Health':gain_health,
                    'Gain 1 Sanity':gain_sanity,#'Change 1 die to Skulls':change_to_skull, 
                    'Adds yellow and red dice':add_yellow_n_red}
    def __init__(self, name:str, effect:str, item_type:str) -> None:
        self.name = name
        self.effect = effect
        self.item_type = item_type
    
    def __str__(self) -> str:
        return f"The {self.name} is a {self.item_type} item.\nEffect: {self.effect}"

    def use(self, investigator):
        self.ITEM_EFFECT[self.effect](investigator)

def gain_elder_sign(num:int, game:'Game') -> None:
    game.current_elder_signs += num
    print(f"{game.investigator.name} now has {game.current_elder_signs} Elder Signs.")

def increase_doom(num:int, game:'Game') -> None:
    game.apply_doom(num)
    
def change_sanity(num:int, game:'Game') -> None:
    game.investigator.sanity += num
    print(f"{game.investigator.name} now has {game.investigator.sanity} Sanity .")

def change_health(num:int, game:'Game') -> None:
    game.investigator.health += num
    print(f"{game.investigator.name} now has {game.investigator.health} Health.")

def draw_unique(num:int, game:'Game') -> None:
    for _ in range(num):
        game.draw_item('Unique')
    game.investigator.list_items()

def draw_common(num:int, game:'Game') -> None:
    for _ in range(num):
        game.draw_item('Common')
    game.investigator.list_items()
    
OUTCOMES = {"Elder Sign": gain_elder_sign,
            "Sanity": change_sanity,
            "Health": change_health,
            "Doom": increase_doom,
            "Unique Item": draw_unique,
            "Common Item": draw_common}

class Task:
    TRANSLATION = {'Inv.': 'Investigate', 'Investigation':'Investigate', 'Lore':'Lore', 
                    'Peril':'Skulls', 'Terror': 'Tentacles','Unique':'Unique Item', 
                    'Common': 'Common Item', 'Elder':'Elder Sign', 'Clues':'Clues','Clue':'Clue', 
                    'Sanity':'Sanity','Stamina':'Health', 'Doom':'Doom', 'unique item': 'Unique',
                    'common item': 'Common', 'spell':'Unique'}#spell can be changed to clue once clues are written.
    def __init__(self, pattern:dict) -> None:
        #needs validation that pattern is acceptable
        self.pattern = pattern
        self.remaining = {key:value for key,value in pattern.items()}

    def __contains__(self, die) -> bool:
        symbol = die.parse()[1]
        if symbol == 'Wild' and not self.complete:
            return True
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
        if symbol == 'Wild':
            symbol = self.assign_wild()
            #print(symbol)
        self.remaining[symbol] -= number
        if self.remaining[symbol] <= 0:
            del self.remaining[symbol]
    
    #I can use get selection here now.
    def assign_wild(self) -> str:
        selection = {str(index+1):key for index, key in enumerate(self.remaining.keys())}
        for index, key in selection.items():
            print(f'{index} = {key}')
        index = input("Please select a symbol to turn your Wild die into.\n")
        while index not in selection.keys():
            print(f"{index} is not a valid choice.")
            index = input("Please select a symbol to turn your Wild die into.\n")
        return selection[index]
    
    def suffer_penalty(self, investigator) -> 'Investigator':
        #if 
        #sort, amount = penalty.split(': ')
        #print(sort, amount)
        return investigator
       
    # resets task for next attempt, if at all
    # eventually this will be removed
    # why was I going to remove this?
    def reset(self) -> None:
        self.remaining = {key:value for key,value in self.pattern.items()} 
    
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
    def __init__(self, name: str, flavor_text:str, tasks: List['Task'], reward: str, penalty: str) -> None:
        self.name = name
        self.flavor_text = flavor_text
        self.tasks = tasks
        self.reward = reward
        self.penalty = penalty

    #this should only be called after selecting a task.
    def display(self):
        pass

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
    SYMBOLS = {'Investigate: 1','Investigate: 2','Investigate: 3','Investigate: 4','Lore: 1','Lore: 2', 'Skulls: 1', 'Tentacles: 1', 'Wild: 1'}
    COLORS = {'green':['Investigate: 1','Investigate: 2','Investigate: 3','Lore: 1', 'Skulls: 1', 'Tentacles: 1'], 
                'yellow':['Investigate: 1','Investigate: 2','Investigate: 3','Investigate: 4','Lore: 1', 'Skulls: 1'],
                'red':['Wild: 1','Investigate: 2','Investigate: 3','Investigate: 4','Lore: 1', 'Skulls: 1'],
                'blue':['Wild: 1' for _ in range(6)]}
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
    def create_die(cls,color:str):
        if color not in cls.COLORS.keys():
            raise ValueError(f"{color} is not a valid color of die")
        return cls(color.capitalize(),*cls.COLORS[color])
# maybe add sorting function and ordering as well as color 
#to order the dice and then only pop from the front will be more appropriate
class DicePool:
    def __init__(self, defn:dict={'green':5,'yellow':2,'red':2, 'blue':1}) -> None:
        self.defn = defn
        self.dice = []
        for color in defn.keys():
            for _ in range(defn[color]):
                self.dice.append(Die.create_die(color))
    
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
        die = Die.create_die(color)
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
        #print("Dice pool is being reset.")
        self.dice = []
        for color in self.defn.keys():
            for _ in range(self.defn[color]):
                self.dice.append(Die.create_die(color))
    
    # adding red dice
    # this requires figuring out wild first.
