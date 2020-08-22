# gdqGraph


# Roadmap

## Setting up pulling archival data

Right now, `sgdq2020.csv` is populated by pinging the totals page every 5 minutes while SGDQ 2020 is currently live. In actuality, archival data should be calculated based on the data listed as part of the donations pages. `testing.html` is a proof-of-concept of what data is needed from the archival pages - with the example of AGDQ 2020 - and how to display it as the needed cumulative graph.

[x] Test what the datetime timezone is returned as when calling `new_archiver.py`. `new_archiver.py` is the script that will pull one page from the entire donations archive and should be storing its results to a CSV. It should read from an env file to get what offset to check and when to stop. CONFIRMED: datetime is returned as "2020-01-11T21:48:36.530573-05:00".
[ ] Update `new_archiver.py` based on the timezone that gets returned from the GitHub Pages call.
[ ] Update `new_archiver.py` to pull the offset from an env file and to update the number once done.


