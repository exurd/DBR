# Dumb Badge(s) Remover
Dumb Badge(s) Remover (DBR) is a Python module that removes [Roblox](https://www.roblox.com) badges, specifically any dumb ones that you don't want anymore.

This is useful if you have been invalidated by the scanner on [MetaGamerScore](https://metagamerscore.com/). You can download the list of invalid games through a function.

The module can also be used to declutter your badge inventory of Badge chains and other various filler badges.

## Requirements
The module(s) require [Python 3.11+](https://www.python.org/downloads/) and the pip packages in `requirements.txt`.
You can run `pip install -r requirements.txt` in the project's directory to install the packages.

## Configuration
To be able to delete badges, you will need to authenticate yourself with a ROBLOSECURITY token. To export your token, [read the ro.py's page](https://ro.py.jmk.gg/v2.0.0/tutorials/roblosecurity/) on the topic. BE VERY CAREFUL WHEN USING THE TOKEN!

**DO NOT SHARE IT WITH ANYONE!**

**IF ANYONE (EVEN YOUR FRIENDS) ASK YOU TO SEND YOUR TOKEN TO THEM SO THEY CAN "DELETE THE BADGES", THEY CAN INSTEAD DO MALICIOUS THINGS TO YOUR ACCOUNT. THIS INCLUDES STEALING YOUR ROBUX, UPLOADING BANNABLE CONTENT AND DELETING YOUR ACCOUNT FOREVER!**

**DO NOT SHARE IT WITH ANYONE!!**

You will also need your Roblox User ID to check for obtained badges. You can find it by going to your profile's URL. It should be a number between `https://www.roblox.com/users/` and `/profile`.

You can use `.example_env` as a starting point. Copy the file and rename it it `.env`.

- Paste the ROBLOSECURITY token into this line: `ROBLOXTOKEN="[TOKEN HERE]"`.
- Insert the User ID with no quotes to: `USERID=[USER ID HERE]`.

For advanced users, you can also change the `USERAGENT=` line to fit more closely to your user agent.

## Example Script

```python
# This is an example script on how to use the module.
# First, make sure the script is in the root. Then, import the module from the modules folder:
from modules import remover

# You can delete a specific badge by using the delete_badge function:
remover.delete_badge(0)

# Deleting all the badges from one game can be done with the delete_from_game function:
remover.delete_from_game(0)

# If you have a whole group that only creates spam games (badge chains), you can use the delete_from_group function:
remover.delete_from_group(0)

# For players, the delete_from_player function can be used instead:
remover.delete_from_player(0)

# You can download the all of the invalidated games that MGS detected from scanning users (https://metagamerscore.com/api/roblox/invalid_games) with this function:
remover.download_mgs_invalid_games()
# This downloads a JSON file to the root of the project called 'mgs_invalid_games.json'.
# It includes the following keys:
# "invalid_games" (list of all invalid games)
# "last_added_id" (the last added invalid game)
# "platform" (should always say "roblox")

# You could manually turn it into a text file (with new lines seperating each game) and use the delete_from_text_file function to delete the badges:
remover.delete_from_text_file(r"C:\example.txt")

# Or, you could create your own script that takes each entry in the JSON and deletes from each game:
import json

for i in json.load(open('mgs_invalid_games.json'))['invalid_games']:
    remover.delete_from_game(i)
```

*This project has been licensed with the MIT License.*