from datetime import datetime, timezone
import json

from .get_request_url import get_request_url

BOR_DATABASE_API_URL = "https://bor-valuable-badge-database-production.up.railway.app/api/v3"


def get_bor_universe_info(universe_id):
    """
    JSON Response for Universe ID 156639:
    {
        "data": [
            {
                "badge_count": 15,
                "badges": {
                    "14417332": {
                        "awarding_universe": 156639,
                        "badge_id": 14417332,
                        "created": 1250140952,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "14468729": {
                        "awarding_universe": 156639,
                        "badge_id": 14468729,
                        "created": 1250213258,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "14468788": {
                        "awarding_universe": 156639,
                        "badge_id": 14468788,
                        "created": 1250213341,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "14468882": {
                        "awarding_universe": 156639,
                        "badge_id": 14468882,
                        "created": 1250213449,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "14469303": {
                        "awarding_universe": 156639,
                        "badge_id": 14469303,
                        "created": 1250213901,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "14469725": {
                        "awarding_universe": 156639,
                        "badge_id": 14469725,
                        "created": 1250214466,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "14498946": {
                        "awarding_universe": 156639,
                        "badge_id": 14498946,
                        "created": 1250275574,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "37135144": {
                        "awarding_universe": 156639,
                        "badge_id": 37135144,
                        "created": 1287511387,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "38830432": {
                        "awarding_universe": 156639,
                        "badge_id": 38830432,
                        "created": 1289330523,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "81077843": {
                        "awarding_universe": 156639,
                        "badge_id": 81077843,
                        "created": 1337299340,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "83094426": {
                        "awarding_universe": 156639,
                        "badge_id": 83094426,
                        "created": 1339264402,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "83094517": {
                        "awarding_universe": 156639,
                        "badge_id": 83094517,
                        "created": 1339264446,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "83094644": {
                        "awarding_universe": 156639,
                        "badge_id": 83094644,
                        "created": 1339264518,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "83094935": {
                        "awarding_universe": 156639,
                        "badge_id": 83094935,
                        "created": 1339264677,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                    "83333920": {
                        "awarding_universe": 156639,
                        "badge_id": 83333920,
                        "created": 1339461657,
                        "found": True,
                        "is_nvl": False,
                        "value": 2,
                    },
                },
                "found": True,
                "free_badges": [],
                "universe_id": 156639,
            }
        ]
    }

    I have no idea what "is_nvl" is.
    """
    bor_url = f"{BOR_DATABASE_API_URL}/query/byuniverseids?universeIds={str(universe_id)}"
    req = get_request_url(bor_url)
    if req.ok:
        bor_info = req.json()
        return bor_info
    return []


def convert_to_roblox_response(universe_id):
    """
    Convert the response we get from the BoR API to the Roblox Universe Badges API.
    """
    universe_info = {}
    universe_info["previousPageCursor"] = None
    universe_info["nextPageCursor"] = None  # so we don't loop around for the "next page"
    universe_info["data"] = []

    bor_info = get_bor_universe_info(universe_id)
    if bor_info == []:
        return {}

    badges = bor_info["data"][0]["badges"]
    for id in badges:
        badge_dict = {}
        badge_info = badges[id]
        
        badge_dict["id"] = int(id)
        badge_dict["name"] = None
        badge_dict["description"] = None
        badge_dict["displayName"] = None
        badge_dict["displayDescription"] = None
        badge_dict["enabled"] = None
        badge_dict["iconImageId"] = None
        badge_dict["displayIconImageId"] = None

        try:
            dt_created = datetime.fromtimestamp(badge_info["created"], tz=timezone.utc)
            badge_dict["created"] = dt_created.isoformat(timespec="milliseconds")
        except TypeError as e:
            print(e)
            badge_dict["created"] = badge_info["created"]

        badge_dict["updated"] = None
        badge_dict["statistics"] = {}
        badge_dict["statistics"]["pastDayAwardedCount"] = None
        badge_dict["statistics"]["awardedCount"] = None
        badge_dict["statistics"]["winRatePercentage"] = None
        badge_dict["awardingUniverse"] = {}
        badge_dict["awardingUniverse"]["id"] = universe_id
        badge_dict["awardingUniverse"]["name"] = None
        badge_dict["awardingUniverse"]["rootPlaceId"] = None

        universe_info["data"].append(badge_dict)
    return universe_info
