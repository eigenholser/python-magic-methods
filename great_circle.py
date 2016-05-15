from math import pi, sin, asin, cos, sqrt


JFK = ("40.641108", "-73.778246")
LAX = ("33.941544", "-118.408755")
SLC = ("40.788139", "-111.980268")


class Point(object):
    """
    Defines a point on the earth's surface using latitude and logitude.
    """
    LATITUDE = 0
    LONGITUDE = 1

    def __init__(self, p):
        """
        Initialize instance.
        """
        self.latitude = self.to_radians(float(p[self.LATITUDE]))
        self.longitude = self.to_radians(float(p[self.LONGITUDE]))

    def to_radians(self, deg):
        """
        Convert degrees to radians.
        """
        rad = deg * pi / 180
        return rad

    def coordinates(self):
        latitude = (self.latitude / pi) * 180
        latitude_deg, latitude_min = str(latitude).split(".")
        latitude_deg = int(latitude_deg)
        latitude_min = round(float("0.{}".format(latitude_min)) * 60)
        if latitude > 0:
            latitude_dir = 'N'
        else:
            latitude_dir = 'S'

        longitude = (self.longitude / pi) * 180
        longitude_deg, longitude_min = str(longitude).split(".")
        longitude_deg = int(longitude_deg)
        longitude_min = round(float("0.{}".format(longitude_min)) * 60)
        if longitude > 0:
            longitude_dir = 'E'
        else:
            longitude_dir = 'W'

        latitude_str = "{deg}\u00B0 {min}\u2032 {dir}".format(
                deg=abs(latitude_deg), min=latitude_min, dir=latitude_dir)
        longitude_str = "{deg}\u00B0 {min}\u2032 {dir}".format(
                deg=abs(longitude_deg), min=longitude_min, dir=longitude_dir)

        return "{latitude}, {longitude}".format(
                latitude=latitude_str, longitude=longitude_str)

    def calculate_distance(self, other):
        """
        Demo how it might work without using magic methods.
        """
        distance = 2.0 * asin(
            sqrt((sin((self.latitude-other.latitude)) / 2.0) ** 2 +
                cos(self.latitude) * cos(other.latitude) *
                (sin((self.longitude-other.longitude) / 2.0)) ** 2))
        return "{0:.2f}".format(distance* 180 * 60 / pi)


class PointMagicMixin(object):
    """
    Adds magic methods to base class.
    """

    def __del__(self):
        """
        Destructor called when object destroyed by Python GC.
        """
        print("__del__() method called on {:.2f}.".format(self))

    def __eq__(self, other):
        """
        Implement behavior for Python "==" operator.
        """
        return ((self.latitude == other.latitude) and
                (self.longitude == other.longitude))

    def __format__(self, formatstr):
        """
        Implement behavior for use in format().
        """
        # If no formatstr, just return the standard coordinates.
        if not formatstr:
            return self.coordinates()

        # If floating point format, return coordinates in radians formatted
        # to specified precision.
        if formatstr.endswith('f') and formatstr.startswith('.'):
            precision = formatstr[1]
            return self._represent_output(precision)

        # Otherwise, just return radians with all decimals.
        return self._represent_output()

    def __repr__(self):
        """
        Implement behavior for Python repr() command.
        """
        return self._represent_output(5)

    def __str__(self):
        """
        Instance unicode string representation.
        """
        return self.coordinates()

    def __sub__(self, other):
        """
        Subtract two points. Return Distance instance.
        """
        return MagicDistance(self, other)

    def _represent_output(self, precision=None):
        """
        Return string representation of point to specified precision. Intended
        to be used in support of magic methods __repr__() and __format__().
        """
        formatstr = "Point({{latitude:{}f}}, {{longitude:{}f}})"
        if not precision:
            formatstr = formatstr.format('', '')
        else:
            float_format = ".{}".format(precision)
            formatstr = formatstr.format(float_format, float_format)
        return formatstr.format(
                latitude=self.latitude, longitude=self.longitude)


class MagicPoint(Point, PointMagicMixin):
    pass


class Distance(object):
    """
    Represents a distance between two points as defined by respective latitude
    and longitude.
    """

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.distance = self.calculate_distance(p1, p2)

    def calculate_distance(self, p1, p2):
        distance = 2.0 * asin(
            sqrt((sin((p1.latitude-p2.latitude)) / 2.0) ** 2 +
                cos(p1.latitude) * cos(p2.latitude) *
                (sin((p1.longitude-p2.longitude) / 2.0)) ** 2))
        return distance * 180 * 60 / pi

class DistanceMagicMixin(object):

    def __call__(self, p1, p2):
        """
        This method called when object instance called like a function.
        """
        distance = self.calculate_distance(p1, p2)
        return "{0:.2f}".format(distance)

    def __del__(self):
        """
        Destructor called when object destroyed by Python GC.
        """
        print("__del__() method called on {}.".format(self))

    def __ge__(self, other):
        """
        Implement behavior for Python ">=" operator.
        """
        return self.distance >= other.distance

    def __gt__(self, other):
        """
        Implement behavior for Python ">" operator.
        """
        return self.distance > other.distance

    def __le__(self, other):
        """
        Implement behavior for Python "<=" operator.
        """
        return self.distance <= other.distance

    def __lt__(self, other):
        """
        Implement behavior for Python "<" operator.
        """
        return self.distance < other.distance

    def __repr__(self):
        """
        Implement behavior for Python repr() command.
        """
        return "MagicDistance(({}) ==> ({}))".format(self.p1, self.p2)

    def __str__(self):
        """
        String representation for class instance. Python calls this method
        when:

            print(distance_obj)
        """
        return "{0:.2f}".format(self.distance)


class MagicDistance(Distance, DistanceMagicMixin):
    pass

