import os
from pathlib import Path

import pandas as pd

from data_preparation.data_formatters import ForecastsFormatter


class ForecstsLoaderService:
    def _get_forecasts_df_from_csv(self, forecast_folder_path: str):
        forecast_folder_path = Path(forecast_folder_path)
        all_forecast_files_paths = [
            f for f in os.listdir(forecast_folder_path) if f.endswith(".csv")
        ]

        combined_forecast_df = pd.concat(
            [
                pd.read_csv(os.path.join(forecast_folder_path, f))
                for f in all_forecast_files_paths
            ],
            ignore_index=True,
        )

        return combined_forecast_df

    def get_formatted_forecasts_df(self, path: str):
        forecasts_df = self._get_forecasts_df_from_csv(path)
        service = ForecastsFormatter()
        service.format_forecasts_df(forecasts_df)
        return forecasts_df
