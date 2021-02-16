# This will be a class that holds all the information for solar energy
# Specifically the energy coming into the solar panels
from math import cos, sin, pi, acos, tan, asin
from numpy import linspace
from sympy import *


def to_rad(angle):
    rad = angle * 2 * pi / 360
    return rad


def integrate(x, y):
    # Given an X and Y data set, numerically integrate
    integral = 0
    for i in range(len(x) - 1):
        integral += (x[i + 1] - x[i]) * (y[i + 1] + y[i]) / 2
    return integral


class SolarDay:

    def __init__(self, day, latitude, longitude, timezone, cloudiness, module_angle,
                 cell_angles, cell_lengths, cell_widths):
        # Integer as the number of days since the start of the year (0 indexed)
        self.day = day
        self.lat = latitude
        self.long = longitude
        # Cloudiness is the percentage of solar insolation
        # Not being blocked by clouds (i.e. between 0 and 1)
        self.cloud = cloudiness
        self.points = []
        # Given as an integer of the difference between us and UTC (Greenwich time)
        self.time = timezone
        # the module angle is the panel angle wrt the horizontal plane.
        # 0 degrees/rad faces North (front of car)
        self.mod_angle = module_angle
        # Cell info (parallel lists)
        self.C_angles = cell_angles  # Radians
        self.C_lengths = cell_lengths
        self.C_widths = cell_widths

    def declination_angle(self):
        """
        :returns: Declination angle in degree's
        Declination angle is the angle the sun sits in the sky at noon
        """
        d = -23.45 * cos(to_rad(360 / 365) * (self.day + 10))
        return d

    def time_correction(self):
        # Measurement of the difference in angle between us and UTC
        # LSTM = Local standard time meridian (in degrees) runs through the center of each time zone
        LSTM = 15 * self.time
        B = 360 / 365 * self.day * -81
        # Eot = the time difference between apparent solar time and mean time
        EoT = 9.87 * sin(2 * B) - 7.53 * cos(B) - 1.5 * sin(B)
        TC = 4 * (self.long - LSTM) + EoT
        return TC

    def sunrise(self):
        """
        :returns: time of sunset (24 hour time) using the hour angle and the sunrise equation
        """
        sunrise = (12 - (1 / to_rad(15))
                   * acos(-1 * tan(to_rad(self.declination_angle()))
                          * tan(to_rad(self.lat))) - self.time_correction() / 60)
        return sunrise

    def sunset(self):
        """
        :returns: time of sunset (24 hour time) using the hour angle and the sunset equation
        """
        sunset = (12 + (1 / to_rad(15))
                  * acos(-1 * tan(to_rad(self.declination_angle()))
                         * tan(to_rad(self.lat))) - self.time_correction() / 60)
        return sunset

    def day_length(self):
        return self.sunset() - self.sunrise()

    def solar_insolation(self, HRA):
        # gives value in kW/m^2
        ID = 1.353 * 0.7 ** (self.AM(HRA) ** 0.678)  # Incident radiation
        elevation = to_rad(90 - self.lat + self.declination_angle())
        IM = ID * sin(to_rad(self.mod_angle) + elevation)
        return IM

    # AM is the airmass, which is a factor that allows us to take into account
    # the effect of the angle of the sun in the sky and the time of day
    def AM(self, HRA):
        elevation = (asin(sin(to_rad(self.declination_angle()))
                          * sin(to_rad(self.lat))
                          + cos(to_rad(self.declination_angle()))
                          * cos(to_rad(self.lat)) * cos(HRA)))
        azimuth = (acos(sin(to_rad(self.declination_angle()))
                        * cos(to_rad(self.lat))
                        - cos(to_rad(self.declination_angle()))
                        * sin(to_rad(self.lat)) * cos(HRA)) / cos(elevation))
        if HRA > 0:
            azimuth = 2 * pi - azimuth
        zenith = (pi / 2) - elevation
        AM = 1 / cos(zenith)
        return AM

    # HRA is the solar time at the car location
    def time_to_HRA(self, time):
        LST = time + self.time_correction() / 60
        HRA = to_rad(15) * (LST - 12)
        return HRA

    def energy_received(self):
        points = linspace(self.sunrise(),
                          self.sunset(), 1000, endpoint=False).tolist()
        energy = []
        for i in range(len(points)):
            energy.append(self.solar_insolation(self.time_to_HRA(points[i])))
        self.total_energy = integrate(points, energy) * self.cloud
        return (energy, points)

    def suns_vector(self, HRA):
        """
        :param HRA: Hour angle
        :returns: unit vector from origin to sun
        """
        elevation = (asin(sin(to_rad(self.declination_angle()))
                          * sin(to_rad(self.lat))
                          + cos(to_rad(self.declination_angle()))
                          * cos(to_rad(self.lat)) * cos(HRA)))
        azimuth = (acos(sin(to_rad(self.declination_angle()))
                        * cos(to_rad(self.lat))
                        - cos(to_rad(self.declination_angle()))
                        * sin(to_rad(self.lat)) * cos(HRA)) / cos(elevation))
        if HRA > 0:
            azimuth = 2 * pi - azimuth
        zenith = (pi / 2) - elevation

        #--------------------------------------------------------------- change as with mod angle
        # Suns unit vector
        x = sin(zenith) * cos(azimuth)
        y = sin(zenith) * sin(azimuth)
        z = cos(zenith)
        vector = (x, y, z)
        return vector

    def projected_solar_area(self, sun_vector):

        x, y, z = sun_vector
        sun_plane = Plane(Point3D(x * 1000, y * 1000, z * 1000), normal_vector=sun_vector)
        # Loop through each solar cell

        for i in range(len(self.C_angles)):
            print("yeilo")
            # initialize the four corners of the solar cell (corner at origin)
            point_1 = Point3D(0, 0, 0)
            point_2 = Point3D(0, self.C_widths[i], 0)
            point_3 = Point3D(self.C_lengths[i] * cos(self.C_angles[i]), self.C_widths[i], self.C_lengths[i] * sin(self.C_angles[i]))
            point_4 = Point3D(self.C_lengths[i] * cos(self.C_angles[i]), 0, self.C_lengths[i] * sin(self.C_angles[i]))
            print("holla")
            point_1_proj = sun_plane.projection(point_1)
            print("yakyak")
            point_2_proj = sun_plane.projection(point_2)
            point_3_proj = sun_plane.projection(point_3)
            point_4_proj = sun_plane.projection(point_4)
            print("yello")

if __name__ == "__main__":
    day = SolarDay(0, 0, 0, 0, 0, 0, [0], [10], [10])

    day.projected_solar_area(day.suns_vector(day.time_to_HRA(12)))