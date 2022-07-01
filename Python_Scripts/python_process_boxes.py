import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from concurrent.futures import ThreadPoolExecutor

from datetime import datetime, timedelta
import os
import pandas as pd
from sensemapi import client
from tqdm import tqdm
# Get the SenseMap API client
cli = client.SenseMapClient()


"""
This is not a clean code script. It is a mess.
Half written by me and the rest copilot.

Ill see if i can rewrite it or improve it later.
Going to test if i can get this api to work with C#.
"""

dayszAgo = input("How many days ago do you want to start reading measurements? Enter nothing for today: ")
if dayszAgo == "":
    dayszAgo = 0
else:
    dayszAgo = int(dayszAgo)

# Read all the lines in the box_ids.csv file. If a line contains a less than 3 characters, skip it. If a line contains more than 3 characters, save it to the box_ids list.
box_ids = []
progLine = 0
with open("box_ids.csv", "r") as f:
    totLine = f.readlines()
    print("Getting box ids from the file... This will not take long.")
    for line in tqdm(totLine):
        if len(line) > 3:
            box_ids.append(line[:-1])
            progLine += 1

# For each box id in the box_ids list, get the box and add it to a boxes list.
boxes = []
prog = 0
print("Getting boxes... This may take a while.")
for i in tqdm(box_ids):
    # Print out the progress of the script
    boxes.append(cli.get_box(i))
    prog += 1

pgon = 0
ascscss = 0
print(f"Got {len(boxes)} boxes. What value do you want to average out between them? It is reccommended to use the original collection data phenomenon.")
for sensor in boxes[0].sensors:
    pgon+=1
    print(f"{pgon} :: {sensor.title}")

ascscss = input("Enter name: ")

    
correctboxes = []
deadboxes = []

# Go through each box and get the last measurements of the value
print("Seperating lists into 4 parts...")
batch0 = []
batch1 = []
batch2 = []
batch3 = []

indexlen = len(boxes)
perindex = indexlen / 4
for i in range(0, int(perindex)):
    batch0.append(boxes[i])
for i in range(0, int(perindex)):
    batch1.append(boxes[i + int(perindex)])
for i in range(0, int(perindex)):
    batch2.append(boxes[i + int(perindex) * 2])
for i in range(0, int(perindex)):
    batch3.append(boxes[i + int(perindex) * 3])

done = []

def runBatch0():
    for box in tqdm(batch0, desc="Batch 1: "):
    # Get the index of the sensor with the name that the user entered
        index = [i for i, x in enumerate(box.sensors) if x.title == ascscss]

        try:
        # Save the measurements to a csv using pandas, where the first column is date and time and the second column is the value
            measurements = box.sensors[index[0]].get_measurements(from_date=datetime.now() - timedelta(days=dayszAgo), to_date=datetime.now())

            if len(measurements.data['value']) == 0:
                deadboxes.append(box)
            else:
                correctboxes.append(box)
                df = pd.DataFrame(measurements.series, dtype=object)
                df.to_csv(f"dumpingground/{box.id}.csv")
        except Exception as e:
            print(f"No measurements or a different error has occured. {e}")
            print("No data for this sensor. Debug: Index Of Sensor: " + str(index[0]) + " Index Of Box: " + str(batch0.index(box)))
    done.append("batch0")
    check()

def runBatch1():
    for box in tqdm(batch1, desc="Batch 2: "):
    # Get the index of the sensor with the name that the user entered
        index = [i for i, x in enumerate(box.sensors) if x.title == ascscss]

        try:
        # Save the measurements to a csv using pandas, where the first column is date and time and the second column is the value
            measurements = box.sensors[index[0]].get_measurements(from_date=datetime.now() - timedelta(days=dayszAgo), to_date=datetime.now())

            if len(measurements.data['value']) == 0:
                deadboxes.append(box)
            else:
                correctboxes.append(box)
                df = pd.DataFrame(measurements.series, dtype=object)
                df.to_csv(f"dumpingground/{box.id}.csv")
        except Exception as e:
            print(f"No measurements or a different error has occured. {e}")
            print("No data for this sensor. Debug: Index Of Sensor: " + str(index[0]) + " Index Of Box: " + str(batch1.index(box)))
    done.append("batch1")
    check()

