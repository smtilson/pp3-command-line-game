# This file contains the game pieces that need to be loaded to play the game
from random import choice, shuffle
from typing import Optional, Union
import datetime
from utilities import print_dict, fit_to_screen, norm


class GreatOldOne:
    """
    Creates Great Old One enemy.
    """
    def __init__(self, index:str, name:str, elder_signs:int, doom:int) -> None:
        self.index = index
        self.name = name
        self.doom = doom
        self.elder_signs = elder_signs

    #should this be a display mehtod instead?
    def __str__(self):
        msg = f"{self.name}:   {self.doom} Doom to Awaken\n"
        white_space = (len(self.name)+4+self.extra[1]-self.extra[0])*' '
        msg += white_space + f'{self.elder_signs} Elder Signs to Banish'
        return msg
    
    @property
    def extra(self):
        doom = str(self.doom)
        elder_signs = str(self.elder_signs)
        length_doom = 2 - len(doom)
        length_elder = 2 - len(elder_signs)
        return length_doom, length_elder

    def selection(self):
        lines = str(self).split('\n')
        factor = len(self.name)-self.extra[0]+(len(str(self.index))-1)
        white_space = (14 - factor)*' '
        print(str(self.index)+'. '+lines[0].replace(': ',': '+white_space))
        print((21+self.extra[1])*' '+lines[1].strip())
    
class Investigator:
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

    def __str__(self):
        return f"{self.name}: {self.sanity} Sanity, {self.health} Health"
    
    def selection(self):
        white_space = (18-len(self.name)-len(str(self.index)))*' '
        line = str(self.index)+'. '+str(self).replace(': ',': '+white_space)
        self.items.append('1 clue')
        line += ';     Items: ' + ', '.join(self.items).title()
        print(line)
    
    # Loss condition
    @property
    def alive(self) -> bool:
        if self.sanity <= 0 or self.health <= 0:
            return False
        else:
            return True
    

class Game:
    def __init__(self, player:str, investigator:'Investigator', 
                 great_old_one:'GreatOldOne', adventure_deck:list['Adventure'], 
                 item_deck:list['Item'], increment:int=8) -> None:
        """
        Creates the game object. Manages win/loss conditions and game state.
        """
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
        self.item_deck = item_deck
        self.item_discard = []
        self.shuffle()
        self.starting_items()
        self.dice_pool = DicePool()
    
    @property
    def num_dice(self) -> int:
        return len(self.dice_pool)

    # should this be __str__?
    def status(self) -> str:
        if not self.great_old_one_summoned:
            print(f"{self.great_old_one.name} has {self.current_doom}/{self.doom_max} Doom.")
        if not self.great_old_one_banished:
            print(f"{self.investigator.name} has {self.current_elder_signs}/{self.elder_sign_max} Elder Signs.")
        print(self.clock)
        print(self.investigator)

    def end_turn(self) -> str:
        self.clock.advance()
        if self.clock.time == 24:
            self.apply_doom(1)
        # self.investigator.reset()
        # self.refill_adventures()
        self.status()
        self.dice_pool.reset()
        return self.end_condition
    
    def apply_doom(self, num:int) -> None:
        self.current_doom += num
        print(f"There is {self.current_doom}/{self.doom_max} Doom.")

    # Loss condition
    @property
    def great_old_one_summoned(self) -> bool:
        if self.current_doom >= self.doom_max:
            return True
        else:
            #print(f"Only {self.doom_max-self.current_doom} more Doom is needed to "\
            #      f"summon {self.great_old_one.name} to this plane of "\
            #      "existence.")
            return False
    
    # Win condition
    @property
    def great_old_one_banished(self) -> bool:
        if self.current_elder_signs >= self.elder_sign_max:
            return True
        else:
            #print(f"Only {self.elder_sign_max-self.current_elder_signs} more Elder "\
            #      f"Signs are needed to banish {self.great_old_one.name} and "\
            #      "save the world.")
            return False

    @property
    def end_condition(self) -> str:
        if self.great_old_one_banished:
            return "Banished"
        elif self.great_old_one_summoned:
            return "Summoned"
        elif not self.investigator.alive:
            return "Died"
        else:
            return ""
    
    def draw_adventure(self) -> None:
        if len(self.adventure_deck) == 0:
            self.adventure_deck = [adv for adv in self.adventure_discard]
            self.adventure_discard = []
            shuffle(self.adventure_deck)
        return self.adventure_deck.pop(0)

    def discard_adventure(self, adventure) -> None:
        adventure.reset()
        self.adventure_discard.append(adventure)
    
    def shuffle(self) -> None:
        shuffle(self.adventure_deck)
        shuffle(self.item_deck)

    def draw_item(self, item_type) -> None:
        item_type = norm(item_type)
        if len(self.item_deck) == 0:
            self.item_deck = [item for item in self.item_discard]
            self.item_discard = []
            shuffle(self.item_deck)
        if "clue" in item_type:
            clue = Item.clue()
            self.investigator.items.append(clue)
            return
        elif "spell" in item_type:
            spell = Item.spell()
            self.investigator.items.append(spell)
            return
        elif item_type in {"common", "unique"}:
            for index, item in enumerate(self.item_deck):
                if item.item_type.lower() == item_type.lower():
                    self.item_deck.remove(item)
                    self.investigator.items.append(item)
                    return
        else:
            print("in else block of draw_item")
            print(self.investigator.name)
            print(item_type)
            input()
    
    def starting_items(self) -> None:
        starting_list = [term for term in self.investigator.items]
        #print(starting_list)
        #input()
        self.investigator.items = []
        for term in starting_list:
            num, item_type = term.split()
            for _ in range(int(num)):
                self.draw_item(item_type)
                #print(self.investigator.items[-1].name)
        #self.draw_item("clue")
        print(f"{self.investigator.name} starts with:")
        item_list = [item.name for item in self.investigator.items]
        string = ', '.join(item_list)
        print(string)
        #print(fit_to_screen(string, ', '))

    def pass_move(self) -> None:
        """
        Removes a die from the dice pool and rerolls remaining dice.
        """
        print("Sacrificing a die.")
        self.dice_pool.pop()
        print("Rerolling your remaining dice.")
        self.dice_pool.roll()
        
        
