# This file is for local testing without interrupting what is hosted and 
# running on Heroku

import game_pieces as gp
import db_utilities as db
import run
from utilities import *



def introduction() -> None:
    basic_idea1 = 'Welcome to "Chtulu Schmtulu," a dice rolling game heavily '\
    "based on Elder Sign from Fantasy Flight Games. In each game, you "\
    "attempt to Banish a Great Old One before they are Summoned or before "\
    "you are Defeated. After selecting a Great Old One to battle against, "\
    "you will select an Investigator to play as. The Great Old Ones are "\
    "Summoned when they gain enough Doom. They are Banished when you collect"\
    " enough Elder Signs."
    tldr = "TL;DR: Go to Adventures, assign dice to complete tasks. Collect "\
    "Elder Signs before you are Defeated or the Great Old One gains enough "\
    "Doom."
    basic_idea2 = "You will collect Elder Signs by completing Adventures. Doom"\
    " is gained when the clock strikes midnight (the clock advances after "\
    "each of your turns) as well as through game effects. If your "\
    "Investigator has 0 Health or 0 Sanity, then you are defeated. If you "\
    "are defeated or the Great Old One is Summoned, then you have lost. If "\
    "you collect enough Elder Signs to Banish the Great Old One, then you "\
    "have won!"
    adventures1 = "Each turn you will go to a Adventure. To complete a Adventure"\
    " you must complete each task at the Adventure. A task is completed by "\
    "assigning matching dice to the task in order to fulfill the "\
    "requirements. Some tasks also have you suffer a penalty by losing "\
    "Health or Sanity. If none of the symbols on your dice match a symbol on"\
    " the task, you may do a Pass."
    adventures2 = "A Pass rerolls all of your dice at the cost of forfeiting "\
    "one of them. You may also use an Item (the Item selection menu also "\
    "contains a description of what each Item does). If you run out of dice,"\
    " you fail the Adventure and suffer associated Penalty. If you complete a"\
    " Adventure, you receive the associated Reward. Penalties can be losing "\
    "Health or Sanity, or the Great Old One gaining additional Doom. Rewards"\
    " can be gaining an Item, Health, or Sanity."
    dice ="As the game revolves around rolling dice, here are the different "\
    "dice that\nare in the game:\nGreen =  1 Investigate, 2 Investigate, "\
    "3 Investigate, \n         1 Lore, 1 Skulls, 1 Tentacles\nYellow = "\
    "1 Investigate, 2 Investigate, 3 Investigate, 4 Investigate,\n     "\
    "    1 Lore, 1 Skulls\nRed =    2 Investigate, 3 Investigate, "\
    "4 Investigate,\n         1 Lore, 1 Skulls, 1 Wild\nSpell =  All "\
    "1 Wild"
    losing_dice = "When you lose a die by passing, you will lose the earliest"\
    "die in your pool\naccording to the ordering:\n       Green < Yellow < "\
    "Red < Spell"
    difficulty = "Difficulty can be adjusted through the setting of two "\
    "different parameters. Increment sets how much the clock advances after "\
    "each of your turns. The standard setting is 6 hours, so Doom "\
    "accumulates every 4 turns. The second is the starting dice pool. "\
    "Standard (which is quite a challenge) is 6 Green dice."
    items = "Each Investigator begins the game with different starting Items."\
    " Items come in 4 varieties: Common, Unique, Clue, and Spell. Common "\
    "Items will usually give you a yellow die, Unique Items will usually "\
    "give you a red die (for that Adventure). Clues allow you to reroll your "\
    "dice without penalty. Spells add a Wild symbol to your dice pool. You "\
    "will also gain Items by completing Adventures."
    future = "In the future, we would like to implement more of the game, "\
    "such as abilities of Investigators as well as Great Old Ones. This is a"\
    " bit of a task though as each ability requires a separate function that"\
    " must be implemented which may take effect at different points in game "\
    "play. There are other notable aspects of game play which we would also "\
    "like to implement in the future, such as focusing, multiplayer mode, "\
    "and Monsters."
    more_help = "If you have further questions, please see the ReadMe for "\
    "this project at, it contains examples of game play. It may also be "\
    'beneficial to view game play or a "how to play" video for Elder Sign on'\
    " YouTube."

    more_details = [basic_idea1, tldr, basic_idea2, adventures1, adventures2,
                    # difficulty, add this once there is a select difficulty 
                    # function in place
                    items, future, more_help]
    dice_text = [dice]
    return more_details, dice_text

#run.introduction()
game = run.test_game()
run.main_gameplay_loop(game)


