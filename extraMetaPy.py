#!/usr/bin/env python3
# Title: extraMetaPy 2.0: The Python3 powered google dorking and metadata extracting tool.
# Author: Jessi
# Usage: extraMetaPy -d <domain> -o <output> -f <filedir> -l <results_limit> (Ex: extraMetaPy -d domain.com -o results.json -f downloads/ -l 150)
# REQUIRES EXIFTOOL INSTALLED (apt install libimage-exiftool-perl)

import sys
import apt
import os
import argparse
import time
import subprocess
import simplejson
import urllib.request
from googlesearch import search
import colorama
from colorama import Fore, Style
from urllib.parse import urlparse
from datetime import datetime


# Define colorama colors
GREEN = Fore.GREEN
RED = Fore.RED
WHITE = Fore.WHITE
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
PINK = Fore.MAGENTA
BRIGHT = Style.BRIGHT
DIM = Style.DIM
NORM = Style.NORMAL
RST = Style.RESET_ALL


# Error if no arguments and print example
if len(sys.argv) <= 1:
    print(f'{RED}{BRIGHT}extraMetaPy{RST}: The Python3 powered {YELLOW}google{RST} dorking and metadata extracting tool. Presented by {PINK}Jessi{RST}.\n')
    print(f'{RED}{BRIGHT}Error{DIM}: Either -d (--domain) or -u (--urllist) required.{RST}')
    print(f'{PINK}{BRIGHT}Example:{RED} extraMetaPy{NORM}{WHITE} -d domain.com -o domain_meta.json -f domain_files/ -l 75{RST}\n')
    print(f'{DIM}-h (--help) to see full usage and arguments.{RST}')
    print('\n')
    print(f'{DIM}Version: {RED}{BRIGHT}2.0{RST}')
    exit(1)


# Define parser and arguments.
parser = argparse.ArgumentParser(description=f'{RED}{BRIGHT}extraMetaPy - Version: 2.0{RST}: The Python3 powered {YELLOW}google{RST} dorking and metadata extracting tool. Presented by {PINK}Jessi{RST}.')

parser.add_argument('-d', '--domain', help=f'Target domain {RED}{BRIGHT}REQUIRED{RST} {DIM}(Unless -u is supplied){RST}', default=None, required=False)
parser.add_argument('-o', '--output', help=f'Output file name {DIM}OPTIONAL (Defualt: extracted_metadata.json){RST}', default='extracted_metadata.json', required=False)
parser.add_argument('-f', '--filedir', help=f'Downloads directory {DIM}OPTIONAL (Default: file_downloads/){RST}', default='file_downloads/', required=False)
parser.add_argument('-l', '--limit', type=int, help=f'Results limit {DIM}OPTIONAL (Default: 100){RST}', default=100, required=False)
parser.add_argument('-u', '--urllist', help=f'URL List (Skips Google Dork task) {DIM}OPTIONAL{RST}', default=None, required=False)
parser.add_argument('-nd', '--nodownload', help=f'Scrape only, skip downloading and metedata extratction {DIM}OPTIONAL (Ex: -nd){RST}', action='store_true', default=False, required=False)

args = parser.parse_args()


# Set args to variables
domain = args.domain
output = args.output
filedir = args.filedir
limit = args.limit
urllist = args.urllist
nodownload = args.nodownload


# Check for exiftool installed
cache = apt.Cache()
pkg = cache['libimage-exiftool-perl']
if not pkg.is_installed:
    if not nodownload:
        print(f'{RED}{BRIGHT}[X] {WHITE}exiftool{NORM} is not installed')
        exifInstall = input(f'Install {BRIGHT}exiftool{NORM}? (y/n){RST} ')
        if exifInstall == 'y':
            pkg.mark_install()
            try:
                cache.commit()
                print(f'{GREEN}{BRIGHT}[+] {WHITE}exiftool{NORM} installed, continuing')
                time.sleep(2)
            except:
                print(f'{RED}{BRIGHT}[X] {RST}{DIM}Failed to install {RST}{BRIGHT}exiftool{DIM}, try manually{RST}')
                exit(1)
        else:
            print(f'{BRIGHT}Google Dork mode{DIM} requires{RST} {BRIGHT}exiftool{DIM} installed')
            exit(1)


