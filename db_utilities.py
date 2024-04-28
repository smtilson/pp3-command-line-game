"""
This file is for routines related to the google spreadsheet storing the game 
data.
"""
import gspread
from google.oauth2.service_account import Credentials
import datetime
from typing import List, Tuple, Dict, Union
# I guess I should change this to not load everything
from game_pieces import *
from utilities import get_selection

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("pp3-command-line-game")


# Great Old One section
def fetch_great_old_ones() -> List[dict]:
    raw = SHEET.worksheet("GreatOldOnes").get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    great_old_ones_dicts = []
    index = 1
    for row in raw:
        great_old_ones_dicts.append({key: val for key, val in zip(keys, row)})
        # storing as string since that is how input will convert it
        great_old_ones_dicts[-1]['index'] = index
        index += 1
    return [goo_dict_to_goo(goo_dict) for goo_dict in great_old_ones_dicts]

def goo_dict_to_goo(goo:dict) -> 'GreatOldOne':
    index = goo['index']
    name = goo['Name']
    elder_signs = int(goo['Elder Signs Needed'])
    doom = int(goo['Doom to Awake'])
    ability = goo['Special Ability']
    return GreatOldOne(index, name, elder_signs, doom, ability)

# Investigator section
def fetch_investigators() -> List[dict]:
    raw = SHEET.worksheet("Investigators").get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    inv_dicts = []
    for row in raw:
        inv_dicts.append({key:val for key, val in zip(keys,row)})
    exclusions = ['Amanda Sharpe','"Ashcan" Pete']
    inv_dicts = [inv_dict for inv_dict in inv_dicts if inv_dict['Name'] not in exclusions]
    for index, inv_dict in enumerate(inv_dicts):    
        # storing as string since that is how input will convert it
        inv_dict['index'] = index+1
    return [inv_dict_to_inv(inv_dict) for inv_dict in inv_dicts]

def inv_dict_to_inv(inv:dict) -> 'Investigator':
    index = inv['index']
    name = inv['Name']
    profession = inv['Profession']
    sanity = int(inv['Sanity'])
    health = int(inv['Stamina'])
    ability = inv['Ability']
    # items are added at the start of the game.
    items = inv['Starting Items'].replace(' item','').split(', ')
    return Investigator(index, name, profession, sanity, health, ability,items)

# Item section
def fetch_items() -> List[dict]:
    raw = SHEET.worksheet("Items").get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    item_dicts = []
    for row in raw:
        item_dicts.append({key:val for key, val in zip(keys,row)})
    exclusions = ['Flute of the Outer Gods','Shotgun','Blue Watcher of the Pyramid','Necronomicon']
    return [item_dict_to_item(item_dict) for item_dict in item_dicts if item_dict['Name'] not in exclusions]

def item_dict_to_item(item:dict) -> 'Item':
    name = item['Name']
    effect = item['Text/Effect']
    item_type = item['Rarity']
    return Item(name, effect, item_type)


# Task Card section
def fetch_locations() -> List[dict]: 
    raw = SHEET.worksheet('Locations').get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    # gold on task cards not yet implemented
    #keys[-1] = 'Gold'
    location_deck = []
    for row in raw:
        task_dict = {key:val for key, val in zip(keys,row)}
        location_deck.append(task_dict_to_location(task_dict))
    #I actually don't need to drop these columns since the data is thrown away when I create the task cards.
    return [location for location in location_deck if location.reward]


def task_dict_to_location(task_dict:dict) -> "Location":
    #print(task_dict)
    #input()
    task_data = [task_dict['Task 1'],task_dict['Task 2'],task_dict['Task 3']]
    tasks = create_task_list(task_data)
    reward = create_outcome(task_dict['Rewards'])
    penalty = create_outcome(task_dict['Penalties'])
    card = Location(task_dict['Name'],task_dict['Flavor Text'],tasks, reward, penalty)
    #print(card)
    #input()
    return card

def create_task_list(task_data:List[str])-> List['Task']:
    tasks = []
    for task_raw in task_data:
        if not task_raw.strip():
            break
        tasks.append(create_task(task_raw))
    return tasks

def clean_raw(raw:str) -> str:
    raw = raw.replace(' -->', ',')
    remove_terms = [' (Total Monster Task)',' (Partial Monster Task)', ' (Total Monter Task)', ' Token', ' Signs', ' Sign'] #,' Item'] 
    for term in remove_terms:
        raw = raw.replace(term, '')
    return raw

#does this need to be a separate function?
def translate_term(term: str) -> str:
    term = term.title()
    return Task.TRANSLATION[term] 

def create_task(task_raw:str) -> 'Task':
    task_raw = clean_raw(task_raw)
    parts = task_raw.split(', ')
    pattern = {}
    for part in parts:
        part = part.split()
        int(part[0])
        pattern[translate_term(part[1])] = int(part[0])
    return Task(pattern)

# refactor this eventually
def clean_outcome_list(outcome_list:List[str]) -> List[str]:
    drop_terms = ['Other', 'Monster', 'Monter', 'Ally']
    cleaned_outcome_list = []
    for item in outcome_list:
        add = True
        for term in drop_terms:
            if term in item:
                add =False
                break
        if add:
            cleaned_outcome_list.append(clean_raw(item))
    return cleaned_outcome_list

#Outcomes should be refactored to work with a dictionary.
def create_outcome(outcome_raw:str) -> dict:
    outcome_list = outcome_raw.split(', ')
    outcome_list = clean_outcome_list(outcome_list)
    proper_outcomes = {}
    for outcome in outcome_list:
        proper_outcomes[translate_term(outcome.split()[1])]=int(outcome.split()[0])
    return proper_outcomes


class GameSelection:
    """
    This class queries the database and initializes the potential game state.
    """
    def __init__(self) -> None:
        print('Loading game data...')
        self.location_deck = fetch_locations()
        self.item_deck = fetch_items()
        self.great_old_ones = fetch_great_old_ones()
        self.investigators = fetch_investigators()
        print('Game data loaded.')
    
    def select_great_old_one(self):
        for great_old_one in self.great_old_ones:
            great_old_one.selection()
        index = get_selection(len(self.great_old_ones),'a Great Old One to '\
                              'battle')
        return self.great_old_ones[index]
    
    def select_investigator(self):
        for investigator in self.investigators:
            investigator.selection()
        index = get_selection(len(self.investigators),'an investigator to '\
                              'play as')
        return self.investigators[index]
    

def record(game):
    result = ''
    investigator = game.investigator.name
    great_old_one = game.great_old_one.name
    if not game.end_condition:
        pass
    elif game.end_condition == "Banished":
        result = f"{investigator} defeated {great_old_one}."
    elif game.end_condition == "Died":
        result = f"{investigator} perished and {great_old_one} devoured the "\
        "world."
    elif game.end_condition == "Summoned":
        result = f"{investigator} was unable to prevent {great_old_one} from "\
        "being summoned and devouring the world."
    target_sheet = SHEET.worksheet('Records')
    record = [game.player, game.game_start_time, str(datetime.datetime.now()), 
              investigator, great_old_one, result]
    target_sheet.append_row(record)