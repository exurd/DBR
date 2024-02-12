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

*This project has been licensed with the MIT License.*