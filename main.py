#!/usr/bin/env python3

import logging
import pickle
import sys

from geo import extract_ips, geolocate_ip

logging.basicConfig(level=logging.INFO)

ips = extract_ips(sys.stdin)
unique_ips = set(ips)
country_of = {}

for ip in unique_ips:
    country_of[ip] = geolocate_ip(ip)

with open("countries.txt", "w") as fh:
    for ip, country in country_of.items():
        print(f"{ip} -- {country}")
        fh.write(f"{ip} -- {country}\n")

logging.info("Dumping collection to file")
pickle.dump(country_of, open("dump.bin", "wb"))
