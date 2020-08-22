# This should pull from the donations pages via GitHub Actions cron
# And store the result in the format needed for showing the graph.

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def get_unixtime(date_str):
    # 2020-01-12T21:35:11.692471-05:00
    date_time = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    unixtime = int(time.mktime(date_time.timetuple()))
    return unixtime

def fetch_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup

def get_donation_id(table_row):
    # A smaller function compared to get_comment_from_table_row() to reduce the number of url requests being made.
    links = table_row.findAll('a')
    hrefs = [ link.get('href') for link in links ]      # ['/tracker/donor/432156/28', '/tracker/donation/655884']
    dono_link = [ href for href in hrefs if "/tracker/donation/" in href ]
    if len(dono_link) == 0:
        return "ERROR"
    return dono_link[0].replace("/tracker/donation/", "")

def get_csv_list(gdq_run, page_num):
    soup = fetch_soup(f"https://gamesdonequick.com/tracker/donations/{gdq_run}?page={page_num}")

    print("utcUnixTimestamp,donationId,donationAmount")
    table = soup.find("table")
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        if len(columns) > 0:
            for column in columns:
                output_row.append(column.text.replace("\n", ""))
            donationId = get_donation_id(table_row)

            gmtTimestamp =columns[1].text.replace("\n", "")                   # 2020-01-11T21:48:33.712968-05:00
            print(gmtTimestamp)
            utcUnixTimestamp = get_unixtime(gmtTimestamp)

            donationAmount = columns[2].text.replace("\n", "")                # $5.00
            donationAmount = donationAmount.replace("$", "").replace(",", "") # Convert money to number

            print(f"{utcUnixTimestamp},{donationId},{donationAmount}")

if __name__ == "__main__":
    get_csv_list('agdq2020', 160)
