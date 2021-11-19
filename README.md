# extraMetaPy 2.0
### Changelog 11/19/21
- Changed output format to pretty JSON.
- Added CSV export function.
- Added socks5 proxy support.
- Fixed logic error in `-nd` function.  
### Requirements Error  
If you get the following error:
```bash
ERROR: Could not find a version that satisfies the requirement python_apt==2.3.0+b1 (from versions: 0.0.0, 0.7.8)
ERROR: No matching distribution found for python_apt==2.3.0+b1
```
Try installing the 'python_apt' package manually:  
```bash
pip3 install python_apt
```
  
### Description
The Python3 powered google dorker and metadata extractor.  
Use Google Dorks against a target domain to scrape URLs containing common filetypes. Download files from scraped URLs. Extract metadata from files into a pretty JSON output file and formatted CSV file.  

### NOTE: REQUIRES EXIFTOOL INSTALLED (apt install libimage-exiftool-perl)  

### About
extraMetaPy has two main modes: Google Dork mode or URL list mode.  
Google Dork mode: Designated by setting the `-d (--domain)` argument to a valid domain name.
- In this mode, extraMetaPy will use Google Dorks to scan a domain for common file types, it will then scrape them into a file called 'urls.txt', then it will proceed to download all of the files, unless `-nd (--nodownload)` is set, finally, it will extract all of the metadata from the files into an output file.  

URL list mode: Designated by setting the `-u (--urllist)` argument to a valid list of URLs.  
- In this mode, extraMetaPy will read an existing list of URLs, skipping Google Dorks as a result, then proceed with the standard process of downloading the files and extracting their metadata. 

### socks5 Proxy Support
Added on 11/19/21, extraMetaPy can now be used through a socks5 proxy:  
Using the `-s` parameter and specifying an IP for a socks5 proxy will enable proxy mode and will route all traffic, including the Google dorks and download requests through that proxy. The `-sp` parameter can be used to modify the default port `1080` that socks5 uses.  

Errors?  
- extraMetaPy creates a log file called `empy.log` by default, it will timestamp relative logs and information into the log, along with exceptions.  
- extraMetaPy will attempt to download a file a maximum of three times before it counts it as failed, but it will continue down the list and download the rest of the files.  
- extraMetaPy will also print out an error if an issue is detected when attempting a Google Dork, this error is usually not because of the tool, but rather because Google has detected you have been making too many requests.  

#### Usage
```bash
git clone https://github.com/jgarcia-r7/extraMetaPy
cd extraMetaPy
chmod +x install.sh
./install.sh

extraMetaPy -d <domain>
Ex: extraMetaPy -d yahoo.com -o yahoo_meta.json -f files/ -l 50
```


#### Screenshots  
Installing:  
![image](https://user-images.githubusercontent.com/28818635/142633168-c816f209-3bad-4402-bf3b-fff55b08cd11.png)  
 
 Example: Google Dork mode (w/ socks5 proxy)  
![image](https://user-images.githubusercontent.com/28818635/142634893-449bea4a-e61b-49cc-8fad-a15928104f29.png)  

Example: URL list mode with errors  
![image](https://user-images.githubusercontent.com/28818635/142635072-3688762d-1bc3-4e0b-a0b8-21abb8e1aaf1.png)  

Example: JSON output  
![image](https://user-images.githubusercontent.com/28818635/142635257-be2cb2a0-d98b-4fbf-9a35-ecd55b4da46d.png)  

