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

def fetch_task_card_data()-> List[dict]: 
    raw = SHEET.worksheet('TaskCards').get_all_values()
    keys = raw.pop(0)
    keys[0] = 'Name'
    # gold on task cards not yet implemented
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
    reward = create_outcome(task_dict['Rewards'])
    penalty = create_outcome(task_dict['Penalties'])
    return TaskCard(task_dict['Name'],task_dict['Flavor Text'],tasks, reward, penalty)

def create_task_list(task_data:List[str])-> List['Task']:
    tasks = []
    #print(task_data)
    for task_raw in task_data:
        #print(task_raw)
        #print(len(task_raw))
        #print(len(task_raw.strip()))
        #input()
        if not task_raw.strip():
            break
        tasks.append(create_task(task_raw))
    return tasks

def clean_raw(raw:str) -> str:
    remove_terms = [' (Total Monster Task)', ' (Total Monter Task)', ' -->', ' Token', ' Signs', ' Sign'] #,' Item'] 
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

def clean_outcome_list(outcome_list:List[str]) -> List[str]:
    drop_terms = ['Other', 'Spell', 'Ally', 'Clue', 'Item']
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
def create_outcome(outcome_raw:str) -> List[str]:
    outcome_list = outcome_raw.split(' ')
    outcome_list = clean_outcome_list(outcome_list)
    proper_outcomes = {}
    for outcome in outcome_list:
        try:
            proper_outcomes[translate_term(outcome.split()[1])]=outcome.split()[0]
        except IndexError as e:
            print(e)
            print(outcome_raw)
            print(outcome_list)
            print(outcome)
            input()
    return proper_outcomes