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
    donation_total = donos_info[2]
    # $323,971.50 (6338) —
    donation_total = donation_total.replace("$", "").replace(") —", "").replace(",", "").split(" (")
    # ['323971.50',' 6338']

    max_avg_donation = donos_info[4]
    # $10,000.00/$51.12
    max_avg_donation = max_avg_donation.replace("$", "").replace(",", "")
    # 10000.00/51.12
    max_avg_donation = max_avg_donation.split("/")

    totals = ",".join(donation_total) + "," + ",".join(max_avg_donation)
    return totals

def add_to_csv(totals_str):
    file = open('sgdq2020.csv','a')
    file.write(f"\n{datetime.now()},{totals_str}")
    file.close()

if __name__ == "__main__":
    donos_info = get_donos_info_from_soup()
    totals_str = extract_totals(donos_info)
    add_to_csv(totals_str)
