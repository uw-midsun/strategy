A directory for the car's model for all the auxiliary energy losses of the car, as well as data on the subject

## AuxPowerConsumption
AuxPowerConsumption class contains `__init__` and two methods, `calculate_instantaneous_power` and `calculate_energy_usage`. 

### `__init__(self, power_budget)`
+ Accepts a csv file (power budget).
+ Reads and stores information about typical and max power usage, etc. of the various components into a dictionary called  `power_consumptions`. Keys are component names, values are dictionaries with column names as values. Any empty keys are discarded.
+ Headers expected: "Component", "Max Power (W)", "Typical Power (W)"
+ Assumes Front and Rear Power infomration stored first. It skips past the first line (which is expected to contain title Front Power Distribution Board) to get the column headers from second line. Reads up until AUX Current Draw and AUX Current Protection title is reached.

### `calculate_instantaneous_power(self, components_used)`
+ Accepts a dictionary with a single key, "components", and a list of strings and tuples. 
+ Strings are component names. If not in tuple, assumes it is using typical power.
+ Tuples should contain component name and percentage of max. power used: eg. `("Fan", 30)`. Assumes that percentage is provided, not in decimal form. 
+ Returns sum of power usage by each component

### `calculate_energy_usage(self, components_used, time_in_seconds)`
+ Accepts a dictionary and time (s) that power is used. See calculate_instantaneous_power above for more information about dictionary.
+ Returns energy = power * time