# Create logfile
timestamp = datetime.now().strftime("%H:%M:%S")
log = open(f'empy.log', 'a')
print(f'{CYAN}{BRIGHT}[!] {NORM}{WHITE}Log file: {BRIGHT}empy.log{RST}\n')
log.write(f'\n[*] Logging started at {timestamp}\n')


# Log: URL list or Google Dork mode
if urllist:
    log.write(f'{timestamp} Starting job in URL list mode\n')
else:
    log.write(f'{timestamp} Starting job in Google Dork mode\n')


# Create filedir if not exists
if not os.path.exists(filedir):
    os.makedirs(filedir)
    timestamp = datetime.now().strftime("%H:%M:%S")
    log.write(f"{timestamp} {filedir} doesn't exist, creating\n") # Log - filedir action


# Define target domain
if not urllist:
    target = domain
else:
    urlData = open(urllist, 'r')
    urlContent = urlData.readlines()
    if not urlContent: # If list is empty
        print(f'{RED}{BRIGHT}[X] {RST}{DIM}{urllist} is empty{RST}')
        exit(1)
    urlTarget = urlContent[0]
    target = urlparse(urlTarget).netloc


# Display target domain and request info
print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Target domain: {BRIGHT}{target}{RST}')
if not urllist:
    print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Max results per filetype: {BRIGHT}{limit}{RST}')
    totalResults = limit * 7
    print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Max results total: {BRIGHT}{totalResults}{RST}')
timestamp = datetime.now().strftime("%H:%M:%S")
log.write(f'{timestamp} Target set as {target}\n') # Log - target identificaiton
if nodownload:
    print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Downloads disabled{RST}\n')
    log.write(f'{timestamp} Downloads disabled\n')
else:
    print(f'{PINK}{BRIGHT}[*] {NORM}{WHITE}Downloads enabled{RST}\n')


# Define fileTypes dictionary
fileTypes = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']


# Open urls.txt to write scraped urls to
if not urllist:
    f = open('urls.txt', 'w+')


# Define primary functions
def dork(domain, ft): # Google Dork function
    timestamp = datetime.now().strftime("%H:%M:%S")
    log.write(f'{timestamp} Dorking {domain} for {ft} files\n')
    query = 'site:' + domain + ' filetype:' + ft
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Dorking {BRIGHT}{domain}{RST} {WHITE}for {BRIGHT}{ft} {NORM}files{RST}')
    try:
        for result in search(query, num_results=limit):
            f.write(f'{result}\n')
            timestamp = datetime.now().strftime("%H:%M:%S")
            log.write(f'{timestamp} Found {ft} file for {domain}\n')
    except:
        timestamp = datetime.now().strftime("%H:%M:%S")
        log.write(f'{timestamp} Dork failed for {domain} and {ft} (Too many requests, try again later)\n')
        print(f'{RED}{BRIGHT}[X]{RST} {WHITE}Dork failed for: {BRIGHT}{ft}{RST}')
        print(f'{DIM}Failure is likely due to too many requests...')
        print(f'Try again later\n{RST}')


def download_url(url,filename): # Download files function
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] # Set our download function to use Mozilla user-agent to avoid being blocked.
    urllib.request.install_opener(opener)
    for i in range(0,3):
        try:
            r = urllib.request.urlretrieve(url,filename)
            #print(f'{GREEN}{BRIGHT}[+]{NORM} {WHITE}Downloading: {BRIGHT}{url}{RST}')
        except urllib.error.HTTPError as exception:
            if i == 2:
                timestamp = datetime.now().strftime("%H:%M:%S")
                log.write(f'{timestamp} Download failed for {url} because: {exception}\n')
                print(f'{RED}{BRIGHT}[x]{DIM} Download failed for:{RST} {WHITE}{url}{RST} ({DIM}{exception}{RST})')
        except urllib.error.ContentTooShortError as exception:
            if i == 2:
                timestamp = datetime.now().strftime("%H:%M:%S")
                log.write(f'{timestamp} Download failed for {url} because: {exception}\n')
                print(f'{RED}{BRIGHT}[x]{DIM} Download failed for:{RST} {WHITE}{url}{RST} ({DIM}{exception}{RST})')
        except:
            if i == 2:
                timestamp = datetime.now().strftime("%H:%M:%S")
                log.write(f'{timestamp} Download failed for {url} because: Unknown\n')
                print(f'{RED}{BRIGHT}[x]{DIM} Download failed for:{RST} {WHITE}{url}{RST} ({DIM}Unknown error{RST})')
        else:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log.write(f'{timestamp} Downloaded {url}\n') # Log - Successful download
            print(f'{GREEN}{BRIGHT}[+]{NORM} {WHITE}Downloaded: {BRIGHT}{url}{RST}')
            break


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

    def get_metadata(self, filedir):
        #return self.execute("-Author", "-Creator", "-LastModifiedBy", file)
        o.write(simplejson.dumps(simplejson.loads(self.execute("-Author", "-Creator", "-LastModifiedBy", "-J", filedir)), indent=4, sort_keys=True))

