# extraMetaPy
The Python3 powered google dorking and metadata extraction tool.

#### Usage  
```bash
git clone https://github.com/jgarcia-r7/extraMetaPy
cd extraMetaPy
pip3 install -r requirements.txt

./extraMetaPy.py -d <target_domain> -o <output_file> -f <file_dir> -l <rate_limit>
Ex: ./extraMetaPy.py -d domain.com -o domain_meta.txt -f domain_files/ -l 150
```

#### Screenshots  
**Arguments**  
![image](https://user-images.githubusercontent.com/81575551/122490925-04b40600-cfb1-11eb-91ac-d0ebff57da12.png)

**In-Use Example**   
![image](https://user-images.githubusercontent.com/81575551/122491101-65dbd980-cfb1-11eb-8c3e-d4595473eef8.png)  

![image](https://user-images.githubusercontent.com/81575551/122491276-adfafc00-cfb1-11eb-9b37-bc8163bf7e9b.png)

**Current Extracted Metadata Format (WIP)**  
![image](https://user-images.githubusercontent.com/81575551/122439670-db23bc00-cf69-11eb-85d1-408cce24a6e3.png)
