import csv

class AuxPowerConsumption:
    def __init__(self, power_budget):
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
        current_power = 0
        for component in components_used["components"]:
            if type(component) is tuple:
                # assumes that percentage is provided (%, not decimal)
                current_power += float(self.power_consumptions[component[0]]["Max Power (W)"]) * component[1] * 0.01
            else:
                current_power += float(self.power_consumptions[component]["Typical Power (W)"])

        return current_power

    def calculate_energy_usage(self, components, time_in_seconds):
        return self.calculate_instantaneous_power(components) * time_in_seconds