# Dumb Badge(s) Remover
Dumb Badge(s) Remover (DBR) is a Python package that removes [Roblox](https://www.roblox.com) badges, specifically any dumb ones that you don't want anymore. It can declutter your badge inventory of Badge chains and other various filler badges.

This is useful you have been invalidated by the scanner on [MetaGamerScore](https://metagamerscore.com/). You can download their list of invalid games through a function.

## Requirements
DBR runs on [Python 3.11+](https://www.python.org/downloads/). To install the required pip packages, you can run `pip install -r requirements.txt` in the project's directory to install the packages.

## Installation and Running
Run `pip install .` to install DBR. To use the program, run `python -m dbr [COMMAND]`. Adding `-h` will give you the full arguments you can use.
```
usage: Dumb Badge(s) Remover [-h] [--version] [--file FILE] [--badge BADGE_ID]
                             [--place PLACE_ID] [--user USER_ID]
                             [--group GROUP_ID] [--mgs-id MGS_ID]
                             [--env-file ENV_FILE] [--rbx-token RBX_TOKEN]
                             [--download-mgs-invalid-list]
                             [--cache-directory CACHE_DIRECTORY]
                             [--user-agent USER_AGENT]

Removes Roblox badges very quickly

There are 12 arguments available.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --file FILE           Filename path with 'https://roblox.com/[TYPE]/[ID]'
                        urls.
  --badge, -b BADGE_ID  Specify a badge ID.
  --place, -p PLACE_ID  Specify a place ID.
  --user, -u USER_ID    Specify a user ID.
  --group, -g, --community GROUP_ID
                        Specify a group / community ID.
  --mgs-id MGS_ID       Specify a MGS ID.
  --env-file, -e ENV_FILE
                        An .env file allows you to specify settings (the below
                        options) for Dumb Badge(s) Remover to follow without
                        cluttering the terminal or risking important tokens.
                        More information on .env files can be found in the
                        README.
  --rbx-token, -t RBX_TOKEN
                        .ROBLOSECURITY token. By using this option, you agree
                        that this is your unique token and not anyone else's.
                        DO NOT SHARE YOUR ROBLOX TOKEN WITH ANYONE! More info
                        can be found here:
                        https://ro.py.jmk.gg/dev/tutorials/roblosecurity/
  --download-mgs-invalid-list
                        Download MetaGamerScore's list of Roblox games that
                        were detected as problematic. May contain games that
                        are not considered spam, so use with caution.
  --cache-directory, -cd CACHE_DIRECTORY
                        The directory where cache data is kept.
  --user-agent, -ua USER_AGENT
                        Sets the user agent for requests made by the program.
```

## Configuration
To be able to delete badges, you will need to authenticate yourself with a ROBLOSECURITY token. To export your token, [read the ro.py's page](https://ro.py.jmk.gg/v2.0.0/tutorials/roblosecurity/) on the topic. BE VERY CAREFUL WHEN USING THE TOKEN!

**DO NOT SHARE IT WITH ANYONE!**

**IF ANYONE (EVEN YOUR FRIENDS) ASK YOU TO SEND YOUR TOKEN TO THEM, DO NOT GIVE THEM YOUR TOKEN! THEY CAN DO ANYTHING TO YOUR ACCOUNT IF THEY HAVE YOUR TOKEN. THIS INCLUDES STEALING YOUR ROBUX, UPLOADING BANNABLE CONTENT AND DELETING YOUR ACCOUNT FOREVER!**

**DO NOT SHARE IT WITH ANYONE!!**

Once you have your token, add the argument `--rbx-token [TOKEN]` to your command.

For better safety, you can use .env files to avoid leaks. Use `.example_env` as a starting point. Copy the file and rename it it `.env`. Paste the ROBLOSECURITY token into this line: `ROBLOXTOKEN="[TOKEN HERE]"`. Use the argument `--env-file [.env file]`. 

*This project has been licensed with the MIT License.*