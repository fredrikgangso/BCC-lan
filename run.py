import datetime
import os
import csv
import sys

import speedtest

class TestRouter:
    def __init__(self, router: str = ""):
        print("Running speedtest...")
        self.todaysDate = datetime.date.today()
        self.todaysTime = datetime.datetime.now().strftime("%H%M%S")
        self.speedtest = speedtest.Speedtest()

        router = sys.argv[1] if len(sys.argv) > 1 else router
        
        # Select nearby servers
        self.speedtest.get_servers()
        self.speedtest.get_best_server()

        # Run multiple tests for better accuracy
        num_tests = 3  # You can adjust this value
        results = [self.run_speed_test() for _ in range(num_tests)]

        self.find_or_create_log_location()
        self.create_log_file(router, results)
        print("Test complete")

    def run_speed_test(self):
        download_speed = self.speedtest.download() / 1_000_000  # Convert to Mbps
        upload_speed = self.speedtest.upload() / 1_000_000  # Convert to Mbps
        ping = self.speedtest.results.ping

        return {
            "Download": download_speed,
            "Upload": upload_speed,
            "Ping": ping
        }

    def find_or_create_log_location(self):
        if os.path.exists(str(self.todaysDate)):
            print("Folder exists: not creating a new folder")
        else:
            os.mkdir(str(self.todaysDate))
            print("Folder does not exist: creating a new folder")

    def create_log_file(self, router: str, results: list):
        if router:
            routerFile = router + "_"

        csv_file = f"{self.todaysDate}/{routerFile}{self.todaysTime}.csv"
        with open(csv_file, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Test", "Router", "Download", "Upload", "Ping"])
            for idx, test in enumerate(results, start=1):
                csvwriter.writerow([f"{idx}", f"{router}", f"{test['Download']:.2f} Mbps", f"{test['Upload']:.2f} Mbps", f"{test['Ping']:.2f} ms"])

if __name__ == "__main__":
    TestRouter()
