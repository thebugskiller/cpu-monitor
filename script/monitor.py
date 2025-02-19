from datetime import datetime
import time
import signal
from typing import Optional
import threading
import psutil
from tabulate import tabulate
from service import create_test_run, create_cpu_log, get_cpu_log
from colorama import Fore, Style


class CPUMonitor:
    def __init__(self, name: str, interval: int, threshold: int, session) -> None:
        self.name = name
        self.interval = int(interval)
        self.default_interval = 5
        self.threshold = int(threshold)
        self.start_time: Optional[datetime] = None
        self.readings = []
        self.total_time_above: float = 0.0
        self.running: bool = False
        self.session = session
        self.test_run_id: str = self.create_task_run()
        self.start_event = threading.Event()

    def create_task_run(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = create_test_run(
            name=self.name, timestamp=timestamp, session=self.session
        )
        if response.status_code != 200:
            print("An error occurred!")
            self.handle_interrupt()

        return response.json()["test_run_id"]

    def handle_interrupt(self, sig, frame) -> None:
        self.running = False
        print("\nInterrupt received, stopping monitoring...")

    def default_interval_thread(self) -> None:
        self.start_event.wait()
        self.start_event.wait()

        while self.running:
            cpu_usage = psutil.cpu_percent(interval=self.default_interval)
            if not self.running:
                break
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[Default Interval - {timestamp}] CPU Usage: {cpu_usage}%")

            if cpu_usage > self.threshold:
                self.total_time_above += self.default_interval
                print(
                    Fore.YELLOW
                    + f"ALERT!! CPU usage has exceeded the threshold of {self.threshold}%"
                    + Style.RESET_ALL
                )

    def user_interval_thread(self) -> None:
        self.start_event.wait()
        while self.running:
            time.sleep(self.interval)
            if not self.running:
                break
            cpu_usage = psutil.cpu_percent(interval=0)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                create_cpu_log(self.test_run_id, cpu_usage, timestamp, self.session)
            except Exception as e:
                print(e)
                print("Couldn't save CPU log")
            print(
                f"[User Interval - {timestamp}] CPU Usage (measured at user interval): {cpu_usage}%"
            )

    def start(self) -> None:
        self.running = True
        self.start_time = datetime.now()

        signal.signal(signal.SIGINT, self.handle_interrupt)
        signal.signal(signal.SIGTERM, self.handle_interrupt)

        psutil.cpu_percent(interval=None)

        default_thread = threading.Thread(target=self.default_interval_thread)
        user_thread = threading.Thread(target=self.user_interval_thread)

        default_thread.start()
        user_thread.start()

        self.start_event.set()

        try:
            while self.running:
                time.sleep(2.0)
        except Exception as e:
            print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)
        finally:
            self.running = False
            default_thread.join()
            user_thread.join()
            self.show_report()

    def show_table(self, response):
        if response.status_code == 200:
            data = response.json()
            cpu_usage_data = data.get("cpu_usage", [])
            if cpu_usage_data:
                table_data = [
                    {
                        "S.No": idx + 1,
                        "Timestamp": entry["timestamp"],
                        "CPU %": entry["cpu_percent"],
                    }
                    for idx, entry in enumerate(cpu_usage_data)
                ]
                return tabulate(table_data, headers="keys", tablefmt="grid")
            else:
                return "No CPU usage data available."
        else:
            return (
                Fore.RED
                + f"Error: {response.status_code}, {response.text}"
                + Style.RESET_ALL
            )

    def show_report(self) -> None:
        if self.start_time is None:
            print("Monitoring never started.")
            return

        duration = (datetime.now() - self.start_time).total_seconds()
        print("\n=== Monitoring Report ===")
        print(f"Test Run ID: {self.test_run_id}")
        print(f"Test Run Name: {self.name}")
        print(f"Total runtime: {duration:.2f} seconds")
        print(f"Time above threshold: {self.total_time_above:.2f} seconds")
        response = get_cpu_log(self.test_run_id, self.session)
        table = self.show_table(response)
        print(table)
