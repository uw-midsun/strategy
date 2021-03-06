# Dynamics

A directory for all the car's dynamics modelling and data

## In this directory

+ `tests` directory
+ `CdACrrCalculator.py`: Extract aero drag and rolling resistance coefficients
+ `parserolldowndata.py`: Method to produce cleaned dataframe from CSV rolldown
+ `car_model.py`: Class to model car object, and using free-body diagram physics to determine energy needed for the car parameters and route

### `motor_efficiency` module

+ `motor_efficiency.py`: Class to generate and graph motor efficiency curves based on test data
+ `HIData.csv`: Test data CSV for high coil, see [mechanical Confluence](https://uwmidsun.atlassian.net/wiki/spaces/MECH/pages/1628012551/Interpreting+the+Graphs+From+Nomura)
+ `LOData.csv`: Test data CSV for low coil, see [mechanical Confluence](https://uwmidsun.atlassian.net/wiki/spaces/MECH/pages/1628012551/Interpreting+the+Graphs+From+Nomura)

### `rolldowndata` module

+ `canlog`: Directory of canlog data CSVs
+ `rolldown`: Scripts for cleaning and processing rolldown CSV data
+ `test.csv`: Sample rolldown CSV
