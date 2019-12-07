class AuxSystem:
    def __init__(self, initial_current, initial_voltage):
        """
        Initialize Auxiliary System object
        """
        self.time = 0
        self.time_old = 0

        if initial_current < 0:
            initial_current = 0

        if initial_voltage < 0:
            initial_voltage = 0

        self.current_old = initial_current
        self.voltage_old = initial_voltage
        self.current = initial_current  # current (A) through aux system
        self.voltage = initial_voltage  # potential difference of aux system

    def energy_consumed(self, time_new, new_current, new_voltage):
        """
        Calculate energy consumed by Auxiliary system.
        Power (W) = Current (A) x Voltage (V)
        Energy (J) = Power (W) x Time (s)
        Energy = Current (A) x Voltage (V) x Time (s)
        """
        # two timepoints to determine energy loss of system over period
        self.time_old = self.time

        # negative time is not allowed
        if time_new < 0:
            self.time = self.time
        else:
            self.time = time_new

        # current divided into two for an average between the two timepoints
        self.current_old = self.current

        # negative current is incorrect value, return previous value instead
        if new_current < 0:
            self.current = self.current
        else:
            self.current = new_current

        # voltage divided into two for an average between the two timepoints
        self.voltage_old = self.voltage

        # negative voltage is considered incorrect, return old value
        if new_voltage < 0:
            self.voltage = self.voltage
        else:
            self.voltage = new_voltage

        energy_consumed = (((self.current + self.current_old) / 2)
                           * ((self.voltage + self.voltage_old) / 2)
                           * (self.time - self.time_old))
        return energy_consumed
