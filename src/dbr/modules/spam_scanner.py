from enum import StrEnum
from warnings import warn
import logging
import os
import time

from . import data_save
from .badge_spam_list import zstd_extract_lines
from .get_request_url import get_request_url
from .remover import ROBLOX_URL_PATTERN

PLACE_SPAM = {}
BADGE_SPAM = {}
FOUND_BADGES = set()
FOUND_PLACES = set()

class R_Type(StrEnum):
    BADGE = "badges"
    PLACE = "games"


def create_folder(folder_name):
    """Creates folder for use in spam_scanner"""
    folder = os.path.join(
        data_save.DATA_FOLDER,
        folder_name
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
                    # this pattern creates a tuple of the type and id, so we need to specify we want the second item
                    [l.append(int(ROBLOX_URL_PATTERN.findall(line)[0][1])) for line in lines]
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

    if not create_spam_list():
        print("Could not compile scan list.")
        return False

    if not convert_to_frozensets():
        warn("Could not create frozen sets... might take longer to scan")

    timestamp = round(time.time())
    scanfolder_name = f"scanresults_{str(user_id)}_{str(timestamp)}"
    create_folder(scanfolder_name)


    def _save_lists(id, type:R_Type, folder=os.getcwd(), so_no_head=False):
        """
        Saves a list of Roblox URLs, which can then
        be used in DBR to delete the badges from
        their inventory.

        `folder` is current working directory as users
        will most likely want to see the results there.

        so_no_head set to True will not request a HEAD.
        """
        try:
            filename = os.path.join(folder, f"{scanfolder_name}_{type.upper()}.txt")

            url = f"https://www.roblox.com/{type}/{str(id)}"
            if not so_no_head:
                head = get_request_url(url, headers_only=True, accept_redirects=True, accept_forbidden=True, accept_not_found=True)
                if head.ok:
                    if head.is_redirect and head.headers["location"]:
                        url = f"https://www.roblox.com{head.headers['location']}"

            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"{url}\n")
                f.close()
                return True
        except Exception as e:
            print(f"Error! {e}")
            return False
            
    
    pageNum = page_count
    if page_cursor == None:
        url_request = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&sortOrder=Asc"
    else:
        url_request = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&cursor={page_cursor}&sortOrder=Asc"
    while True:
        print("\n")
        print(f"Next page ({str(pageNum)})...")
        print("---")
        req = get_request_url(url_request)

        if req.ok:
            request_json = req.json()
            if 'errors' in request_json:
                print("Error in uni_json! [", request_json, "]")
                continue

            # save badge inventory data
            data_save.save_data(request_json, f"badge_inventory/{user_id}_{pageNum}.json")

            for badge_entry in request_json['data']:
                place_id = badge_entry['awarder']['id']
                badge_id = badge_entry['id']
                p = b = False
                if not place_id in FOUND_PLACES:
                    p = [key for key, s in PLACE_SPAM.items() if place_id in s]
                else:
                    # add badges from games that are in FOUND_PLACES
                    # do not get their name as there could be thousands
                    # (if not millions) of these in an inventory
                    FOUND_BADGES.add(badge_id)
                    _save_lists(badge_id, R_Type.BADGE, so_no_head=True)
                if not badge_id in FOUND_BADGES:
                    b = [key for key, s in BADGE_SPAM.items() if badge_id in s]
                if p or b:
                    if p:
                        print(f"Place {place_id} found in {p}")
                    if b:
                        print(f"Badge {badge_id} found in {b}")
                    logging.info(f"Badge: {badge_id} | Place: {place_id} (from: {', '.join(p)})")

                    if not place_id in FOUND_PLACES:
                        FOUND_PLACES.add(place_id)
                        _save_lists(place_id, R_Type.PLACE)

                    if not badge_id in FOUND_BADGES:
                        FOUND_BADGES.add(badge_id)
                        _save_lists(badge_id, R_Type.BADGE)

            print(f"Found {len(FOUND_PLACES)} place(s), {len(FOUND_BADGES)} badge(s).")

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
