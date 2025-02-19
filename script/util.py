import re
import os
import sys
from requests import Session
from requests.exceptions import HTTPError, ConnectionError, Timeout
from service import register, login
from colorama import Fore, Style


def input_manager(text):
    try:
        value = input(text).strip()
        if not value:
            print(
                Fore.YELLOW
                + "Input cannot be empty. Please try again."
                + Style.RESET_ALL
            )
            return input_manager(text)
        return value
    except EOFError:
        print(
            Fore.RED
            + "\nUnexpected end of input (CTRL+D detected). Exiting."
            + Style.RESET_ALL
        )
        sys.exit(1)
    except KeyboardInterrupt:
        print(
            Fore.RED
            + "\nProcess interrupted by user (CTRL+C detected). Exiting."
            + Style.RESET_ALL
        )
        sys.exit(1)


def register_user(session: Session):
    while True:
        name = input_manager("Enter name: ")
        if not re.match(r"^[A-Za-z]+( [A-Za-z]+)*$", name) or len(name) < 3:
            print(
                Fore.YELLOW + "Invalid name. It must be at least 3 characters and only"
                "contain letters and spaces." + Style.RESET_ALL
            )
            continue

        username = input_manager("Enter username: ")
        if not re.match(r"^\w{5,15}$", username):
            print(
                Fore.YELLOW + "Invalid username. It must be 5-15 characters long"
                "and contain only letters, numbers, and underscores." + Style.RESET_ALL
            )
            continue

        password = input_manager("Enter password: ")
        if len(password) < 6:
            print(
                Fore.YELLOW
                + "Password must be at least 6 characters long."
                + Style.RESET_ALL
            )
            continue

        try:
            response = register(name, username, password, session)
            response.raise_for_status()

            print(
                Fore.GREEN
                + "User registered successfully! Login to continue."
                + Style.RESET_ALL
            )
            return
        except ConnectionError:
            print(
                Fore.RED
                + "Connection error. Unable to establish connection"
                + Style.RESET_ALL
            )
        except Timeout:
            print(Fore.YELLOW + "Server timeout. Try again later." + Style.RESET_ALL)
        except HTTPError as e:
            if response.status_code == 400:
                print(
                    Fore.YELLOW
                    + "Invalid registration details. Please check your inputs."
                    + Style.RESET_ALL
                )
            elif response.status_code == 409:
                print(
                    Fore.YELLOW
                    + "Username already exists. Choose a different one."
                    + Style.RESET_ALL
                )
            else:
                print(Fore.RED + f"Registration error: {e}" + Style.RESET_ALL)
        except Exception as e:
            print(
                Fore.RED
                + f"Unexpected error during registration: {e}"
                + Style.RESET_ALL
            )

        print(Fore.YELLOW + "Please try registration again.\n" + Style.RESET_ALL)


def login_user(session: Session):
    while True:
        username = input_manager("Enter username: ")
        if not re.match(r"^\w{5,15}$", username):
            print(
                Fore.YELLOW
                + "Invalid username. It must be 5-15 characters long and contain only letters,"
                "numbers, and underscores." + Style.RESET_ALL
            )
            continue

        password = input_manager("Enter password: ")
        if len(password) < 6:
            print(
                Fore.YELLOW
                + "Password must be at least 6 characters long."
                + Style.RESET_ALL
            )
            continue
        response = None
        try:
            response = login(username, password, session)
            response.raise_for_status()

            print(Fore.GREEN + "User logged in successfully!" + Style.RESET_ALL)
            os.system("clear")
            return True
        except ConnectionError:
            print(
                Fore.RED
                + "Connection error. Please check your internet connection."
                + Style.RESET_ALL
            )
        except Timeout:
            print(Fore.YELLOW + "Server timeout. Try again later." + Style.RESET_ALL)
        except HTTPError as e:
            if response.status_code == 400:
                print(
                    Fore.YELLOW
                    + "Invalid username or password. Please try again."
                    + Style.RESET_ALL
                )
            elif response.status_code == 401:
                print(
                    Fore.YELLOW
                    + "Unauthorized: Incorrect credentials."
                    + Style.RESET_ALL
                )
            elif response.status_code == 403:
                print(
                    Fore.YELLOW
                    + "Account disabled. Contact the administrator."
                    + Style.RESET_ALL
                )
            else:
                print(Fore.RED + f"Login error: {e}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Unexpected error during login: {e}" + Style.RESET_ALL)

        print(Fore.YELLOW + "Please try again.\n" + Style.RESET_ALL)
