# OpenSenseMap-Mass-Data  
 A few programs and python scripts to download and analyze data from opensensemap  


Current progress:  
python_get_boxes  
python_process_boxes  
python_master_reader  

python get boxes:  
A simple way to get boxIDs from sensemap using the sensemapi. Choose your city, add km around it ( innacurate, needs fixing ) add phenomenen and itll save a list of boxIDs to the current folder in a csv file.  

python process boxes:  
A simple way to process the data from many boxes at the same time. It reads the boxIDs stored in the csv made by python_get_boxes and then it will ask you a few questions about data and then download it.  
Itll ask how many days of data you want and what kind of data.  
Once its downloaded you should see a folder called "dumpingground", in there is a master.csv file that contains the boxIDs and their associated csv files.  
The download progress works by reading the boxIDs created earlier, splitting it up into 4 batches and then downloading them together at once.  

python master reader:  
Not really supposed to be used, but it was more testing if it was possible to collect and read the data downloaded earlier. It just goes through the master.csv and extracts the values.  


What i want to add:  
C# based collection, I am more experienced in C# than anything so if I can create a C# solution the speed and quality should go up.  
C# api, related to topic above.  
More efficient downloading in python_process_boxes.py.  
