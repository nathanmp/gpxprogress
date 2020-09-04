import gpxpy
import gpxpy.gpx
import argparse
from coordinates import Coordinates

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

coords = [ [Coordinates(pts[0].point.latitude, pts[0].point.longitude), 0] ]
traveled = 0
ct = 0

for d in dists:
    while d > traveled:
    	##keep going
        ct += 1
        traveled = pts[ct].distance_from_start

    segstartpt = pts[ct-1].point
    startdist = pts[ct-1].distance_from_start

    segendpt = pts[ct].point
    enddist = pts[ct].distance_from_start

    longdiff = segendpt.longitude - segstartpt.longitude
    latdiff = segendpt.latitude - segstartpt.latitude

    extradist = d - startdist
    diffdist = enddist - startdist

    extralon = longdiff * (extradist / diffdist)
    extralat = latdiff * (extradist / diffdist)

    # print(startdist)
    # print(d)
    # print(enddist)
    # print("")

    coords.append([Coordinates(segstartpt.latitude + extralat, segstartpt.longitude + extralon), d/1609.34])

print("")
print("Original position: {}".format(coords[0][0]))
print("")

lc = len(coords)
for i in range(1, lc):
    print("Data point {} of {}, Distance traveled: {:.2f} mi".format(i, lc-1, coords[i][1]))
    print("Position at data point {}: {}".format(i, str(coords[i][0])))
    print("")

# print("Current Data Point {} of {}, Distance traveled: {}".format(lc-1, lc-1, coords[i][2]))
# print("Current position: {}, {}".format(coords[-1][0], coords[-1][1]))
