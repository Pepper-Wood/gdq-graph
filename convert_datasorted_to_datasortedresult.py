def readfileintowords(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

if __name__ == "__main__":
    # STEP 0: Create the sorted file using:
    # sort sgdq2019.csv -o sgdq2019.csv

    # STEP 1: FIND THE TIMESTAMP USING THIS WEBSITE: https://www.unixtimestamp.com/index.php
    event_info = {
        "agdq2020": 1578223800,
        "sgdq2019": 1561293000,
        "agdq2019": 1546774200
    }

    # STEP 2: CHANGE WHAT EVENT THIS IS POINTING TO
    EVENT = "agdq2019"
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
