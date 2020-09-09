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
    # STEP 1: Update the list with the new events to add to the graph
    events = [
        "agdq2018",
        "sgdq2017",
        "sgdq2018",
        "sgdq2020"
    ]

    f = open("reduced_data.txt", "w")
    time = get_time_at_interval(3)
    f.write("['" + "','".join(time) + "']\n\n\n")
    for event in events:
        event_result = readfileintowords(f"data-sorted/{event}_result.csv")
        event_result_data = get_data_at_interval(event_result, 3)
        f.write("['" + "','".join(event_result_data) + "']\n\n\n")
    f.close()

    # STEP 2: Update reduce.js with the new datasets results.
    # Color hexes are starting from the last row of the "Bright Color Palettes" image:
    # https://wondernote.org/color-palettes-for-web-digital-blog-graphic-design-with-hexadecimal-codes/
