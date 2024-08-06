import requests
import json
import configparser
from sqlalchemy import Integer, String, Float, DateTime, Boolean
from datetime import datetime 
from dateutil.parser import parse
import logging

# Configure logging
logging.basicConfig(filename='logs.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Read configuration once
config = configparser.ConfigParser()
config.read('config.ini')
API_URL = config['api']['eso_auction_results_url']
RESOURCE_ID = config['api']['resource_id']
LIMIT = config['api'].getint('limit')  # default to 100 if not specified in config.ini

def filter_results(records):
    """
    Filter records to include only those for the current day based on the deliveryEnd field.

    Parameters:
    records (list): List of records to be filtered.

    Returns:
    list: Filtered records for the current day.
    """
    current_date = datetime.now().date()
    filtered_records = []

    for record in records:
        try:
            delivery_start = datetime.fromisoformat(record['deliveryEnd']).date()
            if delivery_start == current_date:
                filtered_records.append(record)
        except Exception as e:
            logging.error(f"Error processing record {record}: {e}")
    
    return filtered_records

def fetch_auction_results(participant_name):
    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            "resource_id": RESOURCE_ID,
            "limit": LIMIT,
            "filters": {
                "registeredAuctionParticipant": participant_name
            }
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

        response_dict = response.json()
        if not response_dict.get('success', False):
            error_message = response_dict.get('error', {}).get('message', 'Unknown error')
            raise Exception(f"API Error: {error_message}")

        return filter_results(response_dict['result']['records'])
    
    except requests.RequestException as e:
        logging.error(f"Network error occurred while fetching auction results: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error occurred while fetching auction results: {e}")
    except Exception as e:
        logging.error(f"An error occurred while fetching auction results: {e}")
    
    return []

def is_datetime(value):
    """
    Check if a given value is a datetime string.

    Parameters:
    value (str): The value to check.

    Returns:
    bool: True if the value is a datetime string, False otherwise.
    """
    if len(value) < 10:  # ISO 8601 format is at least 10 characters long (YYYY-MM-DD)
        return False
    
    try:
        parse(value)
        return True
    except (ValueError, TypeError):
        return False

def detect_fields(records):
    """
    Detect the fields and their types in the records.

    Parameters:
    records (list): List of records to detect fields from.

    Returns:
    dict: Dictionary with field names as keys and SQLAlchemy types as values.
    """
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