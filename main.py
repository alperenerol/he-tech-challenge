import logging
from datetime import datetime
import configparser

from api.fetch_data import fetch_auction_results, detect_fields
from db.dynamic_schema import create_dynamic_table, save_results

# Configure logging
logging.basicConfig(filename='errors.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
participant_name = config['api'].get('participant_name')
current_date = datetime.now().date()

def main():
    try:
        results = fetch_auction_results(participant_name)
        fields = detect_fields(results)
        auction_results_table = create_dynamic_table(fields)
        save_results(results, auction_results_table)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()