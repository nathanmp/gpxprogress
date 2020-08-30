# gpxprogress
Shows the progress you've achieved on a given GPX file using a list of distances.

## Usage
Pass gpxtrack.py a valid GPX file and a list of distances traveled.
`python gpxtrack.py file.gpx distlog.txt`

## Format of GPX File

They're pretty easily downloadable, you can examine the file if you want to though. A great site to find GPX files is here. Find a route, then find the "GPX" button next to the Print button.
https://www.outdooractive.com/

As an example for testing (renamed to `CTD.gpx`):
https://www.outdooractive.com/en/route/mountain-biking/alberta/tour-divide-route/130569744/

## Format of Distance File

This currently has to be a newline-separated list of workouts, with up to three space-separated arguments each:
- Distance traveled. Required.
- Units the distance is measured in. Optional. Assumed to be miles if empty.
- A number to modify the distance. Optional.

If it's a positive number, the distance is multiplied by it.
If it's a negative number, the distance is divided by its absolute value.

## Output

Easiest to explain it by example.
`python gpxtrack.py CTD.gpx examplelog.txt` outputs the below:

~~~
Original position: 115.56016W, 51.161267N
Data point 1 of 5, Distance traveled: 10000.0
Position at data point 1: 115.483235W, 51.093321N

Data point 2 of 5, Distance traveled: 52164.708
Position at data point 2: 115.325098W, 50.808387N

Data point 3 of 5, Distance traveled: 98145.85085714285
Position at data point 3: 115.002885W, 50.521405N

Data point 4 of 5, Distance traveled: 100145.85085714285
Position at data point 4: 115.002885W, 50.521405N

Current Data Point 5 of 5, Distance traveled: 100145.85085714285
Current position: 115.002885W, 50.521405N
~~~
