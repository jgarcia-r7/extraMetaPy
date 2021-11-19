# extraMetaPy 2.0
The Python3 powered google dorker and metadata extractor.  
Use Google Dorks against a target domain to scrape URLs containing common filetypes. Download files from scraped URLs. Extract metadata from files into a pretty JSON output file and formatted CSV file.  

### NOTE: REQUIRES EXIFTOOL INSTALLED (apt install libimage-exiftool-perl)  

### About
extraMetaPy has two main modes: Google Dork mode or URL list mode.  
Google Dork mode: Designated by setting the `-d (--domain)` argument to a valid domain name.
- In this mode, extraMetaPy will use Google Dorks to scan a domain for common file types, it will then scrape them into a file called 'urls.txt', then it will proceed to download all of the files, unless `-nd (--nodownload)` is set, finally, it will extract all of the metadata from the files into an output file.  

URL list mode: Designated by setting the `-u (--urllist)` argument to a valid list of URLs.  
- In this mode, extraMetaPy will read an existing list of URLs, skipping Google Dorks as a result, then proceed with the standard process of downloading the files and extracting their metadata.  

Errors?  
- extraMetaPy creates a log file called `empy.log` by default, it will timestamp relative logs and information into the log, along with exceptions.  
- extraMetaPy will attempt to download a file a maximum of three times before it counts it as failed, but it will continue down the list and download the rest of the files.  
- extraMetaPy will also print out an error if an issue is detected when attempting a Google Dork, this error is usually not because of the tool, but rather because Google has detected you have been making too many requests.  

#### Usage
```bash
git clone https://github.com/jessisec/extraMetaPy
cd extraMetaPy
chmod +x install.sh
./install.sh

extraMetaPy -d <domain>
Ex: extraMetaPy -d yahoo.com -o yahoo_meta.json -f files/ -l 50
```


#### Screenshots  
Installing:  
![image](https://user-images.githubusercontent.com/28818635/142551732-86bb11f8-03e1-4f7e-b169-c0b554da2fe4.png)
 
 Example: Google Dork mode  
![image](https://user-images.githubusercontent.com/28818635/142552157-7982b81f-af5f-40af-9738-ba59c9832f80.png)

Example: URL list mode with errors  
![image](https://user-images.githubusercontent.com/28818635/142552265-4f406018-5417-4ecb-b63e-9870d34b270e.png)
