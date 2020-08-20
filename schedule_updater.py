# File to re-parse the schedule.csv file to adjust the times to start from time 0
import csv
import datetime

def get_datetime(date_str):
    # 2020-08-16T11:30:00-04:00
    date_str = date_str.replace("-04:00", "").replace("T"," ")
    # 2020-08-16 11:30:00
    date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return date_time


with open('sgdq2020_schedule.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

zero_time = get_datetime(data[1][3])
for row in data:
    if row[0] == "name":
        continue
    start_time = get_datetime(row[3])
    end_time = get_datetime(row[4])
    start_zeroed = start_time - zero_time
    end_zeroed = end_time - zero_time
    print(f"Start: {start_zeroed}\t\t\tEnd  : {end_zeroed}")
