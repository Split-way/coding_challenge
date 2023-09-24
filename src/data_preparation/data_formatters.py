from datetime import datetime

import pandas as pd
from pandas import DataFrame


class DemandsFormatter:
    def _fix_hour_notation(self, date_str: str) -> str:
        if " 24" in date_str:
            date_part, hour_part = date_str.split(" ")
            date_dt = pd.to_datetime(
                date_part, format="%m/%d/%Y"
            ) + pd.Timedelta(days=1)
            return date_dt.strftime("%m/%d/%Y") + " 00"
        return date_str

    # migrating from 1-24 time format to ISO 8601 format because it's the format of datetime objects in Python
    def _standartize_datetime(self, df: DataFrame) -> None:
        df["Date (HE)"] = df["Date (HE)"].apply(self._fix_hour_notation)
        df["Date (HE)"] = pd.to_datetime(df["Date (HE)"], format="%m/%d/%Y %H")
        df["Date (HE)"] = df["Date (HE)"] - pd.Timedelta(hours=1)
        df["Date (HE)"] = df["Date (HE)"].dt.strftime("%Y-%m-%dT%H:%M:%S")
        df["Date (HE)"] = pd.to_datetime(
            df["Date (HE)"], format="%Y-%m-%dT%H:%M:%S"
        )

    def _rename_analyzed_columns(self, demands_df: DataFrame) -> None:
        demands_df.rename(columns={"Date (HE)": "datetime"}, inplace=True)
        demands_df.rename(
            columns={"Forecast Pool Price": "forecast_pool_price"}, inplace=True
        )
        demands_df.rename(
            columns={"Actual Posted Pool Price": "actual_posted_pool_price"},
            inplace=True,
        )
        demands_df.rename(
            columns={"Forecast AIL": "forecast_AIL"}, inplace=True
        )
        demands_df.rename(columns={"Actual AIL": "actual_AIL"}, inplace=True)
        demands_df.rename(
            columns={
                "Forecast AIL & Actual AIL Difference": "AIL_prediction_difference"
            },
            inplace=True,
        )

    def format_demands_df(self, demands_df: DataFrame):
        self._standartize_datetime(demands_df)
        self._rename_analyzed_columns(demands_df)
        demands_df.dropna()
        return demands_df


class ForecastsFormatter:
    # Columns are renamed because spaces cause errors in SQL query,
    # program will only query DB on these columns for simplicity
    def _rename_analyzed_columns(self, forecasts_df: DataFrame) -> None:
        forecasts_df.rename(columns={"Datetime": "datetime"}, inplace=True)
        forecasts_df.rename(
            columns={"Cloud Cover": "cloud_cover"}, inplace=True
        )
        forecasts_df.rename(
            columns={"Solar Radiation": "solar_radiation"}, inplace=True
        )

    def _string_datetime_to_object_datetime(
        self, forecasts_df: DataFrame
    ) -> None:
        forecasts_df["datetime"] = pd.to_datetime(
            forecasts_df["datetime"], format="%Y-%m-%dT%H:%M:%S"
        )

    def format_forecasts_df(self, forecasts_df: DataFrame) -> DataFrame:
        self._rename_analyzed_columns(forecasts_df)
        self._string_datetime_to_object_datetime(forecasts_df)
        return forecasts_df


class DateToStringsFormater:
    def format_datetime_object_to_strings(self, date: datetime) -> tuple[str]:
        year, month, day = date.year, date.month, date.day
        return self._format_date_component(year, month, day)

    def _format_date_component(self, year, month, day) -> tuple[str, str, str]:
        return str(month).zfill(2), str(day).zfill(2), str(year).zfill(4)
