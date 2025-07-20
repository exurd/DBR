import logging
import os
import re
import time

from . import data_save
from .badge_spam_list import zstd_extract_lines
from .get_request_url import get_request_url

# i made a mistake while creating the spam lists...
# some lists don't have `www.` so pattern `(?:www\.)?`
# is needed to avoid issues
roblox_pattern = re.compile(r"https:\/\/(?:www\.)?roblox\.com\/games\/([0-9]+)")

PLACE_SPAM = {}
BADGE_SPAM = {}
FOUND_BADGES = set()
FOUND_PLACES = set()


def create_folder(user_id):
    """Creates folder for use in spam_scanner"""
    folder = os.path.join(
        data_save.DATA_FOLDER,
        "scanresults_"
        f"{str(user_id)}_"
        f"{str(round(time.time()))}"
    )
    data_save.init(root_folder=folder)
    os.makedirs((folder + "/badge_inventory"), exist_ok=True)
    logging.basicConfig(filename=os.path.join(folder, "results.log"),
                        filemode="w",
                        format="%(asctime)s,%(msecs)d %(levelname)s %(message)s",
                        datefmt="%H:%M:%S",
                        level=logging.INFO
                    )



def create_spam_list(folder=os.getcwd()):
    """
    Creates spam place ID list.
    
    Uses the following sources (if they exist locally):
        - mgs_invalid_games.json
        - exurd/badge-spam-lists

    Both are combined into one list of place IDs using
    a dictionary and frozensets.
    """
    global PLACE_SPAM
    global BADGE_SPAM

    # TODO: allow scan to be tracked back to it's roots (or multiple roots)...
    print("Creating list of spam place IDs...")
    try:
        mgs_invalid_games_json = os.path.join(folder, "mgs_invalid_games.json")
        if json := data_save.load_data(mgs_invalid_games_json):
            l = []
            [l.append(int(place_id)) for place_id in json["invalid_games"]]
            PLACE_SPAM["mgs_invalid_games.json"] = l

        badge_spam_list_folder = os.path.join(folder, "badge-spam-lists-main/")
        for filename in os.listdir(badge_spam_list_folder):
            if ".txt.zst" in filename:
                path = os.path.join(badge_spam_list_folder, filename)
                if lines := zstd_extract_lines(path):
                    l = []
                    [l.append(int(roblox_pattern.findall(line)[0])) for line in lines]
                    PLACE_SPAM[filename] = l

        data_save.save_data(PLACE_SPAM, "spam_places_list.json")
    except Exception as e:
        print(f"Failed to create spam place list: {e}")
        return False

    print("Creating list of spam badge IDs...")
    sb_txt = os.path.join(folder, "spam_badges.txt")
    if os.path.exists(sb_txt):
        try:
            with open(sb_txt, mode="r") as f:
                lines = f.readlines()
                f.close()
            l = []
            [l.append(int(line.strip())) for line in lines]
            BADGE_SPAM["spam_badges.txt"] = l

            data_save.save_data(list(BADGE_SPAM), "spam_badges_list.json")
        except Exception as e:
            print(f"Failed to create spam place list: {e}")
            return False

    return True



def convert_to_frozensets():
    """
    Converts lists in a dictonary to frozensets.
    This allows for quicker lookup times.
    """
    global PLACE_SPAM
    global BADGE_SPAM

    try:
        for entry in PLACE_SPAM:
            PLACE_SPAM[entry] = frozenset(PLACE_SPAM[entry])
        return True
    except Exception as e:
        print(e)
        return False


def scan_inventory(user_id:int, page_cursor=None, page_count=1) -> tuple[set, set]:
    """
    Checks a user's inventory for spam badges. DOES NOT DELETE BADGES.
    Returns a tuple of two sets: `FOUND_BADGES` and `FOUND_PLACES`.
    """
    global FOUND_BADGES
    global FOUND_PLACES
    

    pageNum = page_count
    if page_cursor == None:
        url_request = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&sortOrder=Asc"
    else:
        url_request = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&cursor={page_cursor}&sortOrder=Asc"
    while True:
        print("\n---")
        print(f"Next page ({str(pageNum)})...")
        print("---\n")
        req = get_request_url(url_request)

        if req.ok:
            request_json = req.json()
            if 'errors' in request_json:
                print("Error in uni_json! [", request_json, "]")
                continue

            for badge_entry in request_json['data']:
                place_id = badge_entry['awarder']['id']
                badge_id = badge_entry['id']
                k = [key for key, s in PLACE_SPAM.items() if place_id in s]
                if k:
                    logging.info(f"Badge: {badge_id} | Place: {place_id} (from: {', '.join(k)})")
                    FOUND_PLACES.add(place_id)

                k = [key for key, s in BADGE_SPAM.items() if badge_id in s]
                if k:
                    logging.info(f"Badge: {badge_id} | Place: {place_id} (from: {', '.join(k)})")
                    FOUND_BADGES.add(badge_id)

            print(f"Found {len(FOUND_PLACES)} place(s), {len(FOUND_BADGES)} badge(s).")

            # save badge inventory data
            data_save.save_data(request_json, f"badge_inventory/{user_id}_{pageNum}.json")

            if request_json['nextPageCursor'] is None:
                print("Searched all badges.")
                return (FOUND_BADGES, FOUND_PLACES)
            else:
                pageNum += 1
                print("Checking next page of badges...")
                url_request = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&cursor={request_json['nextPageCursor']}&sortOrder=Asc"
        else:
            print("Trying page", str(pageNum), "again...")
            time.sleep(2)
