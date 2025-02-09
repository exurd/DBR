from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import time
import concurrent.futures
import threading
import math
import random

import requests

from . import data_save
from .get_request_url import get_request_url


print_lock = threading.Lock()


def print_thread_safe(message):
    """Print messages while using ThreadPoolExecutor."""
    with print_lock:
        print(message)


NUM_THREADS = 2


requestSession = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=5)
requestSession.mount('https://', adapter)
requestSession.mount('http://', adapter)
requestSession.headers['Referer'] = "https://www.roblox.com"


def get_user_from_token() -> dict:
    """
    Gets user ID from .ROBLOSECURITY token.
    Results are not cached.
    """
    usercheck = get_request_url("https://users.roblox.com/v1/users/authenticated", requestSession=requestSession)
    if usercheck is not None:
        if usercheck.ok:
            return usercheck.json()
    return None


USER_ID = None


def validate_csrf() -> str:
    """
    Gets X-CSRF-Token for Roblox.
    """
    requestSession.headers["X-CSRF-Token"] = None
    req = requestSession.post(url="https://auth.roblox.com/v2/logout", timeout=60)
    return req.headers["X-CSRF-Token"]


def init(user_agent=None, rbx_token=None):
    """
    Initializes the request session with user agent and cookies.
    """
    global USER_ID

    if user_agent is not None:
        requestSession.headers["User-Agent"] = str(user_agent)

    if rbx_token is not None:
        requestSession.cookies[".ROBLOSECURITY"] = str(rbx_token)
    else:
        print("Roblox Token was not specified, exiting.")
        return False

    requestSession.headers["X-CSRF-Token"] = validate_csrf()

    USER_ID = get_user_from_token()
    if USER_ID is not None:
        USER_ID = USER_ID["id"]
    else:
        print("The User ID could not be found. Please check if the specified Roblox token is correct. Exiting.")
        return False
    return True


def delete_request_url(url, retry_amount=8, accept_forbidden=False, accept_not_found=True, initial_wait_time=None) -> requests.Response:
    """
    Internal function to HTTP DELETE urls.
    """
    if not isinstance(url, str):
        print("delete_request_url: url was not string type, sending None")
        return None

    tries = 0
    print(f"Deleting {url}...")
    for _ in range(retry_amount):
        if tries != 0:
            print(f"Attempt {tries}...")
        tries += 1
        try:
            response = requestSession.delete(url)
            print(f"Response Status Code: {response.status_code}")
            sc = response.status_code
            if sc in (200, 302):
                return response
            if accept_forbidden and sc == 403:
                return response  # Forbidden (if acceptForbidden)
            if accept_not_found and sc == 404:
                return response  # Not Found (if acceptNotFound)
            if sc == 410:
                return response  # Gone
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            print("Timed out!")
            print(f"Request failed: {e}")
        except requests.exceptions.TooManyRedirects as e:
            print("Too many redirects!")
            print(f"Request failed: {e}")
            return False
        except requests.exceptions.HTTPError:
            if sc in (403, 419):  # Forbidden (Roblox sends 403 for some requests that need a CSRF token), Page Expired
                print("Token Validation Failed. Re-validating...")
                # validate_csrf()
            elif sc == 400:
                return False  # Bad Request
            elif sc == 429:  # Too Many Requests
                print("Too many requests!")
            elif sc == 401:  # Unauthorized
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
        if tries < retry_amount:
            sleep_time = random.randint(
                math.floor(2 ** (tries - 0.5)),
                math.floor(2 ** tries)
                )
            if initial_wait_time is not None:
                sleep_time = int(initial_wait_time)
                initial_wait_time = None
            print(f"Sleeping {sleep_time} seconds for {url}...")
            time.sleep(sleep_time)
    return False


