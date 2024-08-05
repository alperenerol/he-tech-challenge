# Habitat Energy Data Processing

This project fetches data from the National Grid ESO API, processes it, and stores it in a local database. It is designed to handle dynamic data structures.

## Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd habitat_energy
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

## Logs

Errors are logged in the `errors.log` file.

## Project Structure
# Main Script (main.py)

    Entry point of the application.
    Fetches data, detects fields, creates/loads tables, and saves results.

# Configuration (config.ini)

    Contains database and API configuration settings.

# API Module (api/fetch_data.py)

    Contains the function to fetch data from the National Grid ESO API.

# Database Module (db/dynamic_schema.py)

    Contains functions for dynamic table creation, field detection, date conversion, and data saving.

# Requirements (requirements.txt)

    Lists the Python dependencies required for the project.

# README (README.md)

    Provides instructions on setting up and running the project.

# Logging (errors.log)

    Captures errors encountered during execution.

# Example Usage

    Fetch auction results from the API.
    Detect fields in the fetched data.
    Create or load a dynamic table based on the detected fields.
    Save the results into the database without duplication.