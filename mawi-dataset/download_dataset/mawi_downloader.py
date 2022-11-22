import requests
import sys
from pathlib import Path
from datetime import timedelta, datetime
import pytz
import subprocess

def execute_command(command, output_file):
    with open(output_file, "w") as outfile:
        p = subprocess.run(command, stdout=outfile, stderr=subprocess.STDOUT)

def download_file(url, year, month):
    path = './{}/{}'.format(year, month)
    Path(path).mkdir(parents=True, exist_ok=True)
    file_name = './{}/{}/{}'.format(year, month, url.split('/')[-1])

    with open(file_name, "wb") as f:
        response = requests.get(url, stream=True)
        print("Downloading %s" % file_name)
        print("URL: {}".format(url))

        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            if int(total_length) < 500:
                print("[ERROR] File not found")
            else:
                dl = 0
                total_length = int(total_length)
                print("File size: " + "{:.2f}".format(total_length/(1024*1024)) + "MB")
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()
    
    return file_name

def add_0_if_single(number):
    if len(str(number)) == 1:
        return "0{}".format(number)
    return str(number)


def download_mawi_dump(year, day, month, hour_min):
    day_str = add_0_if_single(day)
    month_str = add_0_if_single(month)
    hour_min = hour_min
    url = "http://mawi.wide.ad.jp/mawi/samplepoint-F/{}/{}{}{}{}.pcap.gz".format(year, year, month_str, day_str, hour_min)

    file_name = download_file(url, year, month)
    return file_name

es_tz = pytz.timezone('Europe/Madrid')

date = es_tz.localize(datetime(2019, 1, 1))
dest_date = es_tz.localize(datetime(2022, 1, 1))
while date < dest_date:
    date += timedelta(days=1)
    # Download all mondays data.
    if date.weekday() == 0:
        file_name = download_mawi_dump(date.year, date.day, date.month, "1400")
        command = '"C:\Program Files\Wireshark\\tshark.exe" -r {} -T fields -e ip.src -e ip.dst -e ip.len -e frame.time_epoch -e icmp -E separator="," -E header=y -Y "tcp and !icmp"'.format(file_name)
        print("Command: {}".format(command))
        execute_command(command, file_name + '.csv')


# Sampling with pcap sampler.
# ./pcapsampler -m COUNT_SYS -r 100 filetosample.pcap sampledfile.pcap


# Tshark pcap to csv with ip source, ip dest, packet len and time. Only TCP packets.
# tshark -r .\200701011400.dump -T fields -e ip.src -e ip.dst -e ip.len -e frame.time_epoch -e icmp -E separator="," -E header=y -Y "tcp and !icmp"
# 491 MB file --> 15 minutes.

# Split pcap files by packets.
# https://www.thegeekstuff.com/2009/02/editcap-guide-11-examples-to-handle-network-packet-dumps-effectively/