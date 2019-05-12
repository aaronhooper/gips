from bs4 import BeautifulSoup
import requests
import re
import logging

SITE = 'https://ipgeolocation.io/ip-location/'

def geolocate_ips(ips):
    """

    @type ips: list
    @param ips: IP addresses

    @rtype: list
    @return: countries from which ips are located
    """
    countries = remove_emptys([geolocate_ip(ip) for ip in ips])
    return countries


def extract_ips(file_object):
    """

    @type file_object: file
    @param file_object: file object containing IP addresses

    @rtype: list
    @returns: IP addresses
    """
    file_text = file_object.read()

    logging.info("Extracting ip addresses from stdin ...")
    ipv4_address = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ips = ipv4_address.findall(file_text)
    return ips


def geolocate_ip(ip):
    """

    @type ip: string
    @param ip: IP address

    @rtype: string
    @returns: country where ip is located or an empty string for a reserved address
    """
    if is_reserved(ip):
        logging.info("Not locating reserved ip address " + ip)
        return ""

    html = requests.get(SITE + ip).text
    logging.info("Extracting country for " + ip + " ...")
    country = extract_country(html)
    logging.info("Country found: " + country)

    return country


def extract_country(html):
    """

    @type html: string
    @param html: HTML text

    @rtype: string
    @returns: the country name or an empty string if none was found
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

    @type ip: string
    @param ip: IP address

    @rtype: boolean
    @returns: if the IP is reserved or not
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


def remove_emptys(array):
    """

    @type array: list
    @param array: a list that contains empty elements

    @rtype: list
    @returns: a list with the empty elements removed
    """
    return list(filter(lambda item: item != '', array))
