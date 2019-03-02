import math


def valid_lat(lat) -> bool:
    """
    return true if the latitude value is valid
    :param lat: latitude to check
    :return: bool
    """
    return -90.0 <= lat <= 90.0


def valid_lon(lon) -> bool:
    """
    return true if the longitude value is valid
    :param lon: longitude value
    :return: bool
    """
    return -180.0 <= lon <= 180.0


class Point:

    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0) -> None:
        """
        A 3D point containing a latitude, longitude and altitude coordinate
        :param lat: latitude value
        :param lon: longitude value
        :param alt: altitude value
        """
        self.lat = 0.0
        self.lon = 0.0

        self.set_latitude(lat)
        self.set_longitude(lon)
        self.alt = alt

    def set_latitude(self, lat) -> None:
        """
        Set the latitude value if it is valid, if it is not valid use the previous value, if there
        was not one set, default to 0.0
        :param lat: latitude value
        :return: none
        """
        self.lat = lat if valid_lat(lat) else self.lat if self.lat else 0.0

    def set_longitude(self, lon) -> None:
        """
        Set the longitude value if it is valid, if it is not valid use the previous value, if there
        was not one set, default to 0.0
        :param lon: longitude value
        :return: none
        """
        self.lon = lon if valid_lon(lon) else self.lon if self.lon else 0.0

    def parse(self, data: str) -> None:
        """
        Read in a string contain lat, lon, altitude. Note, all whitespace is ignored but it is NOT a delimiter

        If data is comma separated it is parsed as lat, lon, alt [altitude is optional -> default to 0.0].

        Ex: 76.45, -110.123, 0.0
        Ex: 76.45, -110.123

        If the data is colon separated with commas, a string identifier should be added to denote the field, AND the
        arguments should be comma delimited

        Ex: Lat: 76.45, LONGITUDE: -110.123, AltitudE: 0.0

        Note: the spelling does not matter

        Values that can be parsed AND are valid will be set, Other values will REMAIN

        :param data: String to be parsed
        :return: None, the values are set internally
        """
        if data:
            """ Remove all whitespace and lower case the value"""
            data = data.lower()
            data = "".join(data.split())

            split_data = data.split(",")
            if ":" in data:

                for x in split_data:
                    kv = x.split(":")

                    if len(kv) == 2:
                        if 'lat' in kv[0]:
                            self.try_set_latitude(kv[1])
                        elif 'lon' in kv[0]:
                            self.try_set_longitude(kv[1])
                        elif 'alt' in kv[0]:
                            self.try_set_altitude(kv[1])
            else:
                if len(split_data) == 2:
                    """" Latitude, Longitude """
                    self.try_set_latitude(split_data[0])
                    self.try_set_longitude(split_data[1])
                elif len(split_data) == 3:
                    """ Latitude, Longitude, Altitude"""
                    self.try_set_latitude(split_data[0])
                    self.try_set_longitude(split_data[1])
                    self.try_set_altitude(split_data[2])

    def try_set_latitude(self, data: str) -> None:
        """
        Function to protect the setting of a latitude value
        :param data: potential latitude value
        :return: none
        """
        try:
            self.set_latitude(float(data))
        except ValueError:
            pass

    def try_set_longitude(self, data: str) -> None:
        """
        Function to protect the setting of a longitude value
        :param data: potential longitude value
        :return: none
        """
        try:
            self.set_longitude(float(data))
        except ValueError:
            pass

    def try_set_altitude(self, data: str) -> None:
        """
        Function to protect the setting of a altitude value
        :param data: potential altitude value
        :return: none
        """
        try:
            self.alt = float(data)
        except ValueError:
            pass


def in_distance(p1: Point, p2: Point, distance: float) -> bool:
    """
    Determine if two latitude/longitude points are within a certain distance from each other.

    Earth's Radius R = 6371 km

    :param p1: Point 1
    :param p2: Point 2
    :param distance: distance in meters
    :return: true if p2 is less than or equal to distance(meters) from p1
    """
    R = 6371.0 * 1000.0 # earth's radius in meters
    lat1r = math.radians(p1.lat)
    lat2r = math.radians(p2.lat)

    diff1 = math.radians(p2.lat - p1.lat)
    diff2 = math.radians(p2.lon - p1.lon)

    a = math.pow(math.sin(diff1/2.0), 2.0) + (math.cos(lat1r) * math.cos(lat2r)) + math.pow(math.sin(diff2/2.0), 2.0)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return (R * c) <= distance