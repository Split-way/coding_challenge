from ask_configurations import CommandLineArgumentsRequests
from db_filler_service import DBFillerService
from model_trainer_service import RandomForestRegressorService

if __name__ == "__main__":
    forecast_folder_path = CommandLineArgumentsRequests().ask_path_to_csvs()
    service = DBFillerService()
    service.fill_database_with_forecasts(forecast_folder_path)
    service.fill_database_with_demands()

    service = RandomForestRegressorService()
    mean_squared_err = service.run()
    print(mean_squared_err)
