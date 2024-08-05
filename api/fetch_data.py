import requests
import json
import configparser
from sqlalchemy import Integer, String, Float, DateTime, Boolean
from datetime import datetime 
from dateutil.parser import parse
import logging

def fetch_auction_results(participant_name):
    config = configparser.ConfigParser()
    config.read('config.ini')

    url = config['api']['eso_auction_results_url']
    resource_id = config['api']['resource_id']
    limit = config['api'].getint('limit') # to get all rows without limitation
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "resource_id": resource_id,
        "limit": limit,
        "filters": {
            "registeredAuctionParticipant": participant_name
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")
    
    response_dict = response.json()
    if not response_dict.get('success', False):
        error_message = response_dict.get('error', {}).get('message', 'Unknown error')
        raise Exception(f"API Error: {error_message}")
    
    return response_dict['result']['records']

def filter_results(records):
    """
    Filter records to include only those for the current day based on the deliveryStart field.

    Parameters:
    records (list): List of records to be filtered.

    Returns:
    list: Filtered records for the current day.
    """
    current_date = datetime.now().date()
    filtered_records = []

    for record in records:
        try:
            delivery_start = datetime.fromisoformat(record['deliveryStart']).date()
            if delivery_start == current_date:
                filtered_records.append(record)
        except Exception as e:
            logging.error(f"Error processing record {record}: {e}")
    
    return filtered_records

def is_datetime(value):
    try:
        parse(value)
        return True
    except (ValueError, TypeError):
        return False

def detect_fields(records):
    if not records:
        return []
    
    field_types = {}
    
    for record in records:
        for key, value in record.items():
            if key not in field_types:
                if isinstance(value, int):
                    field_types[key] = Integer
                elif isinstance(value, float):
                    field_types[key] = Float
                elif isinstance(value, bool):
                    field_types[key] = Boolean
                elif isinstance(value, str) and is_datetime(value):
                    field_types[key] = DateTime
                elif isinstance(value, str):
                    field_types[key] = String
                else:
                    field_types[key] = String  # Default to String for any unknown types
    
    return field_types