from datetime import datetime
import json
import time
from os import path
import requests
from bs4 import BeautifulSoup

def fetch_soup(url):
    """Return soup from url. Useful if multiple calls are needed so that a sleep can be added.

    Args:
        url (string): url string.

    Returns:
        BeautifulSoup: soup object result.
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup

def convert_schedule_gmt_time_to_utc_unixtimestamp(date_str):
    """Returns the UTC unix timestamp based on a GMT-5 datestring.

    Args:
        date_str (string): GMT-5 datestring, i.e. 2020-01-05T11:30:00-05:00

    Returns:
        string: UTC unix timestamp, i.e. 1578882911
    """
    date_time = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
    unixtime = int(time.mktime(date_time.timetuple()))
    return unixtime

def get_schedule_csv():
    soup = fetch_soup(f"https://gamesdonequick.com/tracker/runs/sgdq2019")
    csv_rows = []
    table = soup.find("table")
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        if len(columns) == 0:
            continue
        print([col.text for col in columns])
        '''
        utc_unixtimestamp = convert_gmt_time_to_utc_unixtimestamp(columns[1].text.replace("\n", "").replace(" ", ""))
        donation_id = get_donation_id(table_row)
        donation_amount = convert_money_string_to_number(columns[2].text.replace("\n", "").replace(" ", ""))
        csv_rows.append(f"{utc_unixtimestamp},{donation_id},{donation_amount}")
        '''

if __name__ == "__main__":
    # get_schedule_csv()
    print(convert_schedule_gmt_time_to_utc_unixtimestamp("2020-01-05T11:30:00-05:00"))
    print(convert_schedule_gmt_time_to_utc_unixtimestamp("2019-06-23T12:30:00-04:00"))
