
import requests
import getpass
from pyarrow import flight
from pyarrow.flight import FlightClient
import time
import requests
import json
import time
import urllib3
from datetime import datetime
import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()


def get_nni():
    nni = getpass.getpass(prompt="NNI ?")
    password = getpass.getpass(prompt="password ?")
    return nni, password


def get_token():

    url = os.getenv("DREMIO_URL")
    cert_path = os.getenv("CERT_PATH")
    dremio_username = os.getenv("DREMIO_USERNAME")
    dremio_password = os.getenv("DREMIO_PASSWORD")

    # Verification of the certificate, else False
    if cert_path:
        cert = Path(cert_path)
        verify = cert_path if cert.is_file() else False 
    else:
        verify = False

    # Get NNI and password 
    try:
        username = dremio_username
        password = dremio_password 
        
        payload = {'userName': username, 'password': password}
        
         # First login attempt
        response = requests.post(f"{url}/apiv2/login", json=payload, verify=verify) 

        if response.status_code == 200:
            pass
        else:
            username, password = get_nni()
            payload = {'userName': username, 'password': password}

            #Second login attempt
            response = requests.post(f"{url}/apiv2/login", json=payload, verify=verify) 

        if response.status_code != 200:
            raise ValueError("Authentication failed")
        
    except Exception as e:
        print("Error:", str(e))
        return None, None
   
    # Parse the JSON response
    data = response.json()
    token = data.get("token", "") #Extract the token 
    expires = data.get("expires", 0)/1000 # Expiration time in secondes 
    expiration = datetime.fromtimestamp(expires).strftime("%m/%d/%Y at %I:%M:%S")
    time_left = datetime.fromtimestamp(expires) - datetime.today()
    days = time_left.days
    seconds = time_left.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    print(f"Token aquired, it will expire on {expiration}")
    print(f"Time remaining : {days} days, {hours} hours, {minutes} minutes")

    return token, expires 


def get_results(query, token):
    try:
        token = token[0]
        location = os.getenv("DREMIO_LOCATION")
        headers = [(b"authorization", f"bearer {token}".encode("utf-8"))]
        client = flight.FlightClient(location=location, disable_server_verification=False)
        options = flight.FlightCallOptions(headers=headers)
        flight_info = client.get_flight_info(flight.FlightDescriptor.for_command(query), options)
        if not flight_info.endpoints:
            raise ValueError("No data returned by the query.")
    
        results = client.do_get(flight_info.endpoints[0].ticket, options)
        df = results.read_pandas()
        if not df:
            print("No results found for the query.")
            return pd.DataFrame()
    
        return df
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return pd.DataFrame()


def time_left(token):
    expires = token[1]
    expiration = datetime.fromtimestamp(expires).strftime("%B %d, %Y at %I:%M:%S")
    time_left = datetime.fromtimestamp(expires) - datetime.today()
    days = time_left.days
    seconds = time_left.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    print(f"It will expire on {expiration}")
    print(f"Time remaining : {days} days, {hours} hours, {minutes} minutes")


def get_metadata(path, token):
    url = os.getenv("DREMIO_URL")
    cert_path = os.getenv("CERT_PATH")

    # Verification of the certificate, else False
    if cert_path:
        cert = Path(cert_path)
        verify = cert_path if cert.is_file() else False
    else:
        verify = False

    # request to get the id
    headers = {"Authorization": f"_dremio{token[0]}"}
    path_str = "/".join(path)
    try:
        res = requests.get(f"{url}/api/v3/catalog/by-path/{path_str}", headers=headers, verify=verify)
        info = res.json()
        table_id = info["id"]
    except:
        print("Error retrieving table id, check the path")
    
    # Print type 
    type = info['type']
    print("Type :", type)

    # request to get the tag 
    try:
        restag = requests.get(f"{url}/api/v3/catalog/{table_id}/collaboration/tag", headers=headers, verify=verify)
        tag = restag.json()["tags"]
        if not tag:
            print("No tag")
        else:            
            print("Tag :", tag)
    except:
        print("Failed to retrieve the tag")

    #request to get the wiki
    try:
        reswiki = requests.get(f"{url}/api/v3/catalog/{table_id}/collaboration/wiki", headers=headers, verify=verify)
        wiki = reswiki.json()['text']
        if not wiki:
            print("No wiki")
        else:
            print("Wiki :", wiki)
    except:
        print("Failed to retrieve the wiki")
    



