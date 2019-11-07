class AuxSystem:
    def __init__(self, current, voltage, time):
        """
        Initialize Auxiliary System object
        """
        self.current = current # amount of current in amperes flowing through auxiliary system
        self.voltage = voltage # potential electrical difference of auxiliary system
        self.time = time # time in seconds
    
    def energy_consumed(self):
        """
        Calculate energy consumed by Auxiliary system.
        Power (W) = Current (A) x Voltage (V)
        Energy (J) = Power (W) x Time (s)
        Energy = Current (A) x Voltage (V) x Time (s)
        """
        energy_consumed = self.current * self.voltage * self.time
        return energy_consumed

