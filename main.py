import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_donos_info_from_soup():
    url = "https://gamesdonequick.com/tracker/event/30"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Donation string is in the only <small> tag on the page.
    # It does not have any classes or IDs that can be searched instead.
    return soup.find('small').prettify().split("\n")

def extract_totals(donos_info):
    # ['<small>', ' Donation Total:', '$323,971.50 (6338) —', 'Max/Avg Donation:', '$10,000.00/$51.12', '</small>', '']
    donos_str = donos_info[2]
    # $323,971.50 (6338) —
    donos_str = donos_str.replace("$", "").replace(") —", "").replace(",", "").split(" (")
    # ['323971.50',' 6338']
    return float(donos_str[0]), float(donos_str[1])

def add_to_csv(dono_total, donor_count):
    file = open('sgdq2020.csv','a')
    file.write(f"\n{datetime.now()},{dono_total},{donor_count}")
    file.close()

if __name__ == "__main__":
    donos_info = get_donos_info_from_soup()
    dono_total, donor_count = extract_totals(donos_info)
    add_to_csv(dono_total, donor_count)
