import sqlite3
from typing import List

import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


class RandomForestRegressorService:
    def _train(
        self, x: List[int], y: List[int], x_test: List[int], y_test: List[int]
    ) -> int:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(x, y)

        y_pred = model.predict(x_test)
        mse = mean_squared_error(y_test, y_pred)

        return mse

    def _prepare_data(self, df: DataFrame) -> tuple[list[int]]:
        x = df[["cloud_cover", "solar_radiation"]]
        y = df["actual_posted_pool_price"]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )
        return x_train, y_train, x_test, y_test

    def _get_data_from_database(self) -> DataFrame:
        with sqlite3.connect("energy_predictions") as connection:
            query = """
            SELECT e.actual_posted_pool_price, f.cloud_cover, f.solar_radiation
            FROM energy_demands e JOIN forecasts f ON e.datetime = f.datetime
            WHERE e.actual_posted_pool_price IS NOT NULL AND 
                  f.cloud_cover IS NOT NULL AND 
                  f.solar_radiation IS NOT NULL
            ORDER BY e.datetime
            """
            return pd.read_sql_query(query, connection)

    def run(self) -> int:
        energy_predictions_df = self._get_data_from_database()
        x_train, y_train, x_test, y_test = self._prepare_data(
            energy_predictions_df
        )
        return self._train(x_train, y_train, x_test, y_test)
