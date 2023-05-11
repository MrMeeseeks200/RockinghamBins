#! /usr/bin/env python3
import schedule
import time
from bins import getBins

schedule.every().day.at("05:00").do(getBins)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute