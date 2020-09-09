def readfileintowords(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

if __name__ == "__main__":
    # Schedules found at https://gamesdonequick.com/tracker/runs/sgdq2020
    # Except for agdq2011, which was found at https://horaro.org/agdq/2011
    event_info = {
        "agdq2020": 1578223800, # Done
        "sgdq2019": 1561293000, # Done
        "agdq2019": 1546774200, # Done
        "sgdq2020": 1597577400, # Done
        "sgdq2018": 1529843400, # Done
        "agdq2018": 1515324600, # Done
        "sgdq2017": 1498998600, # Done
        "agdq2017": 1483875000, # Waiting
        "sgdq2016": 1467549000, # Waiting
        "agdq2016": 1451820600, # Waiting
        "sgdq2015": 1437912000, # Waiting
        "agdq2015": 1420372800, # Waiting
        "sgdq2014": 1403445600, # Waiting
        "agdq2014": 1388923200, # Waiting
        "sgdq2013": 1372168800, # Waiting
        "agdq2013": 1357478100, # Waiting
        "sgdq2012": 1337878800, # Waiting
        "agdq2012": 1325696400, # Waiting
        "sgdq2011": 1312470000, # Waiting
        "agdq2011": 1294329600  # Waiting
    }

    # STEP 1: Copy the data to be sorted into data-sorted. Then sort using:
    # sort sgdq2019.csv -o sgdq2019.csv
    # Make sure that the column headers get copied from the bottom of the file to the top

    # STEP 2: CHANGE WHAT EVENT THIS IS POINTING TO
    EVENT = "sgdq2017"
    TIME_START = event_info[EVENT]

    data = readfileintowords(f"data-sorted/{EVENT}.csv")
    cumulative = 0
    f = open(f"data-sorted/{EVENT}_result.csv", "w")
    f.write("seconds,utc_unixtimestamp,donation_id,donation_amount,cumulative_donation_amount\n")
    for i in range(1, len(data)):
        items = data[i].split(",")
        # 0: utc_unixtimestamp  1: donation_id  2: donation_amount
        seconds = int(items[0]) - TIME_START
        cumulative += float(items[2])
        f.write(",".join([
            str(seconds),    # seconds
            items[0],        # utc_unixtimestamp
            items[1],        # donation_id
            items[2],        # donation_amount
            "{:.2f}".format(cumulative)  # cumulative_donation_amount
        ]) + "\n")
    f.close()
