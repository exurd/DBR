import os
from dotenv import load_dotenv
import requests
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import time
import json
import concurrent.futures
import threading
import sys

print_lock = threading.Lock()
#list_lock = threading.Lock()

def print_thread_safe(message):
    with print_lock:
        print(message)

def get_data_file_path():
    data_folder = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), "DBR_Cache") # places cache folder in root of project
    os.makedirs(data_folder, exist_ok=True)
    return data_folder

def load_data(filename):
    data_file_path = os.path.join(get_data_file_path(), filename)
    if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
        with open(data_file_path, "r") as f:
            data = json.load(f)
            f.close()
    else:
        data = []
    return data

def save_data(data, filename):
    data_file_path = os.path.join(get_data_file_path(), filename)
    with open(data_file_path, "w") as f:
        json.dump(data, f)
        f.close()

# load data of json files
checked_places = load_data("checked_places.json")
#checked_badges = load_data("checked_badges.json")

# def append_to_checked_badges(item):
#     with list_lock:
#         checked_badges.append(item)

load_dotenv() # place .env in the root of the project. not in the modules folder!!

user_id = int(os.getenv("USERID"))
NUM_THREADS = int(os.getenv("NUMTHREADS"))

requestSession = requests.Session() # initiate a session
adapter = requests.adapters.HTTPAdapter(max_retries=5)
requestSession.mount('https://', adapter)
requestSession.mount('http://', adapter)
requestSession.headers['User-Agent'] = str(os.getenv("USERAGENT"))
requestSession.cookies[".ROBLOSECURITY"] = str(os.getenv("ROBLOXTOKEN"))
requestSession.headers['Referer'] = "https://www.roblox.com"

def validate_CSRF():
    requestSession.headers["X-CSRF-TOKEN"] = None # Reset token to stop actual sign out
    req = requestSession.post(url="https://auth.roblox.com/v2/logout")
    requestSession.headers["X-CSRF-TOKEN"] = req.headers["X-CSRF-Token"]

validate_CSRF()

def delete_badge(badge_id):
    print_thread_safe("Deleting badge " + str(badge_id) + " from account...")
    attempts = 0
    while attempts < 3:
        url = f"https://badges.roblox.com/v1/user/badges/{str(badge_id)}"

        #try:
        response = requestSession.delete(url)

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
            validate_CSRF()
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

def delete_from_game(placeId):
    print("Getting universe from", str(placeId) + "...")
    universeReq = requestSession.get(f"https://apis.roblox.com/universes/v1/places/{str(placeId)}/universe")

    if universeReq.ok:
        uni_json = universeReq.json()
        if 'errors' in uni_json:
            print("Error in uni_json! [", uni_json, "]")
            #continue
        else:
            universeId = uni_json['universeId']
            
            print("Searching universe's badges...")
            universe_json = requestSession.get(f"https://badges.roblox.com/v1/universes/{str(universeId)}/badges?limit=100&sortOrder=Asc").json()

            #print(universe_json)
            pageCount = 0
            while True:
                nobadgestoremove = False
                badge_check_list = []
                pageCount += 1
                print("Checking badges on page", str(pageCount) + "...")
                for badge in universe_json['data']:
                    badgeId = badge['id']
                    # if badgeId in checked_badges:
                    #     print("Badge", str(badgeId),  "already checked, skipping...")
                    #     continue
                    # else:
                    badge_check_list.append(str(badgeId))

                if badge_check_list == []:
                    nobadgestoremove = True
                else:
                    while True:
                        badge_check = requestSession.get(f"https://badges.roblox.com/v1/users/{str(user_id)}/badges/awarded-dates?badgeIds={', '.join(badge_check_list)}") # shows awarded badges en masse; easy!
                        if badge_check.ok:
                            badge_check = badge_check.json()
                            break
                        time.sleep(3)
                    if badge_check['data'] == []:
                        nobadgestoremove = True

                #print(badge_check['data'])
                
                #print(badge_list)
                #print(nobadgestoremove)


                if nobadgestoremove == False:
                    badge_delete_list = []
                    for badge in badge_check['data']:
                        badgeId = badge['badgeId']
                        # if badgeId in checked_badges:
                        #     print("Badge in checked_badges.json, skipping...")
                        #     continue
                        # else:
                        badge_delete_list.append(badgeId)

                    #user_check = requestSession.get(f"https://inventory.roblox.com/v1/users/{str(user_id)}/items/2/{str(badge['id'])}/is-owned")
                    
                    #if user_check.text == "true":
                    #print("")
                    
                    print(f"/----||{str(pageCount)}||----\\")

                    #delete_badge(badgeId)
                    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                        executor.map(delete_badge, badge_delete_list) # i have NO IDEA how the fuck this works, but if i want to go through 2000 games by the next two weeks, this *has* to be implemented.
                    
                    print(f"\\----||{str(pageCount)}||----/")

                    print("All badges on the page have been removed.") #print("Executor has killed mapped badges.")
                    #print(universe_json['nextPageCursor'])
                    #print("Saving progress to folder...")
                    #print(checked_badges) # for some reason threading only gives out []; time to let this feature die
                    #save_data(checked_badges,"checked_badges.json") # it's for the sake of faster times and besides, it kinda complicated things
                    #print("Saved!")
                    time.sleep(5)
                if universe_json['nextPageCursor'] == None:
                    print("Searched all badges.")
                    return
                else:
                    print("Checking next page of badges...")
                    time.sleep(3)
                    universe_json = requestSession.get(f"https://badges.roblox.com/v1/universes/{str(universeId)}/badges?limit=100&sortOrder=Asc&cursor={universe_json['nextPageCursor']}").json()
    else:
        print("Error! [", universeReq, "]")
        #continue

