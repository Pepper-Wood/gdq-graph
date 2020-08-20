import csv
import time
from datetime import datetime
from pytz import timezone

def get_unixtime(date_str):
    # 2020-01-12T21:35:11.692471-05:00
    date_time = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    unixtime = int(time.mktime(date_time.timetuple()))
    return unixtime

with open('agdq2020_test.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

'''
for row in data:
    if row[0] == "pageNum":
        continue
    curr_unixtime = get_unixtime(row[2])
    curr_datetime = datetime.fromtimestamp(curr_unixtime)
    curr_datetime = timezone('America/New_York').localize(curr_datetime)
    print(curr_datetime.strftime('%Y-%m-%d %H:%M:%S %Z%z') + f"\t\t{row[1]}")
'''

header = "utcUnixTimestamp,donationAmount,comment"
new_csv = []
for row in data:
    if row[0] == "pageNum":
        continue
    new_row = []
    new_row.append('"' + str(get_unixtime(row[2])) + '"')
    new_row.append('"' + row[3] + '"')
    new_row.append('"' + row[4] + '"')
    new_csv.append(",".join(new_row))

new_csv.sort()
for row in new_csv:
    print(row)
