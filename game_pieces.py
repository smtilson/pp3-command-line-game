# This file contains the game pieces that need to be loaded to play the game
from random import choice, shuffle
from typing import Optional, Union
import datetime
from utilities import print_dict, fit_to_screen, norm


class GreatOldOne:
    """
    Creates Great Old One enemy. Contains end condition thresholds.
    """
    def __init__(self, index:str, name:str, elder_signs:int, doom:int) -> None:
        self.index = index
        self.name = name
        self.doom = doom
        self.elder_signs = elder_signs

    def __str__(self) -> str:
        msg = f"{self.name}:   {self.doom} Doom to Awaken\n"
        msg += self.white_space * ' ' + f'{self.elder_signs} Elder Signs to '\
               'Banish'
        return msg
    
    @property
    def white_space(self) -> int:
        """
        Used for spacing in menus.
        """
        return (len(self.name) + 4 + self.extra[1]-self.extra[0])

    @property
    def extra(self) -> tuple[int,int]:
        """
        Used in spacing for menus.
        """
        length_doom = 2 - len(str(self.doom))
        length_elder = 2 - len(str(self.elder_signs))
        return length_doom, length_elder

    def selection(self) -> None:
        """
        Prints GreatOldOne in format for selection screen.
        """
        lines = str(self).split('\n')
        factor = len(self.name)-self.extra[0]+(len(str(self.index))-1)
        white_space = (14 - factor)*' '
        print(str(self.index)+'. '+lines[0].replace(': ',': '+white_space))
        print((21+self.extra[1])*' '+lines[1].strip())
    
class Investigator:
    """
    Creates Investigator that player plays as. Contains starting values.
    """
    def __init__(self, index:str, name:str, profession: str, sanity: int, 
                 health: int, items: list) -> None:
        self.index = index
        self.name = name
        self.profession = profession
        self.starting_sanity = sanity
        self.sanity = sanity
        self.starting_health = health
        self.health = health
        self.items = items

    def __str__(self) -> str:
        return f"{self.name}: {self.sanity} Sanity, {self.health} Health"
    
    @property
    def white_space(self) -> int:
        return 18-len(self.name)-len(str(self.index))

    def selection(self) -> None:
        """
        Prints Investigator in format for selection screen.
        """
        replacement = ': ' + self.white_space * ' '
        line = str(self.index) + '. ' + str(self).replace(': ', replacement)
        self.items.append('1 clue')
        # do I want to change this?
        line += ';     Items: ' + ', '.join(self.items).title()
        print(line)
    
    # Loss condition
    @property
    def alive(self) -> bool:
        if self.sanity <= 0 or self.health <= 0:
            return False
        return True
    

