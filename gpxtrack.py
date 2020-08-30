import gpxpy
import gpxpy.gpx
import argparse

def format_lat(lat):
    if lat < 0:
        return str(abs(lat)) + "S"
    return str(abs(lat)) + "N"

def format_lon(lon):
    if lon < 0:
        return str(abs(lon)) + "W"
    return str(abs(lon)) + "E"

def is_float(s):
    try:
        sf = float(s)
        return True

    except ValueError:
        return False

parser = argparse.ArgumentParser(description='Choose GPX file.')

parser.add_argument("gpx", nargs="?", action='store', type=argparse.FileType('r'))
parser.add_argument("infile", nargs="?", action='store', type=str)
parser.add_argument("--add", action='store', nargs="?", default=0, dest='wolen')

args = parser.parse_args()

gpxd = gpxpy.parse(args.gpx)
args.gpx.close()
gpx = gpxd

pts = gpx.get_points_data()

client_activated = False

s = 0

if args.wolen != 0:
    f = open(args.infile, 'a')
    f.write(str(args.wolen) + "\n")
    f.close()

f = open(args.infile, 'r')
fr = f.readlines()

dists = []
for i in fr:
	##i[-1] will always be newline
    if len(i) < 2:
        continue
    if i[0] not in list("1234567890"):
        continue
    dist = 0
    isp = i[:-1].split(" ")
    flag_a = False
    flag_b = False

    if len(isp) > 1 and not is_float(isp[1]):
            flag_a = True

    if len(isp) > 1:
        if len(isp) > 2 or is_float(isp[1]):
            flag_b = True

    try:
        dist = float(isp[0])
    except ValueError:
        continue

    if flag_a:

        if isp[1] == 'm':
            dist = dist

        elif isp[1] == 'dam':
            dist *= 10

        elif isp[1] == 'hm':
            dist *= 100

        elif isp[1] == 'km':
            dist *= 1000

        elif isp[1] == 'Mm':
            dist *= 1000000

        elif isp[1] == 'Gm':
            dist *= 1000000000

        elif isp[1] == "ft":
            dist *= 0.3048

        elif isp[1] == "yd":
            dist *= 0.9144

        else:
            dist *= 1609.34

    else:
        dist *= 1609.34

    if flag_b == True:
        distmultind = 2
        if len(isp) == 2:
            distmultind = 1

        try:
            distmult = float(isp[distmultind])
            if distmult < 0:
                dist /= abs(distmult)
            elif distmult > 0:
                dist *= distmult

        except ValueError:
            pass

    s += dist
    dists.append(s)

coords = [[format_lon(pts[0].point.longitude), format_lat(pts[0].point.latitude)]]
traveled = 0
ct = 1

for d in dists:
    while d > traveled:
    	##keep going
        ct += 1
        traveled = pts[ct].distance_from_start
    coords.append([format_lon(pts[ct].point.longitude), format_lat(pts[ct].point.latitude), d/1609.34])

print("")
print("Original position: {}, {}".format(coords[0][0], coords[0][1]))

lc = len(coords)
for i in range(1, lc):
    print("Data point {} of {}, Distance traveled: {:.2f} mi".format(i, lc-1, coords[i][2]))
    print("Position at data point {}: {}, {}".format(i, coords[i][0], coords[i][1]))
    print("")

# print("Current Data Point {} of {}, Distance traveled: {}".format(lc-1, lc-1, coords[i][2]))
# print("Current position: {}, {}".format(coords[-1][0], coords[-1][1]))
