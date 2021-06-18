# extraMetaPy
The Python3 powered google dorking and metadata extraction tool.

### About
extraMetaPy has two main modes: Google Dork mode or URL list mode.  
Google Dork mode: Designated by setting the `-d (--domain)` argument to a valid domain name.
- In this mode, extraMetaPy will use Google Dorks to scan a domain for common file types, it will then scrape them into a file called 'urls.txt', then it will proceed to download all of the files, unless `-nd y (--nodownload y)` is set, finally, it will extract all of the metadata from the files into an output file.  

URL list mode: Designated by setting the `-u (--urllist)` argument to a valid list of URLs.  
- In this mode, extraMetaPy will read an existing list of URLs, skipping Google Dorks as a result, then proceed with the standard process of downloading the files and extracting their metadata.  

Errors?  
- extraMetaPy creates a log file called `empy.log` by default, it will timestamp relative logs and information into the log, along with exceptions.  
- extraMetaPy will attempt to download a file a maximum of three times before it counts it as failed, but it will continue down the list and download the rest of the files.  
- extraMetaPy will also print out an error if an issue is detected when attempting a Google Dork, this error is usually not because of the tool, but rather because Google has detected you have been making too many requests.  

#### Usage  
```bash
git clone https://github.com/jgarcia-r7/extraMetaPy
cd extraMetaPy
pip3 install -r requirements.txt

./extraMetaPy.py -d <target_domain> -o <output_file> -f <file_dir> -l <rate_limit>
Ex: ./extraMetaPy.py -d domain.com -o domain_meta.txt -f domain_files/ -l 150
```

## Screenshots  
**Arguments**  
![image](https://user-images.githubusercontent.com/81575551/122490925-04b40600-cfb1-11eb-91ac-d0ebff57da12.png)

**In-Use Example**   
![image](https://user-images.githubusercontent.com/81575551/122491101-65dbd980-cfb1-11eb-8c3e-d4595473eef8.png)  

![image](https://user-images.githubusercontent.com/81575551/122491276-adfafc00-cfb1-11eb-9b37-bc8163bf7e9b.png)

**Current Extracted Metadata Format (WIP)**  
![image](https://user-images.githubusercontent.com/81575551/122439670-db23bc00-cf69-11eb-85d1-408cce24a6e3.png)
