Configuration Instructions
Step 1: Fill in the config.json file
Example:

json
{
  "TELEGRAM_BOT_TOKEN": "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef",
  "TELEGRAM_CHANNEL": "@your_channel",
  "OPENAI_API_KEY": "sk-abcd1234efgh5678ijkl9012mnop3456qrstuvwx",
  "PROMPT": "You summarize the text for the video description for a post in the Telegram channel. You need the main points to interest the listener. The text should be no shorter than 50 words.",
  "HASHTAGS": ["#hashtag_1", "#hashtag_2"]
}


Explanation of Config Parameters:

HASHTAGS
If hashtags are present in the video title, the script will use them automatically.
Alternatively, you can add your own hashtags manually in the config.json.

TELEGRAM_BOT_TOKEN
Create a Telegram bot using BotFather and follow the instructions to obtain the bot token.
Use the /newbot command in BotFather.
Example response:

Done! Congratulations on your new bot. You will find it at t.me/your_bot_name. Use this token to access the HTTP API:
123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef

Keep the token secure, as it can be used by anyone to control your bot.
For more details, refer to the Telegram Bot API documentation.

TELEGRAM_CHANNEL
Specify the Telegram channel in the format "@your_channel".
Add your bot as an administrator to the channel with permission to post messages.
To verify that the bot is correctly linked to the channel:
Post something in the channel using your main Telegram account.

Run the following command in a terminal (replace the token with your bot's token):

bash:
curl -X GET "https://api.telegram.org/bot123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef/getMe"
or
curl -X GET "https://api.telegram.org/bot123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef/getUpdates"

This will display information about the bot and the last channel it interacted with.

OPENAI_API_KEY
Purchase an OpenAI subscription and obtain an API key.
Follow the instructions here: OpenAI Billing Overview.


PROMPT
You can modify the instruction for ChatGPT (PROMPT) to adjust how it processes the transcription text.


--------------------------------
Step 2: Run the teleteller.exe Script
The script performs the following tasks:

Downloads audio from the video into the ./downloads folder (located alongside teleteller.exe).
Extracts a transcript from the audio.
Saves the full transcript as a .txt file in the ./transcriptions folder.
Sends the transcript to ChatGPT via the OpenAI API with the specified prompt for summarization.
Creates a post and sends it to the specified Telegram channel using your bot.

--------------------------------
Prerequisites:
Install Python 3.9 or higher: Python Downloads.
Ensure teleteller.exe and the project code are in the same directory.

Optional: Rebuilding the .exe File
If you need to rebuild the project into an updated .exe file:

Install PyInstaller.
Run the following command:
bash:
pyinstaller --onefile teleteller.py