def delete_from_player(userId):
    print("Finding user", str(userId) + "...")
    playerReq = requestSession.get(f"https://games.roblox.com/v2/users/{userId}/games?limit=50&sortOrder=Asc")
    #print(playerReq)
    if playerReq.ok:
        game_json = playerReq.json()
        if 'errors' in game_json:
            print("Error in uni_json! [", game_json, "]")
            #continue
        else:
            print("Searching player's games...")

            placeCount = 0
            while True:
                for game in game_json['data']:
                    placeCount += 1
                    print("Checking place", str(placeCount) + "...")
                    rootPlaceId = game['rootPlace']['id']
                    if rootPlaceId in checked_places:
                        print("Already checked place, skipping...")
                        continue
                    else:
                        print("\/\/\/\/\/\/\/")
                        print("--------------")
                        delete_from_game(rootPlaceId)
                        print("--------------")
                        print("/\/\/\/\/\/\/\\")
                        checked_places.append(rootPlaceId)
                        save_data(checked_places,"checked_places.json")
                        time.sleep(3)

                #print(universe_json['nextPageCursor'])
                if game_json['nextPageCursor'] == None:
                    print("Searched all games.")
                    return
                else:
                    print("Checking next page of games...")
                    time.sleep(3)
                    game_json = requestSession.get(f"https://games.roblox.com/v2/users/{userId}/games?limit=50&sortOrder=Asc&cursor={game_json['nextPageCursor']}").json()
    else:
        print("Error! [", playerReq, "]")
        #continue

def delete_from_group(groupId):
    print("Finding group", str(groupId) + "...")
    groupReq = requestSession.get(f"https://games.roblox.com/v2/groups/{groupId}/games?accessFilter=2&limit=100&sortOrder=Asc") # gamesV2 only shows 100 games; no page cursor in the api appears. using original
    #print(playerReq)
    if groupReq.ok:
        group_json = groupReq.json()
        print(group_json)
        if 'errors' in group_json:
            print("Error in group_json! [", group_json, "]")
            #continue
        else:
            print("Searching group's games...")

            placeCount = 0
            while True:
                for game in group_json['data']:
                    placeCount += 1
                    print("Checking place", str(placeCount) + "...")
                    rootPlaceId = game['rootPlace']['id']
                    if rootPlaceId in checked_places:
                        print("Already checked place, skipping...")
                        continue
                    else:
                        print("\/\/\/\/\/\/\/")
                        print("--------------")
                        delete_from_game(rootPlaceId)
                        print("--------------")
                        print("/\/\/\/\/\/\/\\")
                        checked_places.append(rootPlaceId)
                        save_data(checked_places,"checked_places.json")
                        time.sleep(3)

                #print(universe_json['nextPageCursor'])
                if group_json['nextPageCursor'] == None:
                    print("Searched all games.")
                    return
                else:
                    print("Checking next page of games...")
                    time.sleep(3)
                    group_json = requestSession.get(f"https://games.roblox.com/v2/groups/{groupId}/games?accessFilter=2&limit=100&sortOrder=Asc&cursor={group_json['nextPageCursor']}").json()
    else:
        print("Error! [", groupReq, "]")
        
def delete_from_text_file(text_file):
    with open(text_file, 'r') as file:
        for line in file:
            url = line.strip()
            #print(url)
            check = PurePosixPath(unquote(urlparse(url).path)).parts

            if check[1] == "badges": # if a badge then use that to check
                badgeId = int(check[2])

                # if badgeId in checked_badges:
                #     print("Badge", str(badgeId),  "already checked, skipping...")
                #     continue

                user_check = requestSession.get(f"https://inventory.roblox.com/v1/users/{str(user_id)}/items/2/{str(badgeId)}/is-owned")
                if user_check.text == "true":
                    delete_badge(badgeId)

                #checked_badges.append(badgeId)
                #save_data(checked_badges,"checked_badges.json")

            elif check[1] == "games":
                placeId = int(check[2])

                if placeId in checked_places:
                    print("Already checked place, skipping...")
                    continue

                delete_from_game(placeId)

                checked_places.append(placeId)
                save_data(checked_places,"checked_places.json")

            elif check[1] == "users":
                userId = int(check[2])
                
                delete_from_player(userId)

            time.sleep(3)

def download_mgs_invalid_games(folder=os.getcwd()):
    json_file = os.path.join(folder + f"/mgs_invalid_games.json")
    # if os.path.isfile(json_file):
    #     print("Already downloaded... Not downloading...")
    #     return None
    #     #print("not downloading file", universeId, "; already downloaded")
    # else:
    print("Downloading MetaGamerScore invalid Roblox games list...")
    mgsReq = requestSession.get(f"https://metagamerscore.com/api/roblox/invalid_games")
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