class Game:
    """
    Creates the game object. Manages win/loss conditions and game state.
    """
    def __init__(self, player: str, investigator:'Investigator', 
                 great_old_one: 'GreatOldOne', 
                 adventure_deck: list['Adventure'], 
                 item_deck: list['Item'], increment: int = 8) -> None:
        self.player = player
        self.investigator = investigator
        self.great_old_one = great_old_one
        self.current_doom = 0
        self.doom_max = great_old_one.doom
        self.current_elder_signs = 0
        self.elder_sign_max = great_old_one.elder_signs
        self.clock = Clock(increment)
        self.game_start_time = str(datetime.datetime.now())
        self.adventure_deck = adventure_deck
        self.adventure_discard = []
        shuffle(self.adventure_deck)
        self.item_deck = item_deck
        self.item_discard = []
        shuffle(self.item_discard)
        self.starting_items()
        self.dice_pool = DicePool()
    
    @property
    def num_dice(self) -> int:
        return len(self.dice_pool)

    def __str__(self) -> str:
        string = f"{self.great_old_one.name} has {self.current_doom}/"\
                 f"{self.doom_max} Doom.\n"
        string += f"{self.investigator.name} has {self.current_elder_signs}/"\
                  f"{self.elder_sign_max} Elder Signs.\n"
        string += str(self.clock) + '\n'
        string += str(self.investigator) + '\n'
        return string

    def end_turn(self) -> str:
        """
        End of turn clean up. Advances clock, applies doom, displays status,
        resets dice and returns end_condition. (should also handle the 
        adventure card stuff)
        """
        self.clock.advance()
        if self.clock.time == 24:
            self.current_doom += 1
        print(self)
        self.dice_pool.reset()
        return self.end_condition

    @property
    def end_condition(self) -> str:
        # Checks win condition first.
        if self.current_elder_signs >= self.elder_sign_max:
            return "Banished"
        elif self.current_doom >= self.doom_max:
            return "Summoned"
        elif not self.investigator.alive:
            return "Died"
        return ""
    
    def draw_adventure(self) -> 'Adventure':
        """
        Draws adventure card. Shuffles discard into deck if it is empty.
        """
        if len(self.adventure_deck) == 0:
            self.adventure_deck = [adv for adv in self.adventure_discard]
            self.adventure_discard = []
            shuffle(self.adventure_deck)
        return self.adventure_deck.pop(0)

    def discard_adventure(self, adventure: 'Adventure') -> None:
        """
        Resets adventure card to initial state. Adds to bottom of discard."
        """
        adventure.reset()
        self.adventure_discard.append(adventure)

    # should this return something instead?
    def draw_item(self, item_type: str) -> 'Item':
        """
        Draws item. If deck is empty, shuffles discard into deck.
        """
        item_type = norm(item_type)
        if len(self.item_deck) == 0:
            self.item_deck = [item for item in self.item_discard]
            self.item_discard = []
            shuffle(self.item_deck)
        if "clue" in item_type:
            return Item.clue()
        elif "spell" in item_type:
            return Item.spell()
        for index, item in enumerate(self.item_deck):
            if item.item_type.lower() == item_type.lower():
                self.item_deck.remove(item)
                return item
    
    def starting_items(self) -> None:
        starting_list = [term for term in self.investigator.items]
        self.investigator.items = []
        for term in starting_list:
            num, item_type = term.split()
            for _ in range(int(num)):
                item = self.draw_item(item_type)
                self.investigator.items.append(item)
        print(f"{self.investigator.name} starts with:")
        item_list = [item.name for item in self.investigator.items]
        string = fit_to_screen(', '.join(item_list))
        print(string)

    def pass_move(self) -> None:
        """
        Removes a die from the dice pool and rerolls remaining dice.
        """
        print("Losing a die.")
        self.dice_pool.pop()
        print("Rerolling dice.")
        self.dice_pool.roll()
        
        
class Clock:
    def __init__(self, increment: int) -> None:
        """
        Creates in game clock. Keeps track of when Doom needs to be assigned.
        """
        self.time = 0
        self. day = 0
        self.increment = increment
    
    def __str__(self) -> str:
        if self.time == 0:
            time = "midnight"
        else:
            time = str(self.time)+" o'clock"
        return f"It is {time} on Day {self.day}."
    
    def advance(self) -> None:
        self.time += self.increment
        if self.time == 24:
            self.time = 0
            self.day += 1

# ITEM_EFFECT functions, called when an Item is used
def add_yellow(game: 'Game') -> None:
    game.dice_pool.add_die('yellow')

def add_red(game: 'Game') -> None:
    game.dice_pool.add_die('red')

def add_yellow_n_red(game:'Game') -> None:
    game.dice_pool.add_die('yellow')
    game.dice_pool.add_die('red')

def gain_health(game:'Game') -> None:
    game.investigator.health += 1

def gain_sanity(game:'Game') -> None:
    game.investigator.sanity += 1

def add_spell_die(game:'Game') -> None:
    game.dice_pool.add_die('spell')

def reroll_dice(game:'game') -> None:
    print("Using a Clue to reroll dice.")
    game.dice_pool.roll()

