import os
import json
from .get_request_url import get_request_url

def download_mgs_invalid_games(folder=os.getcwd()):
    """
    This downloads MGS' list of Roblox games that were detected as problematic.
    May contain games that are not considered spam, so use with caution.
    """
    json_file = os.path.join(folder + f"/mgs_invalid_games.json")
    print("Downloading MetaGamerScore invalid Roblox games list...")
    mgsReq = get_request_url(f"https://metagamerscore.com/api/roblox/invalid_games")
    if mgsReq.ok:
        universe_json = mgsReq.json()

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(universe_json, f, ensure_ascii=False, indent=4, sort_keys=True)
            f.close()
        
        print("Success!")
        return True
    else:
        print("Failed to download:", mgsReq.text)
        return False
