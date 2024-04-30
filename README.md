

## Introduction
"Chtulu Schmtulu" is a dice rolling game based on the board game Elder Sign from Fantasy Flight Games. The game revolves around rolling dice to match symbols on adventure cards. Completing a card gives you a reward. Failing to complete a card gives you a penalty. The goal is to collect enough Elder Signs, through rewards on cards, to banish the Great Old One before they have been summoned. After every 3 turns, the Great Old one accumulates Doom (Doom can also increase as a result of failing an adventure card). When they have enough Doom, they will be summoned, ending the game in a loss for the player.

This game is heavily based on Elder Sign. Almost all of the game data is taken from Elder Sign and directly imported. However, the game is not a full implementation of Elder Sign. This would be a goal for the future.

### Instructions
Each game begins with a player entering their name, choosing a Great Old One to battle against, and choosing an Investigator to play as. After that the game begins. Each turn sees a player attempting to complete an Adventure. After the turn ends, in a success or failure, the player will be rewarded or penalized, their dice will be reset, and the clock will advance. If it is midnight, the Great Old One will accrue Doom. Then the game checks to see if any loss conditions or the win condition are satisfied. IF not, the game continues with the player going on another adventure.

#### Winning and Losing
The only way to win is to collect the required amount of Elder Signs in order to banish the chosen Great Old One. This can only be done by completing adventures that have Elder Signs as Rewards. A player will lose if their Health or Sanity is 0 at the end of a turn. A player will also lose if the Great Old One gains enough Doom to be summoned. Doom is gained every 3 turns (at the turns end), when the clock strikes midnight.

A player should decide in advance which Adventures they can afford to fail and which they can not. It is not wise to use all of your items to complete an Adventure unless it will result in winning the game.

Note: The win and loss conditions are only checked at the end of the turn. If a player achieves both, then the win condition takes precedence.

#### Turn Structure
A turn begins with a player going on an Adventure (drawing an Adventure "card") and rolling their dice. Each adventure card has a name, flavor text, tasks, rewards, and penalties. An adventure is completed by completing each task of the Adventure (in any order). If an Adventure is completed, then the player receives the listed award. If the player runs out of dice before completing the adventure then they fail and suffer the penalty. In either case, the turn ends, the game resets for the next round, and the next turn begins.

##### Completing a task
A task on an adventure consists of keywords (which represent symbols) and associated numbers. These keywords occur as faces on the dice. The player has, by default, 6 Green dice. A Green die has the following 6 faces:
1 Investigate, 2 Investigate, 3 Investigate, 1 Lore, 1 Skulls, 1 Tentacles

A player will assign rolled dice from their dice pool to the task in order to fulfill the requirements. For example, suppose the player rolled:
Roll: 1 --> 2 Investigate;   2 --> 1 Skulls;      3 --> 1 Lore
      4 --> 1 Lore;          5 --> 1 Tentacles;   6 --> 1 Investigate
And has the task:
Remaining: 3 Investigate
They would then enter 1 to assign their first die to the task. Their dice pool would then look like:
Roll: 1 --> 1 Skulls;      2 --> 1 Lore           3 --> 1 Lore
      4 --> 1 Tentacles;   5 --> 1 Investigate
Remaining: 1 Investigate
because they assigned there first die to the task. The requirement decreased by 2 since they had 2 Investigate "symbols" on that die face. The die was removed from their pool, and so all die shifted down one. They might then enter 5 to assign their fifth die to the task. This would complete this task and they would have 4 remaining dice to attempt the rest of the tasks for the current Adventure.

Some tasks require a player to lose health or sanity. These effects take place once the task is chosen. The game only checks if the player is alive at the end of the turn, so a player can use an item to recover even if their health or sanity reaches 0 during the turn.

Note: if a player rolls a wild face, then they choose which part of the task to assign it to.

##### Passing
If none of their dice matched the requirements, the player can enter pass. This rerolls all of their dice at the cost of forfeiting one of them. Thus their dice pool decreases. If a player has only one remaining die, and it does not match then they must pass. They will then fail the Adventure as they have no more dice. For example, a player may be in the following situation:
Roll: 1 --> 2 Investigate;   2 --> 1 Skulls;   3 --> 1 Tentacles
      4 --> 1 Investigate
Remaining: 1 Lore
They have no matching symbols and decide to pass. They might then see:
Roll: 1 --> 1 Lore;   2 --> 3 Investigate;   3 --> 1 Investigate
      
Remaining: 1 Lore
Now they can assign their first die and complete the task.

A player can also pass before choosing a task to attempt. The effect is the same, and this may be necessary if they have no matching dice.

##### Items
A player may use an item before choosing a task or assigning a die. There are various items with various effects. Entering item will bring up the item menu. It lists the name and effect of each item. The different possible effects are:

Add a yellow die, Add a red die, Gain 1 Health, Gain 1 Sanity, 
Add a yellow and a red die, Gain a wild die, Reroll all dice, 
Restore Health and Sanity

A yellow die has the following 6 faces:
1 Investigate, 2 Investigate, 3 Investigate, 4 Investigate, 1 Lore, 1 Skulls

A red die has the following 6 faces:
1 Wild, 2 Investigate, 3 Investigate, 4 Investigate, 1 Lore, 1 Skulls

