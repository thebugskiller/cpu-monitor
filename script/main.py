import signal
import sys
import requests
from monitor import CPUMonitor
from util import register_user, login_user, input_manager
from colorama import Fore, Style


def runner(session) -> None:
    name = input_manager("Please give a name to this scan: ")
    interval = input_manager("Please enter interval (s) to save data: ")
    threshold = input_manager("Please enter a threshold value: ")

    try:
        interval = int(interval)
        threshold = int(threshold)
    except Exception as e:
        print("Interval and threshold can only be numeric value, please enter again.")

    if interval < 5 or threshold < 0 or threshold > 100:
        print(
            "Invalid parameters: interval must be > 5 and threshold must be between 0 and 100."
        )
        runner(session=session)

    print(f"Starting CPU monitoring (interval: {interval}s, threshold: {threshold}%)")
    print("Press Ctrl+C to stop...\n")
    monitor = CPUMonitor(name, interval, threshold, session)
    monitor.start()


def handle_input(option_range):
    if not isinstance(option_range, int) or option_range <= 0:
        raise ValueError("Option range must be a positive integer.")
    signal.signal(signal.SIGINT, signal.default_int_handler)
    while True:
        try:
            option = input_manager("Enter your option: ").strip()

            if not option:
                print(
                    Fore.YELLOW
                    + "Input cannot be empty. Please enter a valid option."
                    + Style.RESET_ALL
                )
                continue

            option = int(option)

            if 1 <= option <= option_range:
                return option
            else:
                print(
                    Fore.YELLOW
                    + f"Please enter a valid option between 1 and {option_range}."
                    + Style.RESET_ALL
                )
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a numeric value.")
        except KeyboardInterrupt:
            print(Fore.RED + "\nProcess interrupted by user. Exiting...")
            sys.exit(1)
        except Exception as e:
            print(Fore.RED + f"Unexpected error: {e}")

def main():
    logged_in = False
    session = requests.Session()
    while True:
        if not logged_in:
            print(
                "## Welcome to CPU Monitor ##\nThis tool will monitor you CPU utilization and \
alert you if the utilization exceeds the given threshold.\n\n1) Register\n2) Login\n3) Quit\n\
Please select an option (e.g. 1): "
            )
            signal.signal(signal.SIGINT, signal.default_int_handler)
            user_option = handle_input(option_range=3)

            if user_option == 1:
                register_user(session=session)
            if user_option == 2:
                logged_in = login_user(session=session)
            if user_option == 3:
                print("\n# Come Back Soon. #")
                break
        else:
            print(
                "## Welcome to CPU Monitor ##\nThis tool will monitor you CPU utilization and \
alert you if the utilization exceeds the given threshold.\n\n1) Scan CPU\n2) Quit\nPlease select \
an option (e.g. 1): "
            )
            signal.signal(signal.SIGINT, signal.default_int_handler)
            user_option = handle_input(option_range=2)

            if user_option == 1:
                runner(session=session)
            if user_option == 2:
                print("\n# Come Back Soon. #")
                break



if __name__ == "__main__":
    main()
