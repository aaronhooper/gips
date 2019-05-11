from bs4 import BeautifulSoup
import requests
import re
import logging

SITE = 'https://ipgeolocation.io/ip-location/'

def geolocate_ips(ips):
    ips = set(ips) - {""}
    countries = [geolocate_ip(ip) for ip in ips]
    return countries

def extract_ips(filename):
    logging.info("Reading file " + filename)
    fh = open(filename, 'r', encoding='utf-8')
    file_text = fh.read()
    fh.close()

    logging.info("Extracting ip addresses from " + filename)
    ipv4_address = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", re.MULTILINE)
    ips = ipv4_address.findall(file_text)
    return ips

def geolocate_ip(ip):
    if is_reserved(ip):
        logging.info("Not locating reserved ip address " + ip)
        return ""

    html = requests.get(SITE + ip).text
    logging.info("Extracting country for " + ip + " ...")
    country = extract_country(html)
    logging.info("Country found: " + country)

    return country

def extract_country(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_cells = soup.findAll('td')

    try:
        country_header = table_cells[8]
    except ValueError:
        logging.error("Unable to extract country from html")
        return ""

    country_name = country_header.find_next_sibling().text.strip()
    return country_name

def is_reserved(ip):
    private_ip = re.compile(r"192\.168\.\d{1,3}\.\d{1,3}")
    return private_ip.match(ip) or ip == "127.0.0.1"

logging.basicConfig(level=logging.INFO)

ips = extract_ips('apache.txt')
countries = geolocate_ips(ips)

print(countries)

fh = open('countries.txt', 'w')
fh.write(str(countries))
fh.close()

