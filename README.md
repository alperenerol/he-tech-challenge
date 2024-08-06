# Habitat Energy Data Processing

This project involves fetching auction results data from the National Grid ESO API, processing it, and saving it to a local SQLite database. The data includes results for Habitat Energy's participation in the Dynamic Frequency Response (DFR) auction.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Logging](#logging)
- [Example Usage](#example-usage)
- [License](#license)

## Project Structure

habitat_energy/
│
├── main.py
├── config.ini
├── requirements.txt
├── README.md
├── logs.log
├── habitat_env/
├── auction_results.db
│
├── api/
│   ├── fetch_data.py
│
├── db/
│   ├── dynamic_schema.py
│
├── tests/
│   ├── test_fetch_data.py
│   ├── test_database.py

### main.py

- Entry point of the application.
- Fetches data, detects fields, creates/loads tables, and saves results.

### config.ini

- Contains database and API configuration settings.

### api/fetch_data.py

- Functions to fetch data from the National Grid ESO API.
- Filters and processes the fetched data.

### db/dynamic_schema.py

- Functions to dynamically create tables, convert dates, and save records.

### tests/test_fetch_data.py

- Unit tests for fetching auction results.

### tests/test_database.py

- Unit tests for database operations and schema validation.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- SQLite

### Installation
1. Change directory to the repo directory:
    ```bash
    cd he-tech-challenge
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv habitat_env
    source habitat_env/bin/activate  # On Windows use `habitat_env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the main script:
    ```bash
    python main.py
    ```

## Configuration

The `config.ini` file contains the configuration for the database and the API.

## Modules

- **api/**: Contains the module for fetching data from the API.
- **db/**: Contains modules for dynamic database schema creation and data saving.
- **tests/**: Contains unit tests.

## Logs

Logs are saved to logs.log file.
Check this file for detailed information about the execution and any errors encountered.

## Usage
Run the main script:
    ```bash
    python main.py
    ```
This script will fetch the auction results, process the data, and save it to the SQLite database.

## Testing

    Run the tests:
    ```bash
    python -m unittest tests/test_fetch_data.py   
    python -m unittest tests/test_database_schema.py
    ```

# Example Usage

Fetch auction results from the API:

    The fetch_auction_results function retrieves data from the specified API endpoint.

Detect fields in the fetched data:

    The detect_fields function analyzes the data and determines the schema.

Create or load a dynamic table based on the detected fields:

    The create_dynamic_table function dynamically creates a table schema.

Save the results into the database without duplication:

    The save_results function inserts the data into the database, ensuring no duplicate entries.