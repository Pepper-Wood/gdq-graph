import csv

with open('agdq2020_test.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

for row in data:
    if len(row) > 5:
        print(row)