import os
import json
import re

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


def get_game_from_mgs_id(mgs_id):
    HTML_mgs_place_pattern = re.compile(r"<a target=\"_blank\" href=\"https://www\.roblox\.com/games/([0-9]+)\">https://www\.roblox\.com/games/[0-9]+</a>")
    request = get_request_url(f"https://metagamerscore.com/game/{mgs_id}")
    if request.ok:
        check = HTML_mgs_place_pattern.findall(request.text)
        if check:
            return check[0]
    else:
        return False
