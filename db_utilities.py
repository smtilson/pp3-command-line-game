"""
This file is for routines related to the google spreadsheet storing the game data.
"""
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Tuple, Optional, Dict, Union

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