def restore(game: 'Game') -> None:
    game.investigator.health = game.investigator.starting_health
    game.investigator.sanity = game.investigator.starting_sanity
    print("You are restored.")
    print(game.investigator)


class Item:
    # Dictionary for storing item functions.
    ITEM_EFFECT = {'Add a yellow die': add_yellow, 'Add a red die': add_red, 
                   'Gain 1 Health': gain_health, 'Gain 1 Sanity': gain_sanity, 
                   'Add a yellow and a red die': add_yellow_n_red, 
                   'Gain a wild die': add_spell_die, 
                   "Reroll all dice": reroll_dice, 
                   "Restore Health and Sanity": restore}

    def __init__(self, name:str, effect:str, item_type:str) -> None:
        """
        Creates Item object.
        """
        self.name = name
        self.effect = effect
        self.item_type = item_type
    
    # I think the following two are not used
    # def __str__(self) -> str:
     #   description = f"The {self.name} is a {self.item_type} item."\
      #                f"\nEffect: {self.effect}"
       # return description
    
    # def __repr__(self):
     #   return self.name + ': ' + self.item_type + ' item' + '\n' + self.effect

    @property
    def white_space(self) -> str:
        return (19-len(self.name)+3)*' '
          
    def use(self, game) -> None:
        """
        Uses item and then discards it.
        """
        self.ITEM_EFFECT[self.effect](game)
        game.investigator.items.remove(self)
        if self.item_type not in {'clue','spell'}:
            game.item_discard.append(self)
    
    @classmethod
    def clue(cls) -> 'Item':
        return Item("Clue", "Reroll all dice", "clue")

    @classmethod
    def spell(cls) -> 'Item':
        return Item("Spell", "Gain a wild die", "spell")


# Outcome functions for Adventure Rewards and Penalties
def gain_elder_sign(num: int, game: 'Game') -> None:
    game.current_elder_signs += num
    print(f"{game.investigator.name} now has {game.current_elder_signs} Elder Signs.")

def increase_doom(num: int, game: 'Game') -> None:
    game.current_doom += num
    print(f"There is {game.current_doom}/{game.doom_max} Doom.")
    
def change_sanity(num: int, game: 'Game') -> None:
    game.investigator.sanity += num
    print(f"{game.investigator.name} now has {game.investigator.sanity} Sanity .")

def change_health(num: int, game: 'Game') -> None:
    game.investigator.health += num
    print(f"{game.investigator.name} now has {game.investigator.health} Health.")
            
def draw_unique(num: int, game: 'Game') -> None:
    for _ in range(num):
        item = game.draw_item('unique')
        game.investigator.items.append(item)
        print(f"You got the {game.investigator.items[-1].name}")

def draw_common(num: int, game: 'Game') -> None:
    for _ in range(num):
        item = game.draw_item('common')
        game.investigator.items.append(item)
        print(f"You got the {game.investigator.items[-1].name}")

def gain_clue(num: int, game: 'Game') -> None:
    if num > 0:
        for _ in range(num):
            clue = game.draw_item('Clue')
            game.investigator.items.append(clue)
            print("You got a Clue.")
    else:
        for item in game.investigator.items:
            if item.item_type == "Clue":
                game.investigator.items.remove(item)
                print("You lost a Clue.")
                break
    
def gain_spell(num: int, game: 'Game') -> None:
    for _ in range(num):
        spell = game.draw_item('spell')
        game.investigator.items.append(spell)
        print("You got a Spell.")

# Dictionary for storing Reward and Penalty functions
OUTCOMES = {"Elder Sign": gain_elder_sign, "Sanity": change_sanity,
            "Health": change_health, "Doom": increase_doom,
            "Unique Item": draw_unique, "Unique Items": draw_unique,
            "Common Item": draw_common, "Common Items": draw_common,
            "Clue": gain_clue, "Spell": gain_spell, "Clues": gain_clue,
            "Spells": gain_spell}

