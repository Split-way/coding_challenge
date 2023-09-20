import argparse
from pathlib import Path


class CommandLineArgumentsRequests:
    def ask_path_to_csvs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--forecasts_folder",
            required=True,
            help="Path to the folder containing forecast CSVs",
        )
        args = parser.parse_args()
        forecast_folder_path = Path(args.forecasts_folder)
        return forecast_folder_path