class Clock:
    def __init__(self, increment:int):
        """
        Creates the in game clock.
        """
        self.time = 0
        self. day = 0
        self.increment = increment
    
    def __str__(self):
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
    #print("Using a Clue to reroll dice.")
    game.dice_pool.roll()

def restore(game: 'Game') -> None:
    game.investigator.health = game.investigator.starting_health
    game.investigator.sanity = game.investigator.starting_sanity

# a clue behaves like an item but it isn't in the item deck.
# or just make clue a item_type
#maybe same with spell, but make it assign a wild die.
# I guess when I write the gain_clue reward function I will just make an item in that function and add it to the inventory.
class Item:
    ITEM_EFFECT = {'Add a yellow die': add_yellow, 'Add a red die': add_red, 'Gain 1 Health': gain_health,
                   'Gain 1 Sanity': gain_sanity,#'Change 1 die to Skulls':change_to_skull, 
                   'Add a yellow and a red die': add_yellow_n_red, 'Gain a wild die': add_spell_die, 
                   "Reroll all dice":reroll_dice, "Restore Health and Sanity": restore}

    def __init__(self, name:str, effect:str, item_type:str) -> None:
        self.name = name
        self.effect = effect
        self.item_type = item_type
    
    def __str__(self):
        description = f"The {self.name} is a {self.item_type} item."\
                      f"\nEffect: {self.effect}"
        return description
    
    def __repr__(self):
        return self.name + ': ' + self.item_type + ' item' + '\n' + self.effect

    @property
    def white_space(self) -> str:
        return (19-len(self.name)+3)*' '
          
    def use(self, game):
        self.ITEM_EFFECT[self.effect](game)
        game.investigator.items.remove(self)
        if self.item_type not in {'clue','spell'}:
            game.item_discard.append(self)
        
        #This is how it will be after the refactor
        #self.ITEM_EFFECT[self.effect](game.investigator)
        #game.investigator.items.remove(self)
        #game.item_discard.append(self)
    
    @classmethod
    def clue(cls) -> 'Item':
        return Item("Clue", "Reroll all dice", "clue")

    @classmethod
    def spell(cls) -> 'Item':
        return Item("Spell", "Gain a wild die", "spell")

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

def gain_item(num: int, game: 'Game', item_type: str) -> None:
    if num > 0:
        for _ in range(num):
            game.draw_item(item_type)

def draw_unique(num:int, game:'Game') -> None:
    for _ in range(num):
        game.draw_item('unique')
        print(f"You got the {game.investigator.items[-1].name}")

def draw_common(num:int, game:'Game') -> None:
    for _ in range(num):
        game.draw_item('common')
        print(f"You got the {game.investigator.items[-1].name}")

def gain_clue(num:int, game:'Game') -> None:
    if num > 0:
        for _ in range(num):
            game.draw_item('Clue')
            print(f"You got a Clue.")
    else:
        for item in game.investigator.items:
            if item.item_type == "Clue":
                game.investigator.items.remove(item)
                print("You lost a Clue.")
                break
    
def gain_spell(num:int, game:'Game') -> None:
    for _ in range(num):
            game.draw_item('spell')
            print(f"You got a Spell.")

OUTCOMES = {"Elder Sign": gain_elder_sign,
            "Sanity": change_sanity,
            "Health": change_health,
            "Doom": increase_doom,
            "Unique Item": draw_unique,
            "Common Item": draw_common,
            "Clue": gain_clue,
            "Spell": gain_spell,
            "Clues": gain_clue,
            "Spells": gain_spell}

