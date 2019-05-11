import logging
import geo
import pickle

logging.basicConfig(level=logging.INFO)

ips = geo.extract_ips('apache.txt')
unique_public_ips = set(ips)
country_of = {}

for ip in unique_public_ips:
    country_of[ip] = geo.geolocate_ip(ip)

fh = open('countries.txt', 'w')

for ip, country in country_of.items():
    print(ip + " -- " + country)
    fh.write(ip + " -- " + country)

fh.close()

logging.info('Dumping collection to file')
pickle.dump(country_of, open('dump.bin', 'wb'))
