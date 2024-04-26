"""
This file is for routines related to the google spreadsheet storing the game data.
"""
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Tuple, Optional, Dict, Union
from game_pieces import TaskCard, Task

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("pp3-command-line-game")

def get_task_card_data()-> List[dict]: 
    raw = SHEET.worksheet('TaskCards').get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    keys[-1] = 'Gold'
    task_card_dicts = []
    for row in raw:
        task_card_dicts.append({key:val for key, val in zip(keys,row)})
    return [drop_cols(card_dict) for card_dict in task_card_dicts]

def drop_cols(task_dict:dict ) -> dict:
    del task_dict['Effect?']
    del task_dict['Locked Dice?']
    del task_dict['Monster Task?']
    return task_dict

def task_dict_to_task_card(task_dict:dict) -> "TaskCard":
    task_data = [task_dict['Task 1'],task_dict['Task 2'],task_dict['Task 3']]
    tasks = create_task_list(task_data)
    reward = create_outcome(task_dict['Reward'])
    penalty = reward = create_outcome(task_dict['Penalty'])
    return 

def create_task_list(task_data:List[str])-> List['Task']:
    tasks = []
    for task_raw in task_data:
        if not task_raw:
            break
        task.append(create_task(task_raw))
    return tasks

def clean_raw(task_raw:str) -> str:
    remove_terms = [' (Total Monster Task)', ' -->', ' Token', ' Item', ' Sign'] 
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
        pattern[translate_term(part[1])] = int(part[0])
    return Task(pattern)

def drop_outcome_terms(outcome_list:List[str]) -> List[str]:
    drop_terms = ['Other World', 'Monster', 'Spell', 'Ally']
    cleaned_outcome_list = []
    for item in outcome_list:
        add = True
        for term in drop_terms:
            if term in item:
                add =False
                break
        if add:
            cleaned_outcome_list.append(item)
    return cleaned_outcome_list

def create_outcome(outcome_raw:str) -> List[str]:
    outcome_list = outcome_raw.split(', ')
    outcome_list = cleaned_outcome_list(outcome_list)
    pass
