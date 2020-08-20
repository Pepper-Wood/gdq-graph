# Alternative web scraper to assemble the full GDQ schedule.

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
    return soup

def get_schedule_csv_from_soup(gdq_run):
    soup = fetch_soup(f"https://gamesdonequick.com/tracker/runs/{gdq_run}")

    file = open(f"{gdq_run}_schedule.csv",'a')
    table = soup.find("table")
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        if len(columns) > 0:
            for column in columns:
                output_row.append('"' + column.text.replace("\n", "") + '"')
            file.write(f"\n" + ",".join(output_row))
    file.close()

def initialize_csv(gdq_run):
    filename = f"{gdq_run}_schedule.csv"
    if not path.exists(filename):
        file = open(filename,'a')
        file.write("name,players,description,startTime,endTime,bidWars")
        file.close()

def get_schedule(gdq_run):
    initialize_csv(gdq_run)
    print(f"Getting schedule for {gdq_run}...")
    get_schedule_csv_from_soup(gdq_run)
    beepy.beep(sound=1) # Play 'coin.wav'

if __name__ == "__main__":
    # actual max is 1085, but this is being broken apart
    get_schedule('sgdq2020')
