"""
This file is for routines related to the google spreadsheet storing the game data.
"""
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Tuple, Optional, Dict, Union
# I guess I should change this to not load everything
from game_pieces import *

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("pp3-command-line-game")


#Great Old One section
def fetch_great_old_ones() -> List[dict]:
    raw = SHEET.worksheet("GreatOldOnes").get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    great_old_ones_dicts = []
    index = 1
    for row in raw:
        great_old_ones_dicts.append({key:val for key, val in zip(keys,row)})
        # storing as string since that is how input will convert it
        great_old_ones_dicts[-1]['index'] = str(index)
        index += 1
    return [g_o_o_dict_to_g_o_o(g_o_o_dict) for g_o_o_dict in great_old_ones_dicts]

def g_o_o_dict_to_g_o_o(g_o_o:dict) -> 'GreatOldOne':
    index = g_o_o['index']
    name = g_o_o['Name']
    elder_signs = int(g_o_o['Elder Signs Needed'])
    doom = int(g_o_o['Doom to Awake'])
    ability = g_o_o['Special Ability']
    return GreatOldOne(index, name, elder_signs, doom, ability)

# Investigator section
def fetch_investigators() -> List[dict]:
    raw = SHEET.worksheet("Investigators").get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    investigator_dicts = []
    index = 1
    for row in raw:
        investigator_dicts.append({key:val for key, val in zip(keys,row)})
        # storing as string since that is how input will convert it
        investigator_dicts[-1]['index'] = str(index)
        index += 1
    return [inv_dict_to_inv(inv_dict) for inv_dict in investigator_dicts]

def inv_dict_to_inv(inv:dict) -> 'Investigator':
    index = inv['index']
    name = inv['Name']
    profession = inv['Profession']
    spirit = int(inv['Sanity'])
    body = int(inv['Stamina'])
    ability = inv['Ability']
    # passing an empty item list until items are implemented with respect to the db
    return Investigator(index, name, profession, spirit, body, ability, [])



# Task Card section
def fetch_task_cards() -> List[dict]: 
    raw = SHEET.worksheet('TaskCards').get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    # gold on task cards not yet implemented
    #keys[-1] = 'Gold'
    task_card_deck = []
    for row in raw:
        task_dict = {key:val for key, val in zip(keys,row)}
        task_card_deck.append(task_dict_to_task_card(task_dict))
    #I actually don't need to drop these columns since the data is thrown away when I create the task cards.
    return [task_card for task_card in task_card_deck if task_card.reward]


def task_dict_to_task_card(task_dict:dict) -> "TaskCard":
    task_data = [task_dict['Task 1'],task_dict['Task 2'],task_dict['Task 3']]
    tasks = create_task_list(task_data)
    reward = create_outcome(task_dict['Rewards'])
    penalty = create_outcome(task_dict['Penalties'])
    return TaskCard(task_dict['Name'],task_dict['Flavor Text'],tasks, reward, penalty)

def create_task_list(task_data:List[str])-> List['Task']:
    tasks = []
    for task_raw in task_data:
        if not task_raw.strip():
            break
        tasks.append(create_task(task_raw))
    return tasks

def clean_raw(raw:str) -> str:
    remove_terms = [' (Total Monster Task)',' (Partial Monster Task)', ' (Total Monter Task)', ' -->', ' Token', ' Signs', ' Sign'] #,' Item'] 
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
    #print(f'{task_raw=}')
    #print(f'{parts=}')
    for part in parts:
        part = part.split()
        try:
            int(part[0])
        except ValueError as e:
            print("Hit ValueError in create task.")
            print(f"{part[0]=}")
            print(f'{part=}')
            print(f"{task_raw=}")
            input()
        pattern[translate_term(part[1])] = int(part[0])
    return Task(pattern)

#maybe not necessary
def clean_outcome_raw(outcome_raw:str) -> str:
    drop_terms = ['Other', 'World', 'Spell', 'Ally','Clues', 'Clue', 'Item']
    cleaned_outcome = ''
    for item in outcome_list.split():
        add = True
        for term in drop_terms:
            if term in item:
                add =False
        if add:
            cleaned_outcome_list.append(clean_raw(item))
    return cleaned_outcome_list

# refactor this eventually
def clean_outcome_list(outcome_list:List[str]) -> List[str]:
    drop_terms = ['Other', 'Monster', 'Monter','Spell', 'Ally', 'Clue', 'Item']
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
        try:
            proper_outcomes[translate_term(outcome.split()[1])]=int(outcome.split()[0])
        except (IndexError, KeyError) as e:
            print("Hit error in create_outcome")
            print(type(e))
            print(e)
            print(outcome_raw)
            print(outcome_list)
            print(outcome)
            input()
    return proper_outcomes