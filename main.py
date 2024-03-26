import csv
import requests
import sys
import math
import time
import matplotlib.pyplot as plt

class Weather:
    def __init__(self, wD, T, wS, P, H, wG, C):
        self.wD = wD
        self.T = T
        self.wS = wS
        self.P = P
        self.H = H
        self.wG = wG
        self.C = C

# This is the core of our weather query URL
def getData():

    BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/'

    if len(sys.argv) < 4:
        print('')
        print('Usage: FetchWeather Location Date API_KEY')
        print()
        print('  Location: Please provide a location for the weatch search.')
        print('    (Make sure to use quotes if the name contains spaces.)')
        print('  Date: Please specify a date in the format YYYY-MM-DD to look up weather for a specific date.')
        print('    Or use the FORECAST to look up the current weather forcast.')
        print('  API_KEY: Please specify your Visual Crossing Weather API Key')
        print('    If you don\'t already have an API Key, get one at www.visualcrossing.com/weather-api.')
        print()
        print('Example: FetchWeather \"Herndon, VA\" 2006-04-12 KEY_123')
        print('Example: FetchWeather \"Beverly Hills, CA\" FORECAST KEY_123')
        print()
        sys.exit()

    print('')
    print(' - Requesting weather for: ', sys.argv[1])

    DateParam = sys.argv[2].upper()

    QueryLocation = '&location=' + requests.utils.quote(sys.argv[1])

    QueryKey = '&key=' + sys.argv[3]

    if DateParam == 'FORECAST':
        print(' - Fetching forecast data')
        QueryTypeParams = 'forecast?&aggregateHours=24&unitGroup=us&shortColumnNames=false'
    else:
        print(' - Fetching history for date: ', DateParam)

        # History requests require a date.  We use the same date for start and end since we only want to query a single date in this example
        QueryDate = '&startDateTime=' + DateParam + 'T00:00:00&endDateTime=' + sys.argv[2] + 'T00:00:00'
        QueryTypeParams = 'history?&aggregateHours=24&unitGroup=us&dayStartTime=0:0:00&dayEndTime=0:0:00' + QueryDate

    URL = BaseURL + QueryTypeParams + QueryLocation + QueryKey

    print(' - Running query URL: ', URL)
    print()

    response = requests.get(URL, timeout=20)

    weatherL =[]

    if response.status_code == 200:
        CSVText = csv.reader(response.text.splitlines())
        RowIndex = 0
        # Collect data
        for Row in CSVText:
            if RowIndex == 0:
                RowIndex+=1
            else:
                weatherL.append(Weather(Row[6], Row[9], Row[10], Row[11], Row[15], Row[16], Row[17]))
                RowIndex+=1
        return weatherL
    else:
        print('Error:', response.status_code)

# Calculate distance
def calcD(a, v, w, weight):

    g = 9.81
    lang = math.radians(a)
    wS = float(w.wS)
    wD = math.radians(float(w.wD))
    t_int = 0.1

    t=0
    xvals=[]
    yvals=[]
    yC = 0
    while True:
        rho = calcAirD(w, yvals[-1] if yvals else 0)

        wH = wS * math.cos(wD)
        wV = wD * math.sin(wD)

        x = v * math.cos(lang) * t + wH * t
        y = v * math.sin(lang) * t - 0.5 * (weight /rho) * g * t**2 + wV * t

        xvals.append(x)
        yvals.append(y)

        if y <= 0 and yC > 0:
            # Make final y coordinate positve grab x
            if y < 0:
                i = len(yvals) - 2
                x_at_y0 = xvals[i] + (xvals[i + 1] - xvals[i]) * (-yvals[i]) / (yvals[i + 1] - yvals[i])
                xvals[-1] = x_at_y0
                yvals[-1] = 0
            break

        t += t_int
        yC = 1

    return xvals, yvals, t_int

# Calculate Air Density 
def calcAirD(w, y):

    lapse_rate = -0.0065
    T_0 = float(w.T)
    P_0 = 101325
    R = 287.058
    T = T_0 + lapse_rate * y
    P = P_0 * ((1 - lapse_rate * y / T_0) ** (5.25588))
    rho = P / (R * T)

    return rho

def main():

    wL = getData()
    day = int(input("Days into the future (MAX of 15): "))

    weight = float(input("Weight (kg): "))
    v0 = float(input("Initial velocity (m/s): "))
    angle = float(input("Angle shot at: "))

    xvals, yvals, t_int = calcD(angle, v0, wL[day], weight)
    for i in range(len(xvals)):
        print("Time: %.1f" % (float(i) * float(t_int)), "s, Position: (%.2f, %.2f)" % (xvals[i], yvals[i]))

    plt.plot(xvals, yvals)
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title('Projectile Trajectory')
    plt.grid(True)
    plt.show()

main()