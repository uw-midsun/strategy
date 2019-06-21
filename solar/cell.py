from solar import SolarDay

class SolarCell:
    def __init__(self, area, temperature):
        self.area = area
        # efficiency of solar energy conversion to electrical energy
        self.efficiency = .237 
        # temp_coeff is the percentage decrease
        # in the cells' efficiency for every degree above 25C
        self.temp_coefficient = -.0029
        # the internal temperature of the cells/array
        self.temperature = temperature
        
    def total_efficiency_decrease(self):
        if self.temperature > 25:
            efficiency = self.efficiency - self.temp_coefficient * (self.temperature - 25)
            return efficiency
        return self.efficiency
    
    def energy_converted(self)
        return SolarDay.energy_received() * total_efficiency_decrease()