import csv

class AuxPowerConsumption:
    def __init__(self, power_budget):
        """
        Initializes AuxPowerConsumption object based on given power budget.

        Reads and stores information about typical and max power usage, etc. of the various components into a dictionary called  `power_consumptions`. Keys are component names, values are dictionaries with column names as values. Any empty keys are discarded.

        :param power_budget: Path to power budget CSV file. 
            Headers expected: "Component", "Max Power (W)", "Typical Power (W)"
        """

        self.power_consumptions = {}

        with open(power_budget, "r") as file:            
            # this is expecting file to start with Front Power Distribution Board
            # ignores this line so expected headers are picked up
            next(file)

            csv_file = csv.DictReader(file)

            for row in csv_file:
                # Front Power Distribution Board included for completion; none of these lines have component data
                if row["Component"] == "Front Power Distribution Board" or row["Component"] == "Rear Power Distribution Board" or row["Component"] == "Component" or not row["Component"]:
                    continue
                
                # assumes AUX Current Draw and AUX Current Protection, etc. is listed last and not relevant
                if row["Component"] == "AUX Current Draw and AUX Current Protection":
                    break
                
                self.power_consumptions[row["Component"]] = {k:v for k,v in row.items()}

    def calculate_instantaneous_power(self, components_used):
        """
        Calculates instantaneous power from auxiliary losses in power budget

        :param components_used: dictionary with a single key, "components", and a list of  components to consider. This list includes strings and/or (string, float) tuples, where string is component name and optional float specifies percentage of typical power used (30% -> 30, not decimal). If float not specified, assumes typical power. Any components not recognized are ignored.
            Example:
                {
                    "components": [("Horn", 100), ("Fan", 50), "Telemetry"]
                }

        :return: float, sum of power usage by each component
        """

        current_power = 0
        for component in components_used["components"]:
            if type(component) is tuple:
                if component[0] not in self.power_consumptions:
                    print("{} is not a recognized component.".format(component[0]))
                    continue

                # assumes that percentage is provided (%, not decimal)
                current_power += float(self.power_consumptions[component[0]]["Max Power (W)"]) * component[1] * 0.01
            else:
                if component not in self.power_consumptions:
                    print("{} is not a recognized component.".format(component))
                    continue

                current_power += float(self.power_consumptions[component]["Typical Power (W)"])

        return current_power

    def calculate_energy_usage(self, components, time_in_seconds):
        """
        Calculates energy usage from instantaneous auxiliary losses in power budget

        :param components: dictionary, see `calculate_instantaneous_power(self, components_used)`
        :param time_in_seconds: float, time (s) that power is used
        
        :return: float, energy = power * time
        """
        return self.calculate_instantaneous_power(components) * time_in_seconds