def delete_badge(badge_id):
    """
    Deletes badge from user's inventory.

    User ID must already be set in order to successfully delete.
    """
    print_thread_safe("Deleting badge " + str(badge_id) + " from account...")
    attempts = 0

    # 3 attempts here * 8 attempts in delete_request_url() = 24 total attempts
    while attempts < 3:
        url = f"https://badges.roblox.com/v1/user/badges/{str(badge_id)}"

        # try:
        response = delete_request_url(url)

        if response.status_code == 200:
            print_thread_safe(f"Badge {badge_id} was succesfully removed.")
            attempts = 3
            time.sleep(.75)
        elif response.status_code == 404:
            print_thread_safe(f"Badge {badge_id} is invalid or does not exist.")
            attempts = 3
            time.sleep(.75)
        elif response.status_code == 403:
            print_thread_safe("Token Validation Failed. Re-validating...")
            time.sleep(5)
            requestSession.headers["X-CSRF-Token"] = validate_csrf()
        elif response.status_code == 401:
            print_thread_safe("Authorization has been denied for this request.")
            time.sleep(5)
        else:
            print_thread_safe("Badge removal failed.")
            print_thread_safe(f"Response: {response.status_code}, {response.text}")
            time.sleep(5)
        # except ConnectionError:
        #     print("Connection Error! Attempting to retry...")
        #     time.sleep(10)
        #     validate()
        attempts += 1


def delete_from_game(place_id):
    """
    Collects badges from a place ID, checks which were awarded to
    the user and puts any badges through delete_from_badge().
    """
    print("Getting universe from", str(place_id) + "...")
    universe_req = get_request_url(f"https://apis.roblox.com/universes/v1/places/{str(place_id)}/universe", requestSession=requestSession)

    if universe_req.ok:
        uni_json = universe_req.json()
        if 'errors' in uni_json:
            print("Error in uni_json! [", uni_json, "]")
        else:
            universe_id = uni_json['universeId']

            print("Searching universe's badges...")
            universebadges_req = get_request_url(f"https://badges.roblox.com/v1/universes/{str(universe_id)}/badges?limit=100&sortOrder=Asc", requestSession=requestSession)
            if universebadges_req.ok:
                universebadges_json = universebadges_req.json()
                if 'data' not in universebadges_json:
                    print("No data in universebadges_json? Skipping...")
                    return False

                page_count = 0
                while True:
                    nobadgestoremove = False
                    badge_check_list = []
                    page_count += 1
                    print("Checking badges on page", str(page_count) + "...")

                    for badge in universebadges_json['data']:
                        badge_id = badge['id']
                        badge_check_list.append(str(badge_id))

                    if badge_check_list == []:
                        nobadgestoremove = True
                    else:
                        while True:
                            badge_check = get_request_url(f"https://badges.roblox.com/v1/users/{str(USER_ID)}/badges/awarded-dates?badgeIds={','.join(badge_check_list)}", requestSession=requestSession)  # shows awarded badges en masse; easy!
                            print(badge_check)
                            if badge_check.ok:
                                badge_check = badge_check.json()
                                break
                            time.sleep(3)
                        if badge_check['data'] == []:
                            nobadgestoremove = True

                    if nobadgestoremove is False:
                        badge_delete_list = []
                        for badge in badge_check['data']:
                            badge_id = badge['badgeId']
                            badge_delete_list.append(badge_id)

                        print(f"|----||{str(page_count)}||----|")

                        # delete_badge(badgeId)
                        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                            executor.map(delete_badge, badge_delete_list)

                        print(f"|----||{str(page_count)}||----|")

                        print("All badges on the page have been removed.")
                        time.sleep(5)
                    if universebadges_json['nextPageCursor'] is None:
                        print("Searched all badges.")
                        return True
                    else:
                        print("Checking next page of badges...")
                        time.sleep(3)
                        universebadges_json = get_request_url(f"https://badges.roblox.com/v1/universes/{str(universe_id)}/badges?limit=100&sortOrder=Asc&cursor={universebadges_json['nextPageCursor']}", requestSession=requestSession).json()
    else:
        print("Error! [", universe_req, "]")
    return False


