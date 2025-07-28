# Dumb Badge(s) Remover
Dumb Badge(s) Remover (DBR) is a Python package that removes [Roblox](https://www.roblox.com) badges, specifically any dumb ones that you don't want anymore. It can declutter your badge inventory of Badge chains and other various filler badges. You can also scan your inventory for spam badges without removing any badges.

This program is useful you have been invalidated by the scanner on [MetaGamerScore](https://metagamerscore.com/). You can download their list of invalid games through a function.

## Requirements
DBR runs on [Python 3.11+](https://www.python.org/downloads/). To install the required pip packages, you can run `pip install -r requirements.txt` in the project's directory to install the packages.

## Installation and Running
Install the program with pip by running `pip install git+https://github.com/exurd/dbr`. Other Python package managers are supported, like `pipx install` and `uv pip install`.

To use the program, run `python -m dbr [COMMAND]` or `dbr [COMMAND]`. Adding `-h` will give you the full arguments you can use.
```
usage: Dumb Badge(s) Remover [-h] [--version] [--file FILE] [--badge BADGE_ID]
                             [--place PLACE_ID] [--user USER_ID]
                             [--group GROUP_ID] [--mgs-id MGS_ID]
                             [--env-file ENV_FILE] [--rbx-token RBX_TOKEN]
                             [--download-mgs-invalid-list]
                             [--download-badge-spam-lists]
                             [--use-bor-badge-database]
                             [--check-inventory USER_ID]
                             [--cache-directory CACHE_DIRECTORY]
                             [--delete-threads NUM_THREADS]
                             [--user-agent USER_AGENT]

Removes Roblox badges very quickly

There are 16 arguments available.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --file FILE           Filename path with 'https://roblox.com/[TYPE]/[ID]'
                        urls you want gone from your account.
  --badge, -b BADGE_ID  Specify a badge ID you want gone from your account.
  --place, -p PLACE_ID  Specify a place ID you want gone from your account.
  --user, -u USER_ID    Specify a user ID you want gone from your account.
  --group, -g, --community GROUP_ID
                        Specify a group / community ID you want gone from your
                        account.
  --mgs-id MGS_ID       Specify a MetaGamerScore game ID you want gone from
                        your account.
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
  --download-badge-spam-lists
                        Download text files from exurd/badge-spam-lists; a
                        bunch of text files containing place IDs from various
                        Roblox badge chains.
  --use-bor-badge-database
                        Tell DBR to instead use the Badgers of Robloxia's
                        Valuable Badge Database to view badges in a universe.
                        Useful for disabled badges, which are hidden when
                        checking universes via the Roblox API. NOTE: Requests
                        for this API can take a long time to complete. It is
                        recommended to instead use the inventory scanner to
                        find hidden badges that you have collected.
  --check-inventory, -c USER_ID
                        Checks a user's inventory for spam badges. DOES NOT
                        DELETE BADGES. Requires a list of place IDs to check
                        (use download arguments above).
  --cache-directory, -cd CACHE_DIRECTORY
                        The directory where cache data is kept.
  --delete-threads NUM_THREADS
                        Sets how many concurrent threads used when deleting
                        multiple badges.
  --user-agent, -ua USER_AGENT
                        Sets the user agent for requests made by the program.
```

## Configuration
To be able to delete badges, you will need to authenticate yourself with a ROBLOSECURITY token. To export your token, [read the ro.py's page](https://ro.py.jmk.gg/v2.0.0/tutorials/roblosecurity/) on the topic. BE VERY CAREFUL WHEN USING THE TOKEN!

**DO NOT SHARE IT WITH ANYONE!**

**IF ANYONE (EVEN YOUR FRIENDS) ASK YOU TO SEND YOUR TOKEN TO THEM, DO NOT GIVE THEM YOUR TOKEN! THEY CAN DO ANYTHING TO YOUR ACCOUNT IF THEY HAVE YOUR TOKEN. THIS INCLUDES STEALING YOUR ROBUX, UPLOADING BANNABLE CONTENT AND DELETING YOUR ACCOUNT FOREVER!**

**DO NOT SHARE IT WITH ANYONE!!**

Once you have your token, add the argument `--rbx-token [TOKEN]` to your command.

For better safety, you can use .env files to avoid leaks. The `.example_env` in this repository can be used as a starting point. Copy the file and rename it it `.env`. Paste the ROBLOSECURITY token into this line: `ROBLOXTOKEN="[TOKEN HERE]"`. Use the argument `--env-file [.env file]`. 

# Downloading lists
There are two commands for downloading lists for this program; `--download-mgs-invalid-list` and `--download-badge-spam-lists`. The first command downloads a list of games that are considered spam by MetaGamerScore. The other command downloads multiple text files from [exurd/badge-spam-lists](https://github.com/exurd/badge-spam-lists).

To delete badges from games in a text file, use the `--file` command with the path to the file. Make sure it ends with `.txt` and not `.json`!

# Scanning inventories
With the `-- check-inventory` option, you can scan any public inventory for spam badges. It will use any lists downloaded via the above commands. It can then be used to gauge how many spam badges a user has.

Two text files will be created; one for places and one for badges. Each place found in the places list will have the name in the URL. For the badge list, only the 

> [!CAUTION]
> Check the results of the scan before using them to remove badges, especially if you have downloaded the MGS spam list; false positives have been known to show up there.

*This project has been licensed with the MIT License.*