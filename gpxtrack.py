import gpxpy
import gpxpy.gpx
import argparse
from coordinates import Coordinates
from workouts import Workout

def is_float(s):
    try:
        sf = float(s)
        return True

    except ValueError:
        return False

parser = argparse.ArgumentParser(description='Choose GPX file.')

parser.add_argument("gpx", nargs=1, action='store', type=str)
parser.add_argument("infile", nargs=1, action='store', type=str)
parser.add_argument("--add", action='store', nargs="?", default=0, dest='wolen')

args = parser.parse_args()
print(args.gpx)

f = open(args.gpx[0], "r")

gpxd = gpxpy.parse(f)
f.close()
gpx = gpxd

pts = gpx.get_points_data()

s = 0

if args.wolen != 0:
    f = open(args.infile[0], 'a')
    f.write(str(args.wolen) + "\n")
    f.close()

f = open(args.infile[0], 'r')
fr = f.readlines()

dists = []
for l in fr:
    w = Workout(line=l[:-1])
    if w.valid:
        s += w.get_dist()
        dists.append(s)

coords = [ [Coordinates(pts[0].point.latitude, pts[0].point.longitude), 0] ]
traveled = 0
ct = 0
done = False
for d in dists:
    while d > traveled:
        ct += 1
        if ct == len(pts)-1:
            done = True
            break

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

    coords.append([Coordinates(segstartpt.latitude + extralat, segstartpt.longitude + extralon), d/1609.34])

print("")
print("Original position: {}".format(coords[0][0]))
print("")

lc = len(coords)
for i in range(1, lc):
    print("Data point {} of {}, Distance traveled: {:.2f} mi".format(i, lc-1, coords[i][1]))
    print("Position at data point {}: {}".format(i, str(coords[i][0])))
    print("")

if done:
    print("You're done!")

# print("Current Data Point {} of {}, Distance traveled: {}".format(lc-1, lc-1, coords[i][2]))
# print("Current position: {}, {}".format(coords[-1][0], coords[-1][1]))