def runBatch2():
    for box in tqdm(batch2, desc="Batch 3: "):
    # Get the index of the sensor with the name that the user entered
        index = [i for i, x in enumerate(box.sensors) if x.title == ascscss]

        try:
        # Save the measurements to a csv using pandas, where the first column is date and time and the second column is the value
            measurements = box.sensors[index[0]].get_measurements(from_date=datetime.now() - timedelta(days=dayszAgo), to_date=datetime.now())

            if len(measurements.data['value']) == 0:
                deadboxes.append(box)
            else:
                correctboxes.append(box)
                df = pd.DataFrame(measurements.series, dtype=object)
                df.to_csv(f"dumpingground/{box.id}.csv")
        except Exception as e:
            print(f"No measurements or a different error has occured. {e}")
            print("No data for this sensor. Debug: Index Of Sensor: " + str(index[0]) + " Index Of Box: " + str(batch2.index(box)))
    done.append("batch2")
    check()

def runBatch3():
    for box in tqdm(batch3, desc="Batch 4: "):
    # Get the index of the sensor with the name that the user entered
        index = [i for i, x in enumerate(box.sensors) if x.title == ascscss]

        try:
        # Save the measurements to a csv using pandas, where the first column is date and time and the second column is the value
            measurements = box.sensors[index[0]].get_measurements(from_date=datetime.now() - timedelta(days=dayszAgo), to_date=datetime.now())

            if len(measurements.data['value']) == 0:
                deadboxes.append(box)
            else:
                correctboxes.append(box)
                df = pd.DataFrame(measurements.series, dtype=object)
                df.to_csv(f"dumpingground/{box.id}.csv")
        except Exception as e:
            print(f"No measurements or a different error has occured. {e}")
            print("No data for this sensor. Debug: Index Of Sensor: " + str(index[0]) + " Index Of Box: " + str(batch3.index(box)))
    done.append("batch3")
    check()


# Run the batches on seperate cpu cores
executor = ThreadPoolExecutor(max_workers=4)
executor.submit(runBatch0)
executor.submit(runBatch1)
executor.submit(runBatch2)
executor.submit(runBatch3)

def check():
    if len(done) == 4:
        CreatingMaster()

"""
for box in tqdm(boxes):
    # Get the index of the sensor with the name that the user entered
    index = [i for i, x in enumerate(box.sensors) if x.title == ascscss]
    
    try:
        # Save the measurements to a csv using pandas, where the first column is date and time and the second column is the value
        measurements = box.sensors[index[0]].get_measurements(from_date=datetime.now() - timedelta(days=dayszAgo), to_date=datetime.now())

        if len(measurements.data['value']) == 0:
            deadboxes.append(box)
        else:
            correctboxes.append(box)
            df = pd.DataFrame(measurements.series, dtype=object)
            df.to_csv(f"dumpingground/{box.id}.csv")
        
    except Exception as e:
        print(f"No measurements or a different error has occured. {e}")
        print("No data for this sensor. Debug: Index Of Sensor: " + str(index[0]) + " Index Of Box: " + str(boxes.index(box)))
"""
# Create a master csv file that contains all the box ids and the location of the csv files
def CreatingMaster():
    print("\n\n\n")
    print(str(len(deadboxes)) + " Dead boxes found and ignored. " + str(len(correctboxes)) + " boxes with data found.")

    print("Creating master csv file...")

    master_df = pd.DataFrame(columns=["box_id", "csv_file"])
    for box in correctboxes:
        master_df = master_df.append({"box_id": box.id, "csv_file": f"dumpingground/{box.id}.csv"}, ignore_index=True)
    master_df.to_csv("dumpingground/master.csv")

    print("Done!")
    os.system("start dumpingground/master.csv")