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
    def __init__(self, name:str, health:int, challenges:tuple, attack:str) -> None:
        self.name = name
        if health <=0:
            raise ValueError(f"{health} is not a valid starting health value.")
        self.starting_health = health
        self.health = health
        self.challenges = challenges
        self.attack = attack # this should be replaced by something later
    
    # Current win condition
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
    
    # should this be check challenges?
    def check_challenge(self, challenge, die_sequence):
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
        self.dice = 6
        self.current_roll = ['' for _ in range(6)]

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
    def attempt_challenge(self, index:int, challenge) -> None:
        die = self.current_roll.pop(index)
        try:
            challenge.add_die(die)
        except ValueError as e:
            print(e)
            self.current_roll.append(die)
            print("Select a different challenge.")
    
# needs validation
# needs overflow check method maybe?
class Challenge:
    """
    Create challenge object. The pattern is what is necessary to succeed at a challenge. The reward is what happens when you succeed, the penalty is what happens when you fail.
    """
    # reward/penalty are currently strings, but should be changed to something else.
    def __init__(self, name: str, pattern: dict, reward: str, penalty: str) -> None:
        self.name = name
        self.pattern = pattern
        self.reward = reward
        self.penalty = penalty
        self.slots = {key:0 for key in pattern.keys()}

    def add_die(self, die_face:str) -> None:
        number, symbol = die_face.split(' x ')
        number = int(number)
        if symbol in self.pattern.keys():
            self.slots[symbol] += number
        else:
            # should this be an error
            raise ValueError(f"""{die_face} is not 
            contained in the pattern for this challenge.""")
        # what should I do about exceeding the maximum error?
        # maybe that is a separate method
    
    @property
    def complete(self):
        for key in self.pattern.keys():
            if self.pattern[key]> self.slots[key]:
                print(f"Challenge is not yet complete, you still need {self.pattern[key] - self.slots[key]} {key}'s.")
                return false
        print(f'You have completed the Challenge: {self.name}!')
        print(f"You get a {self.reward}.")
        return True

class Die:
    SYMBOLS = {'1 x Investigate','2 x Investigate','3 x Investigate','4 x Investigate','1 x Scroll','2 x Scroll', '1 x Skull', '1 x Tentacles'}
    def __init__(self, faces:tuple)-> None:
        for face in faces:
            if face in self.SYMBOLS:
                continue
            else:
                raise ValueError(f"{face} is not a valid symbol. We can not create this die.")
        if len(faces) != 6: # maybe this should also be relaxed
            raise ValueError(f"{faces} has too many sides to be a die.")
        self.faces = faces # tuple of elements of Symbols
    
    def roll(self) -> str:
        return random.choice(self.faces)

green_die = Die(('1 x Investigate','2 x Investigate','3 x Investigate','1 x Scroll', '1 x Skull', '1 x Tentacles'))


def create_generic():
    """
    This function creates basic instances of the above classes for the purpose of development.
    """
    basic_challenge1 = Challenge(name='basic_attack',pattern={'Investigate':2, 'Skull':1}, reward="+1 damage", penalty="-1 health")
    basic_challenge2 = Challenge(name='basic_heal',pattern={'Investigate':1, 'Scroll':2}, reward="+2 health", penalty="-1 health")
    basic_old_one = GreatOldOne("basic old one", 10, (basic_challenge1, basic_challenge2), "+2 damage")
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
c1, c2 = old_one.challenges
joe.roll_dice()