A wild die has all 6 faces 1 Wild.

Each Investigator begins with different collection of starting items that are drawn from the item deck at the start of the game. After an item is used, it is sent to the item_discard. Players gain items by completing adventures. Clues and Spells are considered items but are not in the item_deck. They are unlimited in supply and are not sent to the item_discard.

##### Rewards and Penalties
When an Adventure has all of its tasks completed, the Adventure is complete and the player receives an Award. This can be various items (drawn from the item deck), more Health or Sanity, or an Elder Sign (maybe more than one). These are added to the players inventory. When a player fails an Adventure, by running out of dice, they will suffer the penalty. This can be losing a Clue, the Great Old One gaining more doom, or losing Health or Sanity.
These outcomes are automatically applied and then the turn ends. 

##### End of a Game
Once a game has ended, a record is made of the result. This includes the name the player entered, the start time of the game, the end time of the game, and the result of the game, such as "Vincent Lee perished and Hastur devoured the world."

<a href="https://smtilson-pp3-command-line-game-df86354a3a66.herokuapp.com/">game</a>

### Instructions
The core of the game is completing task cards by completing each task on the given card. An individual task is completed by meeting all of the requirements. Most of these are symbols which are on the dice that you roll. You meet these requirements by assigning dice to the task whose symbol matches it. If no symbols match, we may pass. This results in us losing a die from our pool and rerolling our remaining dice. If we run out of dice before completing all of the tasks on a card we suffer the listed penalty.

Example:

As the game begins, 3 task cards will be dealt. Choose one to attempt by entering the corresponding number. Once a card is selected you will roll your dice pool. Then based on this roll, pick a task on the card to attempt by entering the appropriate number.

## Deployment

### Setting up APIs
1. Go to <a href="https://console.cloud.google.com/">Google Cloud Platform</a>.
2.  Make sure you are logged into the Google account that you want to associate with this project (as opposed to a work account).
3. Open side navigation bar by clicking on the "burger" icon in the upper left.
4. Click on "select a project" and choose "New Project".
5. Enter a project name and click "Create", and select this new project to go to the project page.
6. Select "APIs & Services" from the menu on the left, and then select Library. We will be enabling the Google Drive API and the Google Sheets API.

#### Google Drive API
If necessary, navigate back to the Dashboard for the current project, click on "APIs & Services" then Library in the menu on the left.

1. Search for the Google Drive API in the search bar. Select it, and then enable it.
2. Click "Create Credentials" in the upper right. Once at the form, select Google Drive API in the "Which API are you using?" dropdown menu. Select Application Data, then click "Next".
3. Choose a name for the Service Account. Specify a Service Account ID if one is not generated from the name. Provide a description for the service, such as "Allow for communication between the app and Google Drive." Then click "Create and Continue".
4. Select Role of Editor and click "Continue".
5. On the "Grant users access to this service account" section, leave it blank and click "Done".
6. Once back at the starting Google Drive API page, scroll down to service accounts and click on the account you have just created.
7. Click on "Keys" in the menu at the top. Click on the "Add Key" dropdown menu and select "Create new Key". In the pop-up menu, select JSON and click "Create".
8. Find the downloaded key in your on your machine (usually in your Downloads folder), its name will begin with the name of the service account it is associated with. 
9. Add it to your local repository, change its name (to creds for example), and then add it to your .gitignore file.

#### Connect to Google Sheets account
1. Go to the credentials file in your local repository. Find the client email and copy it without the quotes.
2. Go to the Google Sheets account and open the Sheet you want to grant access to and click the share button.
3. Paste in the copied email address, make sure editor is selected, untick notify people, and click share.

#### Google Sheets API
If necessary, navigate back to the Dashboard for the current project, click on "APIs & Services" then Library in the menu on the left.
1. Search for the Google Sheets API and select it.
2. Click "Enable".
Note: This API does not require credentials.

### Deploying to Heroku

1. Copy/Clone the <a href="https://github.com/smtilson/pp3-command-line-game" target="_blank">repository</a> on github.
2. Log in to your Heroku account.
3. From the Heroku Dashboard, click the dropdown menu "New" and select "Create new app".
4. Choose a unique name for your app, shoose the appropriate region, and then click "Create app".
5. Go to the "Settings" tab. Scroll to "Config Vars" section anc click "Reveal Config Vars".
6. In field for key, enter "CREDS". In the field for value, paste the contents of your creds.json file which you created in the Google Drive API section above.
7. Add a second Config Var with key "PORT" and value "8000".
8. Scroll down to "Buildpacks". Click "Add buildpack", select "python", and click "Add buildpack".
9. Click "Add buildpack", select "nodejs", and click "Add buildpack".

Note: Make sure that the python buildpack is before the nodejs buildpack. If not, you can reorder them by dragging python to the top.

10. Go to the "Deploy" tab. Scroll down to "Deployment method" and select "GitHub". Search for your repository that you copied/cloned in step 1 above.  Click "Connect" once you have found it.
11. Scroll down to "Manual deploy" and click "Deploy Branch". Once the build is complete, click "View" to be taken to your deployed app.

[return to Table of Contents](#toc)