# Begin Google Dork task
if not urllist:
    print(f'{CYAN}{BRIGHT}[!] {NORM}{WHITE}Starting Google Dork task{RST}')
    time.sleep(2)
    for ft in fileTypes:
        dork(domain,ft)
else:
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}URL list supplied: {BRIGHT}{urllist}{RST}')
    print(f'{CYAN}{BRIGHT}[!] {NORM}{WHITE}Skipping Google Dork task{RST}')
    time.sleep(2)


# Close urls.txt file and count urls scraped
urlsSum = 0
if not urllist:
    f.close()
    urllist = 'urls.txt'
    with open(urllist) as urls: # Open urllist temporarily to count
        for url in urls:
            if url.strip():
                urlsSum += 1
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Scraped {BRIGHT}{urlsSum}{NORM} URLs{RST}')
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Scraped URLs saved in {BRIGHT}urls.txt{RST}')
    if nodownload:
        timestamp = datetime.now().strftime("%H:%M:%S")
        log.write(f'[*] Logging stopped at {timestamp}\n') # Log - end
        log.close()
        exit(1)
else:
    with open(urllist) as urls: # Open urllist temporarily to count
        for url in urls:
            if url.strip():
                urlsSum += 1
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Loaded {BRIGHT}{urlsSum}{NORM} URLs{RST}')


# Begin file download task
print(f'\n{CYAN}{BRIGHT}[!] {NORM}{WHITE}Starting files download task{RST}')
time.sleep(2)

with open(urllist) as urls: # Open urllist temporarily to download files
    for i in urls:
        if i.strip():
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
o = open(output, 'w+')
with ExifTool() as e:
    timestamp = datetime.now().strftime("%H:%M:%S")
    log.write(f'{timestamp} Extracting metadata for {dirCount} files\n') # Log - start mdata extract
    #file = filedir + files
    print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Extracting metadata for {BRIGHT}{dirCount}{NORM} files{RST}')
    #o.write(f'{RED}{BRIGHT}[*] {NORM}File: {WHITE}{BRIGHT}{files}{RST}\n')
    e.get_metadata(filedir)
    #o.write(f'{metadata}\n\n')
    #o.write(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Extracting metadata for {BRIGHT}{files}{RST} | {metadata}\n\n')
    timestamp = datetime.now().strftime("%H:%M:%S")
    log.write(f'{timestamp} Metadata written for {dirCount} files\n') # Log - mdata write


# Close out output file
o.close()


# Remove filedir from output file
os.system(f"sed -i 's/{filedir}/' {output}")


# Prettify JSON output and display it in terminal
print('\n')
print(f'{CYAN}{BRIGHT}[!] {NORM}{WHITE}Prettifying JSON{RST}')
time.sleep(2)
print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}Extracted metadata results: {RST}')
os.system(f"cat {output} | jq")


# Output to CSV file
print('\n')
print(f'{CYAN}{BRIGHT}[!] {NORM}{WHITE}Creating CSV file for results {RST}')
os.system(f"cat {output} | jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' > {output}.csv")
os.system("""awk -F ',' '{print $4,$3,$2,$1}' """ + output +""".csv | sed 's/"//g' | sed 's/ /,/g' > tmp && mv tmp """+ output +""".csv""")
print(f'{GREEN}{BRIGHT}[+] {NORM}{WHITE}CSV file written{RST}')


# Close task
timestamp = datetime.now().strftime("%H:%M:%S")
log.write(f'[*] Logging stopped at {timestamp}\n') # Log - end
log.close()

print(f'{GREEN}{BRIGHT}[+] JSON {NORM}{WHITE}Extracted metadata written to {BRIGHT}{output}{RST}')
print(f'{GREEN}{BRIGHT}[+] CSV {NORM}{WHITE}Extracted metadata written to {BRIGHT}{output}.csv{RST}')
