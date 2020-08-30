def readfileintowords(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

def get_time_at_interval(hours_interval):
    time = []
    hours = 0
    while len(time) < 90:
        time.append(str(hours))
        hours += hours_interval
    return time

def get_data_at_interval(event, hours):
    # seconds,utc_unixtimestamp,donation_id,donation_amount,cumulative_donation_amount
    CURR_SECONDS = 0
    event_data = []
    for i in range(1, len(event)):
        row = event[i].split(",")
        if int(row[0]) > CURR_SECONDS:
            event_data.append(row[4])
            CURR_SECONDS += hours * 60 * 60
    return event_data

if __name__ == "__main__":
    agdq2020 = readfileintowords("data-sorted/agdq2020_result.csv")
    sgdq2019 = readfileintowords("data-sorted/sgdq2019_result.csv")

    time = get_time_at_interval(3)
    agdq2020data = get_data_at_interval(agdq2020, 3)
    sgdq2019data = get_data_at_interval(sgdq2019, 3)

    print(len(time))
    print(len(agdq2020data))
    print(len(sgdq2019data))

    f = open("reduced_data.txt", "w")
    f.write("['" + "','".join(time) + "']")
    f.write("\n\n\n")
    f.write("['" + "','".join(agdq2020data) + "']")
    f.write("\n\n\n")
    f.write("['" + "','".join(sgdq2019data) + "']")
    f.close()
