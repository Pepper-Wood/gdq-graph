#!/usr/bin/env python
"""This script is run via a GitHub Actions cron every 5 minutes. It gets what current
GDQ event we're pulling archive from and the current page offset, parses the URL at
https://gamesdonequick.com/tracker/donations/{gdq_run}?page={page_num} and appends
the data to a CSV found in the data/ folder."""

from datetime import datetime
import json
import time
from os import environ, path
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
import sys

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

def get_donation_id(table_row):
    """Return the donation ID based on the table_row soup.

    Args:
        table_row (PageElement): soup element for the row in the table.

    Returns:
        string: donation ID as a string.
    """
    links = table_row.findAll('a')
    hrefs = [link.get('href') for link in links]
    # Expected hrefs result: ['/tracker/donor/432156/28', '/tracker/donation/655884']

    dono_link = [href for href in hrefs if "/tracker/donation/" in href]
    if len(dono_link) == 0:
        return "-1"
    return dono_link[0].replace("/tracker/donation/", "")

def convert_gmt_time_to_utc_unixtimestamp(date_str):
    """Returns the UTC unix timestamp based on a GMT-5 datestring.

    Args:
        date_str (string): GMT-5 datestring, i.e. 2020-01-12T21:35:11.692471-05:00

    Returns:
        string: UTC unix timestamp, i.e. 1578882911
    """
    try:
        date_time = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    except ValueError:
        date_time = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
    unixtime = int(time.mktime(date_time.timetuple()))
    return unixtime

def convert_money_string_to_number(money_string):
    """Transform dollar representation to a number-safe representation for calculations.

    Args:
        money_string (string): dollar representation of donation amount, i.e. $1,337.00.

    Returns:
        string: number representation of donation amount, i.e. 1337.00.
    """
    return money_string.replace("$", "").replace(",", "")

def write_csv_rows_to_csv(gdq_run, csv_rows):
    """Append new rows to the corresponding data/ CSV.

    Args:
        gdq_run (string): GDQ event string, i.e. agdq2020.
        csv_rows (string[][]): 2D list of new CSV row data.
    """
    file = open(f"data/{gdq_run}.csv", 'a')
    for row in csv_rows:
        file.write("\n" + row)
    file.close()

def update_csv_data(gdq_run, page_num):
    """Pull table from the specified donations page and update the corresponding data/ CSV.

    Args:
        gdq_run (string): GDQ event string, i.e. agdq2020.
        page_num (int): Current page to pull from.
    """
    soup = fetch_soup(f"https://gamesdonequick.com/tracker/donations/{gdq_run}?page={page_num}")
    csv_rows = []
    table = soup.find("table")
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        if len(columns) == 0:
            continue
        utc_unixtimestamp = convert_gmt_time_to_utc_unixtimestamp(columns[1].text.replace("\n", "").replace(" ", ""))
        donation_id = get_donation_id(table_row)
        donation_amount = convert_money_string_to_number(columns[2].text.replace("\n", "").replace(" ", ""))

        csv_rows.append(f"{utc_unixtimestamp},{donation_id},{donation_amount}")
    write_csv_rows_to_csv(gdq_run, csv_rows)

def open_archive_runs_json():
    """Get the data from archive_runs.json as a dictionary.

    Returns:
        gdq_runs (dict): Dictionary object representing JSON structure.
    """
    with open("archive_runs.json", "r") as openfile:
        gdq_runs = json.load(openfile)
    return gdq_runs

def save_archive_runs_json(gdq_runs):
    """Update archive_runs.json file with updated page_num and statuses.

    Args:
        gdq_runs (dict): Dictionary object representing JSON structure.
    """
    with open("archive_runs.json", "w") as outfile:
        json.dump(gdq_runs, outfile, indent=4)

def get_current_query():
    """Get the current GDQ event and the page number we are pulling from and update
    the offset once obtained.

    Returns:
        string, int: GDQ event string, i.e. agdq2020 & current page to pull from.
    """
    gdq_runs = open_archive_runs_json()
    for i, curr_run in enumerate(gdq_runs):
        if curr_run['status'] == "DONE":
            continue
        gdq_run = curr_run['gdq_run']
        page_num = curr_run['current_page']
        if curr_run['current_page'] == curr_run['max_page']:
            gdq_runs[i]['status'] = "DONE"
        else:
            gdq_runs[i]['current_page'] += 1
        save_archive_runs_json(gdq_runs)
        return gdq_run, page_num
    return "DONE", 0

def initialize_csv(gdq_run):
    """Create a new CSV for the run data if we are starting a new dataset.

    Args:
        gdq_run (string): GDQ event string, i.e. agdq2020.
    """
    filename = f"data/{gdq_run}.csv"
    if not path.exists(filename):
        file = open(filename, 'a')
        file.write("utc_unixtimestamp,donation_id,donation_amount")
        file.close()

if __name__ == "__main__":
    try:
        GDQ_RUN, PAGE_NUM = get_current_query()
        if GDQ_RUN != "DONE":
            initialize_csv(GDQ_RUN)
            update_csv_data(GDQ_RUN, PAGE_NUM)
    except:
        discord_webhook_url = environ.get("DISCORD_WEBHOOK")
        webhook = DiscordWebhook(
            url=discord_webhook_url,
            content=f"@here ERROR: {sys.exc_info()[0]}\n{sys.exc_info()[1]}"
        )
        response = webhook.execute()
