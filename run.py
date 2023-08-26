import time,threading
import os
import logging
from dotenv import load_dotenv
import requests

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

#Global Vars
DOMAIN = ''
SUBDOMAINS = []
AUTH_HEADERS = {}
INTERVAL = 60

def get_current_ip():
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    logging.info('external ip address: {}'.format(ip))
    return ip


def update_dns():
    ctime = time.ctime()
    logging.info(f"Starting JOB at {ctime}")

    ip = get_current_ip()
    list_request_url = 'https://api.digitalocean.com/v2/domains/{}/records'.format(DOMAIN)
    response = requests.get(list_request_url, headers=AUTH_HEADERS)
    if response.status_code == 200:
        logging.info('Received Records List')
    else:
        logging.error('Something went wrong by receiving list, check network connection')
        return

    list_response = response.json()

    for sub in SUBDOMAINS:
        record = next(filter(lambda n: True if n['name'] == sub and n['type'] == 'A' else False, list_response['domain_records']), None)
        if record is None:
            print(f'A Record not found for {sub}')
        else:
            update_a_record(record, ip)

    threading.Timer(INTERVAL, update_dns).start()


def update_a_record(record, ip):
    record_domain = record['name']
    record_id = record['id']
    if record['data'] == ip:
        logging.info(f'DNS Record {record_domain} has already IP {ip}')
        return

    update_url = 'https://api.digitalocean.com/v2/domains/{}/records/{}'.format(DOMAIN, record_id)
    response = requests.patch(update_url, json={'data': ip, 'type': 'A'}, headers=AUTH_HEADERS)

    if response.status_code == 200:
        logging.info("Updated DNS record")
    else:
        logging.error("Update failed")
        logging.error('HTTP Status Code: {}'.format(response.status_code))
        logging.error(response.content)

def main():
    global AUTH_HEADERS, SUBDOMAINS, DOMAIN, INTERVAL
    load_dotenv()

    if os.getenv("API_TOKEN") is None:
        print("API_TOKEN is not set")
        exit(1)

    if os.getenv("DOMAIN") is None:
        print("DOMAIN is not set")
        exit(1)

    if os.getenv("SUBDOMAINS") is None:
        SUBDOMAINS.append("@")
    else:
        subd_str = os.getenv("SUBDOMAINS")
        SUBDOMAINS =subd_str.split(";")

    api_token = os.getenv("API_TOKEN")
    AUTH_HEADERS = {'Authorization': 'Bearer ' + api_token}
    DOMAIN = os.getenv("DOMAIN")
    INTERVAL = int(os.getenv("INTERVAL_M", "5"))*60

    update_dns()


if __name__ == '__main__':
    main()