import os
import whois
import argparse
import requests
import datetime
from urllib.parse import urlparse
from dateutil import relativedelta


def load_urls4check(path):
    with open(path, 'r') as infile:
        text = infile.read()
    return filter(None, text.split('\n'))


def is_server_respond_with_200(url):
    try:
        return requests.get(url).status_code == 200
    except requests.exceptions.BaseHTTPError:
        return False


def is_server_payed_for_month(domain_name):
    delta = relativedelta.relativedelta(
        get_domain_expiration_date(domain_name),
        datetime.datetime.now(),
    )
    return bool(delta.months or delta.years)


def get_domain_expiration_date(domain_name):
    date = whois.whois(domain_name).expiration_date
    if isinstance(date, datetime.datetime):
        return date
    elif isinstance(date, list):
        return date[0]


def output_urls_check(urls):
    for url in urls:
        print('url: {}\nreturn HTTP OK (200): {}\ndomain payed for month: {}\n'.format(
            url,
            is_server_respond_with_200(url),
            is_server_payed_for_month(urlparse(url).netloc),
        ))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Input filename')

    args = parser.parse_args()

    if args.filename and os.path.isfile(args.filename):
        urls = load_urls4check(args.filename)
        output_urls_check(urls)
