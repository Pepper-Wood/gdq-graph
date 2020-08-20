# Alternative web scraper to pull data from the donations list
# This will be used to get the archival data

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from progress.bar import ChargingBar    # progress==1.5
import time
import beepy                            # beepy==1.0.7
from os import path

def fetch_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    FIVE_MINUTES = 5 * 60 # number of seconds in five minutes
    bar = ChargingBar(f"  - Sleeping", max=FIVE_MINUTES)
    for i in range(FIVE_MINUTES):
        bar.next()
        time.sleep(1)
    bar.finish()
    return soup

def get_comment_from_table_row(table_row):
    links = table_row.findAll('a')
    hrefs = [ link.get('href') for link in links ]      # ['/tracker/donor/432156/28', '/tracker/donation/655884']
    dono_link = [ href for href in hrefs if '/tracker/donation/' in href ]
    if len(dono_link) == 0:
        return "ERROR: dono link not found"

    soup = fetch_soup("https://gamesdonequick.com" + dono_link[0])
    comment = soup.find("td", class_="APPROVED")
    if comment is None:
        return "ERROR: td.APPROVED not found"
    return comment.get_text().replace("\n", "")

def get_comment_url_from_table_row(table_row):
    # A smaller function compared to get_comment_from_table_row() to reduce the number of url requests being made.
    links = table_row.findAll('a')
    hrefs = [ link.get('href') for link in links ]      # ['/tracker/donor/432156/28', '/tracker/donation/655884']
    dono_link = [ href for href in hrefs if '/tracker/donation/' in href ]
    if len(dono_link) == 0:
        return "ERROR: dono link not found"
    return dono_link[0]

def update_csv_from_soup(gdq_run, page_num):
    soup = fetch_soup(f"https://gamesdonequick.com/tracker/donations/{gdq_run}?page={page_num}")

    file = open(f"{gdq_run}.csv",'a')
    table = soup.find("table")
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        if len(columns) > 0:
            for column in columns:
                output_row.append(column.text.replace("\n", ""))
            comment = "No comment"
            if output_row[-1] == "Yes":
                comment = get_comment_url_from_table_row(table_row)
            file.write(f"\n{page_num}," + ",".join(output_row[:-1]) + "," + comment)
    file.close()

def initialize_csv(gdq_run):
    filename = f"{gdq_run}.csv"
    if not path.exists(filename):
        file = open(filename,'a')
        file.write("pageNum,donorName,timeReceived,amount,comment")
        file.close()

def collect_data(gdq_run, start_page, end_page):
    initialize_csv(gdq_run)
    print(f"Collecting donation data from {gdq_run}...")
    for page_num in range(start_page, end_page+1):
        print(f"- Page {page_num}")
        update_csv_from_soup(gdq_run, page_num)
    beepy.beep(sound=6) # Play 'success.wav'

if __name__ == "__main__":
    # actual max is 1085, but this is being broken apart
    collect_data('agdq2020', 6, 20)
