To run this script:
1. if case you don't want to use CSV files in the repository, download CSV files from the link below and unpack them into one folder;
2. create a virtual environment on the same level as 'README.MD' and download requirements;
3. if not done yet, install chrome web driver, and make sure OS can see it through the 'PATH' environment variable (on Linux and MacOS, it means to put it in '/usr/local/bin' and make it executable with 'sudo chmod +x /usr/local/bin/drivername');
4. go to the 'src' directory of this repository and run 'main.py' from there with one argument - absolute path to the folder with the CSV files with forecasts (included in the repository; check the 'forecasts' folder).


Example bash commands:
'''bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python main.py --forecasts_folder /home/user/data/forecasts
'''

After you run the script, it fills the SQLite database with the data from CSVs and the website, and the model trains on data from SQLite. As an output, you will get a mean squared error; it will be much bigger than normal since this model had almost no feature engineering.

Link to CSVs - https://drive.google.com/file/d/1asPqcC5xIMtHJo8ZrownS2N05N1376hv/view?usp=sharing
Link to website - http://ets.aeso.ca/ets_web/docroot/Market/Reports/HistoricalReportsStart.html