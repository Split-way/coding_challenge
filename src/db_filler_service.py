import sqlite3

from pandas import DataFrame

from data_preparation.demands_data_loader import DemandsLoaderService
from data_preparation.forecasts_data_loader import ForecstsLoaderService


class DBFillerService:
    def _get_formatted_demands(self) -> DataFrame:
        service = DemandsLoaderService()
        return service.get_formatted_demands_df()

    def _get_formatted_forecasts(self, path: str) -> DataFrame:
        service = ForecstsLoaderService()
        return service.get_formatted_forecasts_df(path)

    def _fill_database_with_dataframe(
        self, collection_name: str, dataframe: DataFrame
    ) -> None:
        with sqlite3.connect("energy_predictions") as connection:
            dataframe.to_sql(
                name=collection_name,
                con=connection,
                index=False,
                if_exists="replace",
            )

    def fill_database_with_forecasts(self, path: str) -> None:
        self._fill_database_with_dataframe(
            "forecasts", self._get_formatted_forecasts(path)
        )

    def fill_database_with_demands(self) -> None:
        self._fill_database_with_dataframe(
            "energy_demands", self._get_formatted_demands()
        )
