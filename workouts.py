def is_float(s):
    try:
        sf = float(s)
        return True

    except ValueError:
        return False

prefixes = {
    # "": 1,
    "da": 10,
    "h": 100,
    "k": 1000,
    "M": 1000000,
    "G": 1000000000
}
baseunits = {
    "ft": 0.3408,
    "yd": 0.9144,
    "m": 1,
    "mi": 1609.34
}

prefixkeys = list(prefixes.keys())
baseunitkeys = list(baseunits.keys())

class Workout:

    def __init__(self, dist=0, modifier=1, units="mi", line=""):
        self.valid = True

        if line != "":
            self.parse(line)

        else:
            self.dist = dist
            self.modifier = modifier
            self.unitmult = self.parse_units(units)

            if self.dist <= 0 or self.modifier <= 0 or len(units) == 0:
                self.valid = False


    def get_dist(self):
        if not self.valid:
            return 0

        print(self.dist)
        print(self.unitmult)
        print(self.dist * self.modifier * self.unitmult)

        return self.dist * self.modifier * self.unitmult

    def parse_units(self, u):

        unitmult = 0

        if len(u) == 0 or (len(u) == 1 and u != "m"):
            return 0

        if u[-1] == "m":
            unitmult = 1
            if u[:-1] in list(prefixes.keys()):
                unitmult *= prefixes[u[:-1]]
            return unitmult

        elif u[-2:] in baseunitkeys:
            unitmult = baseunits[u[-2:]]
            print(u[:-2])
            if u[:-2] in list(prefixes.keys()):
                unitmult *= prefixes[u[:-2]]

        else:
            return 0

        return unitmult

    def parse(self, st):
        ssplit = st.split(" ")

        if not is_float(ssplit[0]):
            self.dist = 0
            self.units = "mi"
            self.modifier = 1
            self.valid = False
            return

        self.invalid = True

        if "." in ssplit[0]:
            self.dist = float(ssplit[0])
        else:
            self.dist = int(ssplit[0])
        self.unitmult = 1609.34
        self.modifier = 1

        if len(ssplit) == 1:
            return

        for ind in range(1, len(ssplit)):
            if ind > 3:
                return

            elif is_float(ssplit[ind]):
                if "." in ssplit[ind]:
                    self.modifier = float(ssplit[ind])
                else:
                    self.modifier = int(ssplit[ind])

            else:
                su = self.parse_units(ssplit[ind])
                if su == 0:
                    self.valid == False
                else:
                    self.unitmult = su
