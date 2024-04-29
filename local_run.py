# This file is for local testing without interrupting what is hosted and 
# running on Heroku

import game_pieces as gp
import db_utilities as db
import run
from utilities import *

#game = run.start_game()
#run.main_gameplay_loop(game)
game = run.test_game()
run.main_gameplay_loop(game)