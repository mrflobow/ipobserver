import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import miniupnpc
from dotenv import load_dotenv
import requests


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

#Global Vars
domain = ''
subdomains = []
auth_headers = {}

def get_current_ip():
    u = miniupnpc.UPnP()
    u.discoverdelay = 200
    u.discover()
    u.selectigd()
    logging.info('external ip address: {}'.format(u.externalipaddress()))
    return u.externalipaddress()


def update_dns():
    global auth_headers, subdomains, domain
    ip = get_current_ip()
    list_request_url = 'https://api.digitalocean.com/v2/domains/{}/records'.format(domain)
    response = requests.get(list_request_url, headers=auth_headers)
    if response.status_code == 200:
        logging.info('Received Records List')
    else:
        logging.error('Something went wrong by receiving list, check network connection')
        return

    list_response = response.json()



    for sub in subdomains:
        record = next(filter(lambda n: True if n['name'] == sub and n['type'] == 'A' else False, list_response['domain_records']), None)
        if record is None:
            print(f'A Record not found for {sub}')
        else:
            update_a_record(record, ip)


def update_a_record(record, ip):
    record_domain = record['name']
    record_id = record['id']
    if record['data'] == ip:
        logging.info(f'DNS Record {record_domain} has already IP {ip}')
        return

    update_url = 'https://api.digitalocean.com/v2/domains/{}/records/{}'.format(domain, record_id)
    response = requests.patch(update_url, json={'data': ip, 'type': 'A'}, headers=auth_headers)

    if response.status_code == 200:
        logging.info("Updated DNS record")
    else:
        logging.error("Update failed")
        logging.error('HTTP Status Code: {}'.format(response.status_code))
        logging.error(response.content)



def main():
    global auth_headers, subdomains, domain
    load_dotenv()

    if os.getenv("API_TOKEN") is None:
        print("API_TOKEN is not set")
        exit(1)

    if os.getenv("DOMAIN") is None:
        print("DOMAIN is not set")
        exit(1)

    if os.getenv("SUBDOMAINS") is None:
        subdomains.append("@")
    else:
        subd_str = os.getenv("SUBDOMAINS")
        subdomains =subd_str.split(";")

    api_token = os.getenv("API_TOKEN")
    auth_headers = {'Authorization': 'Bearer ' +api_token }
    domain = os.getenv("DOMAIN")
    interval = int(os.getenv("INTERVAL_M", "5"))


    scheduler = BackgroundScheduler()
    scheduler.add_job(update_dns, 'interval', minutes=interval)
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

if __name__ == '__main__':
    main()