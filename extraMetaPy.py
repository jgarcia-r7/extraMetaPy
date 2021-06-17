#!/usr/bin/env python3
# Title: extraMetaPy
# Author: Jessi
# Usage: ./extraMetaPy.py -d <domain> -o <output> -f <filedir> -l <results_limit> (Ex: ./extraMetaPy.py -d domain.com -o results.txt -f downloads/ -l 150)

import os
import argparse
import time
import subprocess
import json
import urllib.request
from googlesearch import search
import colorama
from colorama import Fore, Style
from urllib.parse import urlparse


# Define parser and arguments.
parser = argparse.ArgumentParser(description=f'{Fore.RED}{Style.BRIGHT}extraMetaPy{Style.RESET_ALL}: The Python3 powered {Fore.YELLOW}google{Style.RESET_ALL} dorking and metadata extracting tool. Presented by {Fore.MAGENTA}Jessi{Style.RESET_ALL}.')

parser.add_argument('-d', '--domain', help=f'Target domain {Fore.RED}{Style.BRIGHT}REQUIRED{Style.RESET_ALL} {Style.DIM}(Unless -u is supplied){Style.RESET_ALL}', default=None, required=False)
parser.add_argument('-o', '--output', help=f'Output file name {Style.DIM}OPTIONAL (Defualt: extracted_metadata.txt){Style.RESET_ALL}', default='extracted_metadata.txt', required=False)
parser.add_argument('-f', '--filedir', help=f'Downloads directory {Style.DIM}OPTIONAL (Default: file_downloads/){Style.RESET_ALL}', default='file_downloads/', required=False)
parser.add_argument('-l', '--limit', type=int, help=f'Results limit {Style.DIM}OPTIONAL (Default: 100){Style.RESET_ALL}', default=100, required=False)
parser.add_argument('-u', '--urllist', help=f'URL List (Skips Google Dork task) {Style.DIM}OPTIONAL{Style.RESET_ALL}', default=None, required=False)
parser.add_argument('-nd', '--nodownload', help=f'Scrape only, skip downloading and metedata extratction {Style.DIM}OPTIONAL (Ex: -nd y){Style.RESET_ALL}', default=None, required=False)

args = parser.parse_args()


# Set args to variables
domain = args.domain
output = args.output
filedir = args.filedir
limit = args.limit
urllist = args.urllist
nodownload = args.nodownload

# Create filedir if not exists
if not os.path.exists(filedir):
    os.makedirs(filedir)


# Define coloroma colors
GREEN = Fore.GREEN
RED = Fore.RED
WHITE = Fore.WHITE
CYAN = Fore.CYAN
PINK = Fore.MAGENTA
BRIGHT = Style.BRIGHT
DIM = Style.DIM
NORM = Style.NORMAL
RST = Style.RESET_ALL


# Display target domain
if not urllist:
    target = domain
else:
    urlData = open(urllist, 'r')
    urlContent = urlData.readlines()
    urlTarget = urlContent[1]
    target = urlparse(urlTarget).netloc
print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Target domain: {BRIGHT}{target}{RST}')


# Define fileTypes dictionary
fileTypes = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']


# Open urls.txt to write scraped urls to
if not urllist:
    f = open('urls.txt', 'a')


# Define primary functions
def dork(domain, ft): # Google Dork function
    query = 'site:' + domain + ' filetype:' + ft
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Dorking {BRIGHT}{domain}{RST} {WHITE}for {BRIGHT}{ft} {NORM}files{RST}')
    try:
        for result in search(query, num_results=limit):
            f.write(f'{result}\n')
    except:
        print(f'{RED}{BRIGHT}[X]{RST} {WHITE}Dork failed for: {BRIGHT}{ft}{RST}')
        print(f'{DIM}Failure is likely due to too many requests...')
        print(f'Try again later\n{RST}')


def download_url(url,filename): # Download files function
    try:
        r = urllib.request.urlretrieve(url,filename)
        print(f'{GREEN}{BRIGHT}[+]{NORM} {WHITE}Downloading: {BRIGHT}{url}{RST}')
    except urllib.error.HTTPError as exception:
        print(f'{RED}{BRIGHT}[x]{DIM} Download failed for:{RST} {WHITE}{url}{RST}')
    except urllib.error.ContentTooShortError as exception:
        print(f'{RED}{BRIGHT}[x]{DIM} Download failed for:{RST} {WHITE}{url}{RST}')


class ExifTool(object): # Define ExifTool class

    sentinel = "{ready}\n"

    def __init__(self, executable="/usr/bin/exiftool"):
        self.executable = executable

    def __enter__(self):
        self.process = subprocess.Popen(
            [self.executable, "-stay_open", "True",  "-@", "-"],
            universal_newlines=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return self

    def  __exit__(self, exc_type, exc_value, traceback):
        self.process.stdin.write("-stay_open\nFalse\n")
        self.process.stdin.flush()

    def execute(self, *args):
        args = args + ("-execute\n",)
        self.process.stdin.write(str.join("\n", args))
        self.process.stdin.flush()
        output = ""
        fd = self.process.stdout.fileno()
        while not output.endswith(self.sentinel):
            output += os.read(fd, 4096).decode('utf-8')
        return output[:-len(self.sentinel)]

    def get_metadata(self, file):
        return json.loads(self.execute("-G", "-j", "-n", file))


# Begin Google Dork task
if not urllist:
    print(f'{CYAN}{BRIGHT}[!] {NORM}{WHITE}Starting Google Dork task{RST}')
    time.sleep(2)
    for ft in fileTypes:
        dork(domain,ft)
else:
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}URL list supplied {BRIGHT}{urllist}{RST}')
    print(f'{CYAN}{BRIGHT}[!] {NORM}{WHITE}Skipping Google Dork task{RST}')
    time.sleep(2)


# Close urls.txt file and count urls scraped
if not urllist:
    f.close()
    urllist = 'urls.txt'
    urlsFile = open(urllist, 'r')
    urlsSum = sum(num is not None for num in urlsFile)
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Scraped {BRIGHT}{urlsSum}{NORM} URLs{RST}')
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Scraped URLs saved in {BRIGHT}urls.txt{RST}')
    if nodownload:
        exit(1)
else:
    urlsFile = open(urllist, 'r')
    urlsSum = sum(num is not None for num in urlsFile)
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Loaded {BRIGHT}{urlsSum}{NORM} URLs{RST}')


# Begin file download task
print(f'\n{CYAN}{BRIGHT}[!] {NORM}{WHITE}Starting files download task{RST}')
time.sleep(2)
with open(urllist) as urlsFile:
    for i in urlsFile:
        url = i.rstrip()
        name = url.rsplit('/', 1)[1]
        filename = filedir + name
        download_url(url,filename)


# Count downloaded files
dirCount = 0
dirListing = os.listdir(filedir)
for num in dirListing:
    if num:
        dirCount += 1
print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Downloaded {BRIGHT}{dirCount}{NORM} files to {BRIGHT}{filedir}{RST}')


# Extract metadata
print(f'\n{CYAN}{BRIGHT}[!] {NORM}{WHITE}Startig metadata extraction task{RST}')
time.sleep(2)
o = open(output, 'a')
with ExifTool() as e:
    for files in dirListing:
        file = filedir + files
        print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Extracting metadata for {BRIGHT}{files}{RST}')
        o.write(f'{RED}{BRIGHT}[*] {NORM}File: {WHITE}{BRIGHT}{files}{RST}\n')
        metadata = e.get_metadata(file)
        o.write(f'{metadata}\n\n')
o.close()
print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Extracted metadata written to {BRIGHT}{output}{RST}')
