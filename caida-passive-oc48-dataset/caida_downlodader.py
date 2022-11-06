import requests
from bs4 import BeautifulSoup
import os    

session = requests.session()

base_dir = "./pcap_stats/" # Dir where will be downloaded all the data.
base_url = "https://publicdata.caida.org/datasets/passive/passive-oc48/20020814-160000.UTC/pcap/"

response = session.get(base_url)

soup = BeautifulSoup(response.content, 'html.parser')

for a in soup.find_all('a'):
    if a.get('href') and "pcap.stats" == a.get('href')[-10::]:
        dir = a.get('href').split('.')[1]
        download_url = base_url + a.get('href')
        print("Downloading file from: {}".format(download_url))
        response = session.get(download_url)
        os.makedirs(base_dir + '/{}/'.format(dir), exist_ok=True)
        with open(base_dir + '/{}/'.format(dir) + a.get('href'), 'wb') as downloaded_file:
            downloaded_file.write(response.content)