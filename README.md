# Dumb Badge(s) Remover
Dumb Badge(s) Remover (DBR) is a Python package that removes [Roblox](https://www.roblox.com) badges, specifically any dumb ones that you don't want anymore. It can declutter your badge inventory of Badge chains and other various filler badges.

This is useful you have been invalidated by the scanner on [MetaGamerScore](https://metagamerscore.com/). You can download their list of invalid games through a function.

## Requirements
DBR requires [Python 3.11+](https://www.python.org/downloads/) and the required pip packages. You can run `pip install -r requirements.txt` in the project's directory to install the packages.

## Installation and Running
Run `pip install .` to install DBR. To use the program, run `python -m dbr [COMMAND]`. Adding `-h` will give you the full arguments you can use.

## Configuration
To be able to delete badges, you will need to authenticate yourself with a ROBLOSECURITY token. To export your token, [read the ro.py's page](https://ro.py.jmk.gg/v2.0.0/tutorials/roblosecurity/) on the topic. BE VERY CAREFUL WHEN USING THE TOKEN!

**DO NOT SHARE IT WITH ANYONE!**

**IF ANYONE (EVEN YOUR FRIENDS) ASK YOU TO SEND YOUR TOKEN TO THEM, DO NOT GIVE THEM YOUR TOKEN! THEY CAN DO ANYTHING TO YOUR ACCOUNT IF THEY HAVE YOUR TOKEN. THIS INCLUDES STEALING YOUR ROBUX, UPLOADING BANNABLE CONTENT AND DELETING YOUR ACCOUNT FOREVER!**

**DO NOT SHARE IT WITH ANYONE!!**

Once you have your token, add the argument `--rbx-token [TOKEN]` to your command.

For better safety, you can use .env files to avoid leaks. Use `.example_env` as a starting point. Copy the file and rename it it `.env`. Paste the ROBLOSECURITY token into this line: `ROBLOXTOKEN="[TOKEN HERE]"`. Use the argument `--env-file [.env file]`. 

*This project has been licensed with the MIT License.*