def delete_from_player(player_id):
    """
    Checks the inventory of a player for their games,
    and puts any games found through delete_from_game().
    """
    print("Finding user", str(player_id) + "...")
    player_req = get_request_url(f"https://games.roblox.com/v2/users/{player_id}/games?limit=50&sortOrder=Asc", requestSession=requestSession)
    # print(playerReq)
    if player_req.ok:
        game_json = player_req.json()
        if 'errors' in game_json:
            print("Error in game_json! [", game_json, "]")
            # continue
        else:
            print("Searching player's games...")

            place_count = 0
            while True:
                for game in game_json['data']:
                    place_count += 1
                    print("Checking place", str(place_count) + "...")

                    root_place_id = game['rootPlace']['id']
                    if root_place_id in data_save.CHECKED_PLACES:
                        print("Already checked place, skipping...")
                        continue

                    print("⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄")
                    print("--------------")
                    delete_from_game(root_place_id)
                    print("--------------")
                    print("^^^^^^^^^^^^^^")
                    data_save.CHECKED_PLACES.append(root_place_id)
                    data_save.save_data(data_save.CHECKED_PLACES, "checked_places.json")
                    time.sleep(3)

                # print(universe_json['nextPageCursor'])
                if game_json['nextPageCursor'] is None:
                    print("Searched all games.")
                    return True
                else:
                    print("Checking next page of games...")
                    time.sleep(3)
                    game_json = get_request_url(f"https://games.roblox.com/v2/users/{player_id}/games?limit=50&sortOrder=Asc&cursor={game_json['nextPageCursor']}", requestSession=requestSession).json()
    else:
        print("Error! [", player_req, "]")
    return False


def delete_from_group(group_id):
    """
    Checks public game list for a group,
    and puts any games found through delete_from_game().

    Note the API will not show any private game that is in a group.
    """
    print("Finding group", str(group_id) + "...")

    # v2/groups/*/gamesV2 only shows 100 games; no page cursor in the api appears. using original
    group_req = get_request_url(f"https://games.roblox.com/v2/groups/{group_id}/games?accessFilter=2&limit=100&sortOrder=Asc", requestSession=requestSession)
    # print(playerReq)
    if group_req.ok:
        group_json = group_req.json()
        # print(group_json)
        if 'errors' in group_json:
            print("Error in group_json! [", group_json, "]")
        else:
            print("Searching group's games...")

            place_count = 0
            while True:
                for game in group_json['data']:
                    place_count += 1
                    print("Checking place", str(place_count) + "...")
                    root_place_id = game['rootPlace']['id']
                    if root_place_id in data_save.CHECKED_PLACES:
                        print("Already checked place, skipping...")
                        continue
                    else:
                        print("⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄")
                        print("--------------")
                        delete_from_game(root_place_id)
                        print("--------------")
                        print("^^^^^^^^^^^^^^")
                        data_save.CHECKED_PLACES.append(root_place_id)
                        data_save.save_data(data_save.CHECKED_PLACES, "checked_places.json")
                        time.sleep(3)

                # print(universe_json['nextPageCursor'])
                if group_json['nextPageCursor'] is None:
                    print("Searched all games.")
                    return True
                else:
                    print("Checking next page of games...")
                    time.sleep(3)
                    group_json = get_request_url(f"https://games.roblox.com/v2/groups/{group_id}/games?accessFilter=2&limit=100&sortOrder=Asc&cursor={group_json['nextPageCursor']}", requestSession=requestSession).json()
    else:
        print("Error! [", group_req, "]")
    return False


def delete_from_text_file(lines):
    """
    Accepts a text file with Roblox urls.

    Example:
    ```
    https://www.roblox.com/games/123
    https://www.roblox.com/users/1234
    https://www.roblox.com/badges/12345
    ```
    """
    for line in lines:
        url = line.strip()
        # print(url)
        check = PurePosixPath(unquote(urlparse(url).path)).parts

        if check[1] == "badges":  # if a badge then use that to check
            badge_id = int(check[2])

            user_check = get_request_url(f"https://inventory.roblox.com/v1/users/{str(USER_ID)}/items/2/{str(badge_id)}/is-owned", requestSession=requestSession)
            if user_check.text == "true":
                delete_badge(badge_id)

        elif check[1] == "games":
            place_id = int(check[2])

            if place_id in data_save.CHECKED_PLACES:
                print("Already checked place, skipping...")
                continue

            delete_from_game(place_id)

            data_save.CHECKED_PLACES.append(place_id)
            data_save.save_data(data_save.CHECKED_PLACES, "checked_places.json")

        elif check[1] == "users":
            player_id = int(check[2])

            delete_from_player(player_id)

        time.sleep(3)
