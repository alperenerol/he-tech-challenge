from api.fetch_data import fetch_auction_results, filter_results, detect_fields
from db.dynamic_schema import create_dynamic_table, save_results
from datetime import datetime 

if __name__ == "__main__":

    current_date = datetime.now().date()
    participant_name = "HABITAT ENERGY LIMITED"

    try:
        results = fetch_auction_results(participant_name)
        fields = detect_fields(results)
        current_date_results = filter_results(results)
        auction_results_table = create_dynamic_table(fields)
        save_results(current_date_results, auction_results_table)
        
    except Exception as e:
        print(f"An error occurred: {e}")