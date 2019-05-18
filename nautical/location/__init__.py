from math import sin, cos, sqrt, radians, atan2


EARTH_RADIUS_METERS = 6372800


class Point:

    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0) -> None:
        """
        A 3D point containing latitude, longitude and altitude coordinates

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
        try:
            self.lat = float(lat) if -90.0 <= float(lat) <= 90.0 else self.lat if self.lat else 0.0
        except ValueError:
            pass

    def set_longitude(self, lon) -> None:
        """
        Set the longitude value if it is valid, if it is not valid use the previous value, if there
        was not one set, default to 0.0
        :param lon: longitude value
        :return: none
        """
        try:
            self.lon = float(lon) if -180.0 <= float(lon) <= 180.0 else self.lon if self.lon else 0.0
        except ValueError:
            pass

    def set_altitude(self, data: str) -> None:
        """
        Function to protect the setting of a altitude value
        :param data: potential altitude value
        :return: none
        """
        try:
            self.alt = float(data)
        except ValueError:
            pass

    def parse(self, data: str) -> None:
        """
        Read in a string contain lat, lon, altitude. Note, all whitespace is ignored but it is NOT a delimiter

        If data is comma separated it is parsed as lon, lat, alt [altitude is optional -> default to 0.0].
        NOTE: NOAA data is in the form LON, LAT

        Ex: -110.123, 76.45, 0.0
        Ex: -110.123, 76.45

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
                            self.set_latitude(kv[1])
                        elif 'lon' in kv[0]:
                            self.set_longitude(kv[1])
                        elif 'alt' in kv[0]:
                            self.set_altitude(kv[1])
            else:
                if len(split_data) == 2:
                    """" Latitude, Longitude """
                    self.set_longitude(split_data[0])
                    self.set_latitude(split_data[1])
                elif len(split_data) == 3:
                    """ Latitude, Longitude, Altitude"""
                    self.set_longitude(split_data[0])
                    self.set_latitude(split_data[1])
                    self.set_altitude(split_data[2])

    def get_distance(self, lat: float, lon: float) -> float:
        """
        Get the distance between this point and a lat/lon coordinate. This is the haversine methodology
        of calculating the distance between two points.
        :param lat: latitude coordinate (degrees)
        :param lon: longitude coordinate (degrees)
        :return: distance between the two points
        """
        lat1 = radians(self.lat)
        lat2 = radians(lat)

        diff1 = radians(self.lat - lat)
        diff2 = radians(self.lon - lon)

        a = sin(diff1 / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(diff2 / 2.0) ** 2

        return 2.0 * EARTH_RADIUS_METERS * atan2(sqrt(a), sqrt(1 - a))

    def in_range(self, lat: float, lon: float, distance: float) -> bool:
        """
        Determine if the latitude and longitude point is within the distance specified
        :param lat: latitude coordinate (degrees)
        :param lon: longitude coordinate (degrees)
        :param distance: distance to measure (meters)
        :return: true if it is in the distance
        """
        return self.get_distance(lat, lon) <= distance