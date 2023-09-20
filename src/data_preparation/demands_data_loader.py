from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

from data_preparation.data_formatters import (DateToStringsFormater,
                                              DemandsFormatter)


class DemandsLoaderService:
    def _take_data_for_time_period(
        self,
        beginning_month: str,
        beginning_day: str,
        beginning_year: str,
        end_month: str,
        end_day: str,
        end_year: str,
        driver: WebDriver,
        columns: list[str],
    ) -> list[list[str]]:
        frame = driver.find_element(By.NAME, "report_nav")
        driver.switch_to.frame(frame)

        self._configure_dates_in_dropdowns(
            driver,
            beginning_month,
            beginning_day,
            beginning_year,
            end_month,
            end_day,
            end_year,
        )

        ok_button = driver.find_element(By.XPATH, "//a//img[@alt='OK']/..")
        ok_button.click()

        driver.switch_to.parent_frame()

        frame = driver.find_element(By.NAME, "report_content")
        driver.switch_to.frame(frame)

        table = driver.find_element(
            By.XPATH, "//table[@border='1']"
        ).get_attribute("outerHTML")
        soup = BeautifulSoup(table, "html.parser")
        rows = soup.find_all("tr")

        processed_rows_list = []

        self._iterate_and_save_rows_to_list(rows, processed_rows_list, columns)

        driver.switch_to.parent_frame()

        return processed_rows_list

    def _iterate_and_save_rows_to_list(
        self, rows, destination_collection: list, columns: list[str]
    ) -> None:
        for row in rows:
            elements = row.find_all("td")
            row_data = [element.text for element in elements]
            if len(row_data) == len(columns):
                destination_collection.append(row_data)

    def _configure_dates_in_dropdowns(
        self,
        driver: WebDriver,
        beginning_month: str,
        beginning_day: str,
        beginning_year: str,
        end_month: str,
        end_day: str,
        end_year: str,
    ) -> None:
        dropdown = Select(driver.find_element(By.NAME, "SelectReport"))
        dropdown.select_by_visible_text("--- Actual Forecast")

        dropdown = Select(driver.find_element(By.NAME, "BeginMonth"))
        dropdown.select_by_visible_text(beginning_month)

        dropdown = Select(driver.find_element(By.NAME, "BeginDay"))
        dropdown.select_by_visible_text(beginning_day)

        dropdown = Select(driver.find_element(By.NAME, "BeginYear"))
        dropdown.select_by_visible_text(beginning_year)

        dropdown = Select(driver.find_element(By.NAME, "EndMonth"))
        dropdown.select_by_visible_text(end_month)

        dropdown = Select(driver.find_element(By.NAME, "EndDay"))
        dropdown.select_by_visible_text(end_day)

        dropdown = Select(driver.find_element(By.NAME, "EndYear"))
        dropdown.select_by_visible_text(end_year)

    def _get_demands_df(self) -> pd.DataFrame:
        columns = [
            "Date (HE)",
            "Forecast Pool Price",
            "Actual Posted Pool Price",
            "Forecast AIL",
            "Actual AIL",
            "Forecast AIL & Actual AIL Difference",
        ]
        driver = webdriver.Chrome()
        link = "http://ets.aeso.ca/ets_web/docroot/Market/Reports/HistoricalReportsStart.html"
        start_date = datetime(year=2022, month=1, day=1)
        end_date = datetime(year=2023, month=9, day=1)
        delta = timedelta(days=30)
        driver.get(link)
        demands_df = pd.DataFrame(columns=columns)
        service = DateToStringsFormater()
        while start_date <= end_date:
            temp_end_date = start_date + delta
            if temp_end_date > end_date:
                temp_end_date = end_date

            start_date_strings = service.format_datetime_object_to_strings(
                start_date
            )
            end_date_strings = service.format_datetime_object_to_strings(
                temp_end_date
            )
            new_rows = self._take_data_for_time_period(
                *start_date_strings,
                *end_date_strings,
                driver=driver,
                columns=columns
            )
            new_df = pd.DataFrame(new_rows, columns=columns)
            demands_df = demands_df._append(new_df, ignore_index=True)

            start_date += delta + timedelta(days=1)

        driver.quit()

        return demands_df

    def get_formatted_demands_df(self) -> pd.DataFrame:
        service = DemandsFormatter()
        return service.format_demands_df(self._get_demands_df())
