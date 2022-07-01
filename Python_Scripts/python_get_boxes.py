from datetime import datetime
import sensemapi
import sys
import config
import os
import math
from sensemapi import client

from geopy import geocoders
gn = geocoders.GeoNames(username="Martin_Martin")

"""
Get all the boxes from a city and a radius in km.
The city is given by the user.
The Long Lat calculation is not very accurate. at all.
"""


city = input("Enter city: ")
rangeKM = input("Enter range in KM: ")
hasParams = input("Enter parameters (PM10, PM2.5, CO2, Temp, AirPressure. SEPERATE WITH ,): ")

Params = hasParams.split(",")

LongLatTemp = gn.geocode(city)
r_earth = 6378.137
pi = 3.14159265359

print("CITY LOCATED AT: ",LongLatTemp.latitude, LongLatTemp.longitude, "\nADDING {} KM AS BOUNDING BOX".format(rangeKM))
new_latitude  = LongLatTemp.latitude  - (int(rangeKM)*20 / r_earth) * (180 / pi)
new_longitude = LongLatTemp.longitude + (int(rangeKM)*20 / r_earth) * (180 / pi) / math.cos(LongLatTemp.latitude * pi/180)

bbox = [LongLatTemp.latitude, LongLatTemp.longitude, new_latitude, new_longitude]

phenomenon = []
if "PM10" in Params:
    phenomenon.append("PM10")
if "PM2.5" in Params:
    phenomenon.append("PM2.5")
if "CO2" in Params:
    phenomenon.append("CO2")
if "Temp" in Params:
    phenomenon.append("Temperatur")
if "CH4" in Params:
    phenomenon.append("CH4")

    




cli = client.SenseMapClient()


# Round all the values in bbox to 0 decimal places
for i in range(len(bbox)):
    bbox[i] = round(bbox[i], 3)
print(bbox)


boxes = cli.get_boxes(bbox=bbox,from_date=datetime.strptime('4/5/22', '%d/%m/%y'), to_date=datetime.now(), phenomenon=phenomenon, minimal=True)
print(f"Found {len(boxes)} boxes. How many do you want to download? Enter nothing to download them all." )

download_count = input("Enter number: ")
if download_count == "":
    download_count = int(len(boxes))
else:
    download_count = int(download_count)

# Go through all the boxes and get their box id
box_ids = []
for i in range(download_count):
    box_ids.append(boxes[i].id)

# Print out the first 10 box ids
print(box_ids[:10])

#Save all the box ids to a csv file with the header "ID" 
with open("box_ids.csv", "w") as f:
    f.write("ID\n")
    for i in box_ids:
        f.write(str(i) + "\n")

# Print success
print("Successfully saved box ids to box_ids.csv")


print("Run another script to get the data.")