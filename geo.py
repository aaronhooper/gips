from bs4 import BeautifulSoup
import requests
import re
import logging

SITE = 'https://ipgeolocation.io/ip-location/'

def geolocate_ips(ips):
    """
    Returns a list of countries that the IP addresses belong to.

    @type ips: list
    @rtype: list
    """
    countries = remove_emptys([geolocate_ip(ip) for ip in ips])
    return countries


def extract_ips(file_object):
    """
    Returns a list containing all IP addresses found in the file
    object.

    @type file_object: file
    @rtype: list
    """
    file_text = file_object.read()

    logging.info("Extracting ip addresses from stdin ...")
    ipv4_address = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ips = ipv4_address.findall(file_text)
    return ips


def geolocate_ip(ip):
    """
    Returns a country from which an IP address is located or '' for a
    reserved address.

    @type ip: string
    @rtype: string
    """
    if is_reserved(ip):
        logging.info(f"Not locating reserved ip address {ip}")
        return ""

    html = requests.get(SITE + ip).text
    logging.info(f"Extracting country for {ip} ...")
    country = extract_country(html)
    logging.info(f"Country found: {country}")

    return country


def extract_country(html):
    """
    Returns the country name extracted from the HTML or '' if none was
    found.

    @type html: string
    @rtype: string
    """
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
    """
    Returns a boolean representing whether the IP address is reserved
    or not.

    @type ip: string
    @rtype: boolean
    """
    ip_split = ip.split(".")

    if (ip_split[0] == "172" and 16 <= int(ip_split[1]) <= 31):
        return True

    if (ip_split[0] == "192" and ip_split[1] == "168"):
        return True

    if (ip_split[0] == "127"):
        return True

    if (ip_split[0] == "10"):
        return True

    return False


def remove_emptys(list_):
    """
    Returns a list with the empty elements removed.

    @type list_: list
    @rtype: list
    """
    return [item for item in list_ if item != '']
