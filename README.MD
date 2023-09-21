# Launching the project

1. In case you don't want to use CSV files in the repository, download CSV files from the link below and unpack them into one folder:
[Link to CSVs](https://drive.google.com/file/d/1asPqcC5xIMtHJo8ZrownS2N05N1376hv/view?usp=sharing)

2. If not done yet, install chrome web driver, and make sure OS can see it by default; put it in the folder that is included in the `PATH` environment variable: 

* On Linux and MacOS, it means to put it in `/usr/local/bin` and make it executable with 
```
sudo chmod +x /usr/local/bin/drivername
```
* On Windows they are already executable after download, just put it in forder that is included in `PATH`

3. Clone the repository and go to it's root directory:
```
git clone https://github.com/Split-way/coding_challenge.git
cd coding_challenge
```
4. Create a virtual environment on the same level as `readme.md`:
```
python3 -m venv venv
```
* Activate it; if you have Linux/macOS
```
source venv/bin/activate
```
* If you have Windows
```
source venv/Scripts/Activate
```

5. Upgrade pip and download requirements from `requirements.txt`:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Go to the `src` directory of this repository and run `main.py` from there with one argument - absolute path to the folder with the CSV files with forecasts, included in repository (or the one you downloaded manually).

```
cd src
python main.py --forecasts_folder /absolute/path/to/folder/with/csv
```

After you run the script, it fills the SQLite database with the data from CSVs and the website (link below), and the model trains on this data. As an output, you will get a mean squared error of model; it will be much bigger than normal since the model had almost no feature engineering.

* [Link to the website](http://ets.aeso.ca/ets_web/docroot/Market/Reports/HistoricalReportsStart.html)

## Author

Volodymyr Sovyk 
* [LinkedIn](https://www.linkedin.com/in/volodymyr-sovyk/)