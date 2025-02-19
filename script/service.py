import os
import re
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    raise ValueError(Fore.RED + "BASE_URL is not set in the .env file" + Style.RESET_ALL)


def handle_http_errors(response):
    try:
        response.raise_for_status()
    except HTTPError:
        error_message = response.text
        try:
            error_message = response.json().get(
                "detail", response.text
            )
        except ValueError:
            pass

        if 400 <= response.status_code < 500:
            raise HTTPError(
                Fore.RED
                + f"Client Error {response.status_code}: {error_message}"
                + Style.RESET_ALL
            )
        elif response.status_code >= 500:
            raise HTTPError(
                Fore.RED
                + f"Server Error {response.status_code}: Please try again later"
                + Style.RESET_ALL
            )

    return response


def create_test_run(name, timestamp, session):
    if not name or len(name) < 3:
        raise ValueError(
            Fore.RED
            + "Test run name must be at least 3 characters long."
            + Style.RESET_ALL
        )
    if not isinstance(timestamp, str):
        raise ValueError(
            Fore.RED + "Invalid timestamp format. Must be a string." + Style.RESET_ALL
        )

    try:
        response = session.post(
            f"{BASE_URL}/monitor/test-runs",
            json={"name": name, "started_at": timestamp},
        )
        return handle_http_errors(response)
    except ConnectionError:
        raise ConnectionError(
            Fore.RED + "Network error: Unable to reach the server." + Style.RESET_ALL
        )
    except Timeout:
        raise Timeout(Fore.RED + "Server timeout. Try again later." + Style.RESET_ALL)
    except RequestException as e:
        raise Exception(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)


def create_cpu_log(test_id, utilization, timestamp, session):
    if not isinstance(test_id, str):
        raise ValueError(
            Fore.RED + "Invalid test ID. Must be an integer." + Style.RESET_ALL
        )
    if not isinstance(utilization, (int, float)) or not (0 <= utilization <= 100):
        raise ValueError(
            Fore.RED
            + "CPU utilization must be a percentage between 0 and 100."
            + Style.RESET_ALL
        )
    if not isinstance(timestamp, str):
        raise ValueError(
            Fore.RED + "Invalid timestamp format. Must be a string." + Style.RESET_ALL
        )

    try:
        response = session.post(
            f"{BASE_URL}/monitor/cpu-usage/{test_id}",
            json={"cpu_percent": utilization, "timestamp": timestamp},
        )
        return handle_http_errors(response)
    except ConnectionError:
        raise ConnectionError(
            Fore.RED + "Network error: Unable to reach the server." + Style.RESET_ALL
        )
    except Timeout:
        raise Timeout(Fore.RED + "Server timeout. Try again later." + Style.RESET_ALL)
    except RequestException as e:
        raise Exception(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)


def get_cpu_log(test_id, session):
    if not isinstance(test_id, str):
        raise ValueError(
            Fore.RED + "Invalid test ID. Must be an integer." + Style.RESET_ALL
        )

    try:
        response = session.get(f"{BASE_URL}/monitor/cpu-usage/{test_id}")
        return handle_http_errors(response)
    except ConnectionError:
        raise ConnectionError(
            Fore.RED + "Network error: Unable to reach the server." + Style.RESET_ALL
        )
    except Timeout:
        raise Timeout(Fore.RED + "Server timeout. Try again later." + Style.RESET_ALL)
    except RequestException as e:
        raise Exception(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)


def register(name, username, password, session):
    if not name or len(name) < 3:
        raise ValueError(
            Fore.RED + "Name must be at least 3 characters long." + Style.RESET_ALL
        )
    if not re.match(r"^\w{5,15}$", username):
        raise ValueError(
            Fore.RED
            + "Username must be 5-15 characters long and contain only letters, numbers, and underscores."
            + Style.RESET_ALL
        )
    if len(password) < 6:
        raise ValueError(
            Fore.RED + "Password must be at least 6 characters long." + Style.RESET_ALL
        )

    try:
        response = session.post(
            f"{BASE_URL}/auth/register",
            json={"name": name, "username": username, "password": password},
        )
        return handle_http_errors(response)
    except ConnectionError:
        raise ConnectionError(
            Fore.RED + "Network error: Unable to reach the server." + Style.RESET_ALL
        )
    except Timeout:
        raise Timeout(Fore.RED + "Server timeout. Try again later." + Style.RESET_ALL)
    except RequestException as e:
        raise Exception(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)


def login(username, password, session):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = session.post(
            f"{BASE_URL}/auth/login/",
            {"username": username, "password": password},
            headers=headers,
        )

        return handle_http_errors(response)
    except ConnectionError:
        raise ConnectionError(
            Fore.RED + "Network error: Unable to reach the server." + Style.RESET_ALL
        )
    except Timeout:
        raise Timeout(Fore.RED + "Server timeout. Try again later." + Style.RESET_ALL)
    except RequestException as e:
        raise Exception(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)
