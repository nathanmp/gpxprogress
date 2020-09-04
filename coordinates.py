class Coordinates:

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f"{self.lat:5f}{'N' if self.lat > 0 else 'S'}, {self.lon:5f}{'E' if self.lon > 0 else 'W'}"

    def __repr__(self):
        return f"Coordinates {self.lat:5f}{'N' if self.lat > 0 else 'S'}, {self.lon:5f}{'E' if self.lon > 0 else 'W'}"