class Task:
    # clean up this translation dictionary
    # to do this look at where I am using this and what for.
    TRANSLATION = {'Inv.': 'Investigate', 'Investigation':'Investigate', 
                   'Lore':'Lore', 'Peril':'Skulls', 'Terror': 'Tentacles',
                   'Unique':'Unique Item', 'Common': 'Common Item', 
                   'Elder':'Elder Sign', 'Clues':'Clues','Clue':'Clue', 
                   'Sanity':'Sanity','Stamina':'Health', 'Doom':'Doom', 
                   'unique item': 'Unique', 'common item': 'Common', 
                   'spell':'Spell', 'Spells':'Spells', 'Spell':'Spell'}
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
        return print_dict(0, 3, self.remaining)
    
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
        selection = {str(index+1):key for index, key in 
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
        self.remaining = {key:value for key,value in self.pattern.items()} 

    @property
    def complete(self):
        for val in self.remaining.values():
            if val > 0:
                return False
        return True


class Adventure:
    """
    Create Adventure "card". Contains text for flavor, tasks to complete,
    rewards and penalties. Displays information and controls game progression.
    """
    def __init__(self, name: str, flavor_text: str, tasks: list['Task'],
                 reward: dict, penalty: dict) -> None:
        self.name = name
        self.flavor_text = flavor_text
        self.tasks = tasks
        self.reward = reward
        self.penalty = penalty

    def __str__(self):
        string = f"{self.name}\n\n"
        string += fit_to_screen("Flavor Text: " + self.flavor_text)
        string += "\n\n"
        for index, task in enumerate(self.tasks):
            string += f"Task {index + 1}: {str(task)}\n"
        string += f"Reward:  {print_dict(9, 3, self.reward)}\n"
        string += f"Penalty: {print_dict(9, 3, self.penalty)}\n"
        return string

    def __iter__(self):
        return iter(self.tasks)

    def __getitem__(self, index) -> 'Task':
        return self.tasks[index]

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


class Die:
    SYMBOLS = {'1 Investigate', '2 Investigate', '3 Investigate',
               '4 Investigate', '1 Lore', 'Lore 2', '1 Skulls', '1 Tentacles',
               '1 Wild'}
    COLORS = {'green': ['1 Investigate', '2 Investigate', '3 Investigate',
                        '1 Lore', '1 Skulls', '1 Tentacles'],
              'yellow': ['1 Investigate', '2 Investigate', '3 Investigate',
                         '4 Investigate', '1 Lore', '1 Skulls'],
              'red': ['1 Wild', '2 Investigate', '3 Investigate',
                      '4 Investigate', '1 Lore', '1 Skulls'],
              'spell': ['1 Wild' for _ in range(6)]}

    def __init__(self, color, *faces: str) -> None:
        self.color = color
        self.faces = faces
        self.face = ''

    def __str__(self) -> str:
        return self.face

    def __repr__(self) -> str:
        return self.color + ': ' + self.face

    def __lt__(self, other: 'Die') -> bool:
        order = {'Green': 0, 'Yellow': 1, 'Red': 2, 'Spell': 3}
        return order[self.color] < order[other.color]

    def __eq__(self, other: 'Die') -> bool:
        return self.color == other.color

    @property
    def white_space(self):
        return len('3 Investigate')-len(str(self))
        

    def parse(self):
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
    def create_die(cls, color: str):
        die = cls(color.capitalize(), *cls.COLORS[color])
        die.roll()
        return die


class DicePool:
    """
    Objects contains dice and relevant methods for rolling, removing,
    displaying, and resetting dice at end of turn.
    """
    def __init__(self, defn: dict[str:int] = {'green': 6}) -> None:
        self.defn = defn
        self.dice = []
        for color in defn.keys():
            for _ in range(defn[color]):
                self.dice.append(Die.create_die(color))

    # Iterator type hint?
    def __iter__(self):
        return iter(self.dice)

    def __getitem__(self, index: int) -> 'Die':
        return self.dice[index]

    def __str__(self) -> str:
        # something other than : and , should be used, things blend in
        self.dice.sort()
        # I could write a method for a die called display which addressed
        # this. a bit.
        dice_strs = []
        for index, die in enumerate(self.dice):
            string = (2-len(str(index+1))) * ' ' + f"{index+1} -->  {str(die)}"
            string += (die.white_space+1)*" "
            dice_strs.append(string)
        lines = []
        count = 0
        current = []
        #print(dice_strs)
        for string in dice_strs:
            if count == 3:
                count = 0
                lines.append([part for part in current])
                current = []
            current.append(string)
            count += 1
        lines.append(current)
        string =  'Roll: '
        lines = ['  '.join(line) for line in lines]
        string += '\n      '.join(lines)
        #for line in lines:
         #   string += '  '.join(line)
          #  string += '\n      '
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
