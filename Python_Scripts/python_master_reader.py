import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from scipy.interpolate import interp1d
import numpy as np

# In the dumpingground folder read the master.csv file and extract the paths of the csv files.
df = pd.read_csv("dumpingground/master.csv")
import re
# Read the 2nd column of the master.csv file and save it to a list.
csv_paths = df.iloc[:,2]


"""
Basic example of how to use the saved data to create a graph.
Again, this is not the best way to do this, but it works.

Because of glitches in the sensors I had to use a threshold as to not have spikes in the graph.

Smoothing doesnt really look good but it works.
"""
smoothing = True
threshold = 150

# Read the csv files and save them to a list.
csv_files = []
for i in tqdm(csv_paths):
    csv_files.append(pd.read_csv(i))

# For each csv file, read the 1st column and save it to a list.
csv_Date_values = []
for i in tqdm(csv_files):
    csv_Date_values.append(i.iloc[:,0])

# For each csv file read the 2nd column and save it to a list.
csv_Value_values = []
for i in tqdm(csv_files):
    csv_Value_values.append(i.iloc[:,1])

# Split each string in the csv_Value_values into a list of integers and then save it to a list and store that list in another list.

csv_Value_values_intC = []
ind = 0
for i in tqdm(csv_Value_values):
    csv_Value_values_int = []
    ind+=1
    tempList = i.values
    for j in tempList:
        csv_Value_values_int.append(float(re.sub(r"[^0123456789\.]","",str(j))))
    csv_Value_values_intC.append(csv_Value_values_int)

ind = 0
averaged_out = []
for i in tqdm(csv_Value_values_intC, desc="Averaging: "):
    csv_Value_values_intC_first = []
    for it in csv_Value_values_intC:
        if ind > len(csv_Value_values_intC[ind]) - 1:
            csv_Value_values_intC_first.append(csv_Value_values_intC[ind][len(csv_Value_values_intC[ind]) - 1])
        else:
            csv_Value_values_intC_first.append(csv_Value_values_intC[ind][ind])

# Average out the values in the csv_Value_values_intC_first list.
    csv_Value_values_intC_first_avg = []
    csv_Value_values_intC_first_avg.append(sum(csv_Value_values_intC_first)/len(csv_Value_values_intC_first))
    averaged_out.append(csv_Value_values_intC_first_avg)
    ind+=1



# Create a list of datetimes from the csv_Date_values list.
csv_Date_values_datetime = []

for i in csv_Date_values:
    csv_Date_values_datetime.append(pd.to_datetime(i))

# Remove the last 6 characters from each string in the csv_Date_values_datetime list.
csv_Date_values_datetime_str = []
for i in csv_Date_values_datetime:
    csv_Date_values_datetime_str.append(str(i)[:-6])

# Create a list with numbers counting up until the length of the averaged_out list
csv_Date_values_datetime_str_count = []
for i in range(len(averaged_out)):
    csv_Date_values_datetime_str_count.append(i)

# Go through each averaged out value and if it is above the threshold limit it to the threshold limit.
for i in range(len(averaged_out)):
    if averaged_out[i][0] > threshold:
        averaged_out[i][0] = threshold


# Plot the csv_Value_values_int_avg list and the csv_Date_values_datetime list.
if smoothing == True:
    # Convert averaged_out and csv_Date_values_datetime_str_count to numpy arrays.
    averaged_out_np = np.array(averaged_out).squeeze()
    csv_Date_values_datetime_str_count_np = np.array(csv_Date_values_datetime_str_count).squeeze()

    # Using cubic interpolation to smooth the data.
    f = interp1d(csv_Date_values_datetime_str_count_np, averaged_out_np, kind='cubic', fill_value='extrapolate')
    xnew = np.linspace(0, len(averaged_out_np), num=len(averaged_out_np)*2)
    # If the smooth data goes under 0 set it to 0.
    for i in range(len(xnew)):
        if xnew[i] < 0:
            xnew[i] = 0

    plt.plot(xnew, f(xnew))

    #plt.plot(csv_Date_values_datetime_str_count, smooth_averaged_out, label="Smoothed Average")
else:
    plt.plot(csv_Date_values_datetime_str_count, averaged_out, color="red", label="Average", linewidth=0.5)
plt.ylabel('Average Value')
plt.xlabel('Time')
plt.title('Average Value of the Sensor')
plt.show()