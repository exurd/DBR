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
    try:
        json_file = os.path.join(folder + "/mgs_invalid_games.json")
        txt_file = os.path.join(folder + "/mgs_invalid_games.txt")
        print("Downloading MetaGamerScore invalid Roblox games list...")
        mgs_req = get_request_url("https://metagamerscore.com/api/roblox/invalid_games")
        if mgs_req.ok:
            mgs_json = mgs_req.json()

            if mgs_json:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(mgs_json, f, ensure_ascii=False, indent=4, sort_keys=True)
                    f.close()

                if mgs_json["invalid_games"]:
                    with open(txt_file, "w", encoding="utf-8") as f:
                        for place_id in mgs_json["invalid_games"]:
                            f.write(f"https://www.roblox.com/games/{place_id}\n")
                        f.close()

                print("Success!")
                return True
    except Exception as e:
        print(e)

    print("Failed to download list.")
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
