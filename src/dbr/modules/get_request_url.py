import time
import random
import math
import requests


def get_request_url(url, requestSession=None, retry_amount=8, accept_forbidden=False, accept_not_found=True, initial_wait_time=None) -> requests.Response:
    """
    Internal function to request urls.
    """
    if not isinstance(url, str):
        print("getRequestURL: url was not string type, sending None")
        return None

    if requestSession is None:
        requestSession = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        requestSession.mount('https://', adapter)
        requestSession.mount('http://', adapter)

    tries = 0
    print(f"Requesting {url}...")
    for _ in range(retry_amount):
        if tries != 0:
            print(f"Attempt {tries}...")
        tries += 1
        try:
            response = requestSession.get(url)
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
                # print("Token Validation Failed. Re-validating...")
                # validate_csrf()
                return False
            if sc == 400:
                return False  # Bad Request
            if sc == 429:  # Too Many Requests
                print("Too many requests!")
            if sc == 401:  # Unauthorized
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
            # print(f"Something happened when trying to get [{url}]!")
            print(f"Sleeping {sleep_time} seconds...")
            time.sleep(sleep_time)
    return False
