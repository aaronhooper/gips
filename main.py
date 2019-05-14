#!/usr/bin/env python3

import logging
from geo import extract_ips, geolocate_ip
import pickle
import sys

logging.basicConfig(level=logging.INFO)

ips = extract_ips(sys.stdin)
unique_ips = set(ips)
country_of = {}

for ip in unique_ips:
    country_of[ip] = geolocate_ip(ip)

fh = open('countries.txt', 'w')

for ip, country in country_of.items():
    print(ip + " -- " + country)
    fh.write(ip + " -- " + country + "\n")

fh.close()

logging.info('Dumping collection to file')
pickle.dump(country_of, open('dump.bin', 'wb'))