class Task:
    def __init__(self, pattern: dict[str, int]) -> None:
        """
        Creates Task for Adventure cards.
        """
        self.pattern = pattern
        self.remaining = {key: value for key, value in pattern.items()}

    def __contains__(self, die: 'Die') -> bool:
        symbol = die.parse()[1]
        if symbol == 'Wild' and not self.complete:
            return True
        return die.parse()[1] in self.remaining.keys()

    def __str__(self) -> str:
        if self.complete:
            return "This task is complete."
        return print_dict(0, 3, self.remaining)

    def valid(self, dice_pool: 'DicePool') -> bool:
        """
        Checks if dice can make progress on given task.
        """
        for die in dice_pool:
            if die in self:
                return True
        return False

    def assign_die(self, die: 'Die') -> None:
        """
        Assigns die to task.
        """
        print(f"Assigning {str(die)}.")
        number, symbol = Die.parse(die)
        if symbol == 'Wild':
            symbol = self.assign_wild()
        self.remaining[symbol] -= number
        if self.remaining[symbol] <= 0:
            del self.remaining[symbol]
    
    def assign_wild(self) -> str:
        """
        Picks symbol for wild die.
        """
        selection = {str(index+1): key for index, key in 
                     enumerate(self.remaining.keys())}             
        for index, key in selection.items():
            if len(selection.items()) == 1:
                return selection[index]
            print(f'{index} = {key}')
        index = input("Please select a symbol to turn your Wild die into.\n")
        while index not in selection.keys():
            print(f"{index} is not a valid choice.")
            index = input("Please select a symbol to turn your Wild die into."
                          "\n")
        return selection[index]

    def suffer_penalty(self, investigator) -> 'Investigator':
        if "Health" in self.remaining.keys():
            amount = self.remaining['Health']
            print(f"You lose {abs(amount)} Health.")
            investigator.health += amount
            del self.remaining['Health']
        elif "Sanity" in self.remaining.keys():
            amount = self.remaining['Sanity']
            print(f"You lose {abs(amount)} Sanity.")
            investigator.sanity += amount
            del self.remaining['Sanity']
        return investigator

    def reset(self) -> None:
        """
        Resets task to initial state.
        """
        self.remaining = {key:value for key,value in self.pattern.items()} 

    @property
    def complete(self):
        for val in self.remaining.values():
            if val > 0:
                return False
        return True


class Adventure:
    """
    Creates Adventure "card". Contains text for flavor, tasks to complete,
    rewards and penalties. Displays information and controls game progression.
    """
    def __init__(self, name: str, flavor_text: str, tasks: list['Task'],
                 reward: dict[str: int], penalty: dict[str: int]) -> None:
        self.name = name
        self.flavor_text = flavor_text
        self.tasks = tasks
        self.reward = reward
        self.penalty = penalty

    def __str__(self) -> None:
        string = f"{self.name}\n\n"
        string += fit_to_screen("Flavor Text: " + self.flavor_text)
        string += "\n\n"
        for index, task in enumerate(self.tasks):
            string += f"Task {index + 1}: {str(task)}\n"
        string += f"Reward:  {print_dict(9, 3, self.reward)}\n"
        string += f"Penalty: {print_dict(9, 3, self.penalty)}\n"
        return string

    #is the right type hint just iter?
    def __iter__(self):
        return iter(self.tasks)

    def __getitem__(self, index: int) -> 'Task':
        return self.tasks[index]

    @property
    def remaining(self) -> list:
        return [task for task in self if not task.complete]
    
    @property
    def complete(self) -> bool:
        if len(self.remaining) == 0:
            return True
        return False

    def reset(self) -> None:
        for task in self:
            task.reset()


class Die:
    # Different die faces
    SYMBOLS = {'1 Investigate', '2 Investigate', '3 Investigate',
               '4 Investigate', '1 Lore', 'Lore 2', '1 Skulls', '1 Tentacles',
               '1 Wild'}
    # Data for different possible dice
    COLORS = {'green': ['1 Investigate', '2 Investigate', '3 Investigate',
                        '1 Lore', '1 Skulls', '1 Tentacles'],
              'yellow': ['1 Investigate', '2 Investigate', '3 Investigate',
                         '4 Investigate', '1 Lore', '1 Skulls'],
              'red': ['1 Wild', '2 Investigate', '3 Investigate',
                      '4 Investigate', '1 Lore', '1 Skulls'],
              'spell': ['1 Wild' for _ in range(6)]}

    def __init__(self, color: str, *faces: str) -> None:
        """
        Creates a die.
        """
        self.color = color
        self.faces = faces
        self.face = ''

    def __str__(self) -> str:
        return self.face

    def __repr__(self) -> str:
        return self.color + ': ' + self.face

    def __lt__(self, other: 'Die') -> bool:
        """
        Used to sort dice_pool before popping a die.
        """
        order = {'Green': 0, 'Yellow': 1, 'Red': 2, 'Spell': 3}
        return order[self.color] < order[other.color]

    def __eq__(self, other: 'Die') -> bool:
        """
        Used to sort dice_pool before popping a die.
        """
        return self.color == other.color

    @property
    def white_space(self) -> int:
        """
        Used for spacing on selection screen.
        """
        return len('3 Investigate')-len(str(self))
        
    def parse(self) -> tuple[int, str]:
        """
        Parses the face of the die. Returns number of symbols as int and
        symbol as string.
        """
        number, symbol = self.face.split(' ')
        number = int(number)
        return number, symbol

    def roll(self) -> None:
        # having a weird error where
        self.face = choice(self.faces)

    @classmethod
    def create_die(cls, color: str) -> 'Die':
        die = cls(color.capitalize(), *cls.COLORS[color])
        die.roll()
        return die


class DicePool:
    """
    Creates pool of dice. Has relevant methods for rolling, removing,
    displaying, and resetting dice at end of turn.
    """
    def __init__(self, defn: dict[str: int] = {'green': 6}) -> None:
        self.defn = defn
        self.dice = []
        for color in defn.keys():
            for _ in range(defn[color]):
                self.dice.append(Die.create_die(color))

    def __iter__(self):
        return iter(self.dice)

    def __getitem__(self, index: int) -> 'Die':
        return self.dice[index]

    @property
    def dice_strs(self) -> list[str]:
        """
        Creates list of spaced representations of dice in dice pool.
        """
        self.dice.sort()
        dice_strs = []
        for index, die in enumerate(self.dice):
            string = (2-len(str(index+1))) * ' ' + f"{index+1} -->  {str(die)}"
            string += (die.white_space+1)*" "
            dice_strs.append(string)
        return dice_strs
        
    def __str__(self) -> str:
        """
        Creates well spaced display of dice pool.
        """
        lines = []
        count = 0
        current = []
        for string in self.dice_strs:
            if count == 3:
                count = 0
                lines.append([part for part in current])
                current = []
            current.append(string)
            count += 1
        lines.append(current)
        lines = ['  '.join(line) for line in lines]
        string = 'Roll: '
        string += '\n      '.join(lines)
        return string

    def __repr__(self) -> str:
        self.dice.sort()
        dice_reprs = [die.__repr__() for die in self.dice]
        print(dice_reprs)
        return ', '.join(dice_reprs)

    def __len__(self) -> int:
        return len(self.dice)

    def add_die(self, color: str) -> None:
        die = Die.create_die(color)
        self.dice.append(die)

    def roll(self) -> None:
        for die in self.dice:
            die.roll()

    def pop(self, index: int = None) -> 'Die':
        # Defaults to removing first die
        if index is None:
            self.dice.sort()
            index = 0
        return self.dice.pop(index)

    def reset(self) -> None:
        self.dice = []
        for color in self.defn.keys():
            for _ in range(self.defn[color]):
                self.dice.append(Die.create_die(color))
