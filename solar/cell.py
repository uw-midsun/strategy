# Class for a single Solar Cell
# Tracks efficiency of energy conversion from solar to electrical
from solar import SolarDay


class SolarCell:
    def __init__(self, area, temperature):
        # area of solar cell
        self.area = area

        # efficiency of solar energy conversion to electrical energy
        self.efficiency = .237

        # temp_coeff is the percentage decrease
        # in the cells' efficiency for every degree above 25C
        self.temp_coefficient = -.0029
        # efficiency and temp_coeff. values based off
        # manufacturer details
        # Check Confluence for more information

        # the internal temperature of the cells/array
        self.temperature = temperature

    def total_efficiency_decrease(self):
        # returns modified efficiency percentage if temperature is above 25
        # otherwise returns normal efficiency of cell
        if self.temperature > 25:
            efficiency = (self.efficiency - self.temp_coefficient
                          * (self.temperature - 25))
            return efficiency
        return self.efficiency

    def energy_converted(self):
        # returns product of solar insolation and efficiency
        return SolarDay.energy_received() * self.total_efficiency_decrease()
