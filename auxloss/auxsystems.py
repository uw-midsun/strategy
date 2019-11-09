class AuxSystem:
    def __init__(self, initial_current, initial_voltage):
        """
        Initialize Auxiliary System object
        """
        self.time = 0
        self.time_old = 0
        self.current_old = initial_current
        self.voltage_old = initial_voltage
        self.current = initial_current # amount of current in amperes flowing through auxiliary system
        self.voltage = initial_voltage # potential electrical difference of auxiliary system
    
    def energy_consumed(self, time_new, new_current, new_voltage):
        """
        Calculate energy consumed by Auxiliary system.
        Power (W) = Current (A) x Voltage (V)
        Energy (J) = Power (W) x Time (s)
        Energy = Current (A) x Voltage (V) x Time (s)
        """
        # two timepoints to determine energy loss of system over period
        self.time_old = self.time
        self.time = time_new 

        # current will be divided into two for an average between the two timepoints
        # could be several points of time period in an array?
        self.current_old = self.current
        self.current = new_current

        # voltage will be divided into two for an average between the two timepoints
        # could be several points of time  period in an array?
        self.voltage_old = self.voltage
        self.voltage = new_voltage
        
        energy_consumed = ((self.current + self.current_old)/2) * ((self.voltage + self.voltage_old)/2) * (self.time - self.time_old)
        return energy_consumed

