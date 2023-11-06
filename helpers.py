import os, requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET 

load_dotenv()

def get_url(method: str, **kwargs):
    rest_url = 'https://services.datafordeler.dk/BBR/BBRPublic/1/rest/'
    request = rest_url + method +'?'
    username = 'username=' + os.getenv('USER')
    password = 'password=' + os.getenv('PASSWORD')
    
    inputparams = ["=".join(map(str,item)) for item in kwargs.items()]

    return '&'.join([request,*inputparams,username, password])

def load(method: str, **kwargs):
    url = get_url(method=method, **kwargs)
    
    resp = requests.get(url)
    
    with open('test.xml','wb') as f:
        f.write(resp.content) # TODO: Why is it not getting the right XML content from the HTTP response?

def parseXML(xml_file):
    # Not necessary before load() has been fixed
    pass
    

if __name__ == '__main__': 
    print("lol")
    print(load('bygning',Kommunekode='0173'))
    parseXML('test.xml')