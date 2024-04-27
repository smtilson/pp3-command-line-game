## Introduction
"Chtulu Schmtulu" is a yazhee style game based on the board game Elder Sign from Fantasy Flight Games. The game revolves around completing task cards by rolling dice. Completing a card gives you a reward. Failing to complete a card gives you a penalty. The goal is to collect enough Elder Signs, through rewards on cards, to banish the Great Old One before they have been summoned. A Great Old One is summoned when they have accumulated a certain amount of doom. Doom acculumates through card effects and by the clock reaching 12 midnight.

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
7. Scroll down to "Buildpacks". Click "Add buildpack", select "python", and click "Add buildpack".
8. Click "Add buildpack", select "nodejs", and click "Add buildpack".

Note: Make sure that the python buildpack is before the nodejs buildpack. If not, you can reorder them by dragging python to the top.

9. Go to the "Deploy" tab. Scroll down to "Deployment method" and select "GitHub". Search for your repository that you copied/cloned in step 1 above.  Click "Connect" once you have found it.

10. Scroll down to "Manual deploy" and click "Deploy Branch". Once the build is complete, click "View" to be taken to your deployed app.

[return to Table of Contents](#toc)