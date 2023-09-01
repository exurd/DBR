# Dumb Badge(s) Remover
Dumb Badge(s) Remover (DBR) is a Python script that removes [Roblox](https://www.roblox.com) badges, specifically the dumb ones.

## Requirements
The module(s) have been tested to work on [Python 3.11](https://www.python.org/downloads/) and require the packages that are specified in `requirements.txt`.
You can run `pip install -r requirements.txt` in the project's directory to install the packages.

## Configuration
Due to how deleting badges work, you need to authenticate yourself with a ROBLOSECURITY token. To export your token, [read the ro.py's page on it](https://ro.py.jmk.gg/dev/roblosecurity/). BE VERY CAREFUL WITH THE TOKEN!

**DO NOT SHARE IT WITH ANYONE!**

You will also need your Roblox User ID to check for obtained badges. You can find it by going to your profile's URL. It should be a number between `https://www.roblox.com/users/` and `/profile`.

You can use `.example_env` as a starting point. Copy the file and rename it it `.env`.

- Paste the ROBLOSECURITY token into this line: `ROBLOXTOKEN="[TOKEN HERE]"`.
- Insert the User ID with no quotes to: `USERID=[USER ID HERE]`.

For advanced users, you can also change the `USERAGENT=` line to fit more closely to your user agent.

*This project has been licensed with the MIT License.*