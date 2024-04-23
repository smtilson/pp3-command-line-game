# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Eventually classes should probably be changed to named tuples


class GreatOldOne:
    """
    Creates Great Old One enemy.
    """
    def __init__(self, health:int, challenges:tuple, attack:str): -> None
        self.starting_health = health
        self.health = health
        self.challenges = challenges
        self.attack = attack # this should be replaced by something later
        self.alive = True # refactor to property
    
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


class Challenge:
    """
    Create challenge object. The pattern is what is necessary to succeed at a challenge. The reward is what happens when you succeed, the penalty is what happens when you fail.
    """
    # reward/penalty are currently strings, but should be changed to something else.
    def __init__(self, pattern: tuple, reward: str, penalty: str) -> None:
        self.pattern = pattern
        self.reward = reward
        self.penalty = penalty
        self.slots = []

    def add_die(self, die_face:str) -> None: