import os
import json
import re

from .get_request_url import get_request_url


mgs_place_html_pattern = re.compile(r"<a target=\"_blank\" href=\"https://www\.roblox\.com/games/([0-9]+)\">https://www\.roblox\.com/games/[0-9]+</a>")


def download_mgs_invalid_games(folder=os.getcwd()):
    """
    This downloads MGS' list of Roblox games that were detected as problematic.
    May contain games that are not considered spam, so use with caution.
    """
    json_file = os.path.join(folder + "/mgs_invalid_games.json")
    print("Downloading MetaGamerScore invalid Roblox games list...")
    mgs_req = get_request_url("https://metagamerscore.com/api/roblox/invalid_games")
    if mgs_req.ok:
        universe_json = mgs_req.json()

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(universe_json, f, ensure_ascii=False, indent=4, sort_keys=True)
            f.close()

        print("Success!")
        return True

    print("Failed to download:", mgs_req.text)
    return False


def get_game_from_mgs_id(mgs_id):
    """
    Gets Roblox Place ID from MGS game ID.
    """
    request = get_request_url(f"https://metagamerscore.com/game/{mgs_id}")
    if request.ok:
        check = mgs_place_html_pattern.findall(request.text)
        if check:
            return check[0]
    else:
        return False
