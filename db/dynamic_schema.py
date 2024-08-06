from sqlalchemy import create_engine, MetaData, Table, Column, Integer, inspect
from sqlalchemy.orm import sessionmaker
import datetime
from dateutil.parser import parse
import configparser
import logging

from utils.utils import is_datetime

# Configure logging
logging.basicConfig(filename='logs.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
RESOURCE_ID = config['api']['resource_id']
table_name = f'auction_results_{RESOURCE_ID[:8]}'

# Database setup
DATABASE_URL = config['database']['url']
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

def create_dynamic_table(fields):
    """
    Create a new table with the given fields if it doesn't already exist.

    Parameters:
    fields (dict): Dictionary of field names and SQLAlchemy field types.
    table_name (str): The name of the table to be created.

    Returns:
    sqlalchemy.Table: The created or existing table.
    """
     
    # Check if the table already exists
    if not inspect(engine).has_table(table_name):
        # Create the columns for the new table
        columns = [Column('id', Integer, primary_key=True, index=True)]
        for field_name, field_type in fields.items():
            columns.append(Column(field_name, field_type))
        
        # Define the table with the metadata
        dynamic_table = Table(table_name, metadata, *columns)
        metadata.create_all(engine)  # Create the table in the database
    else:
        # Load the existing table
        dynamic_table = Table(table_name, metadata, autoload_with=engine)
        logging.info(f"Table {table_name} already exists, loaded existing table schema.")

    return dynamic_table
    
def convert_dates(record):
    """
    Convert string dates in the record to datetime objects.

    Parameters:
    record (dict): The record containing data to be inserted.

    Returns:
    dict: The record with dates converted to datetime objects.
    """
    for key, value in record.items():
        if isinstance(value, str) and is_datetime(value):
            try:
                record[key] = datetime.datetime.fromisoformat(value)
            except ValueError as e:
                logging.error(f"Error converting date for field {key} in record {record}: {e}")
                raise
    return record

def save_results(records, table):
    """
    Save the given records to the specified table.

    Parameters:
    records (list): List of records to be inserted.
    table (sqlalchemy.Table): The table to insert records into.
    """
    db = SessionLocal()
    for record in records:
        # Check if the record already exists to avoid duplication
        if not db.query(table).filter_by(_id=record['_id']).first():
            try:
                record = convert_dates(record)  # Convert date strings to datetime objects
                ins = table.insert().values(**record)
                db.execute(ins)  # Execute the insert statement
                logging.info(f"Inserted record {record}")
            except Exception as e:
                logging.error(f"Error inserting record {record}: {e}")
                logging.error(f"Record causing error: {record}")
    db.commit()
    logging.info(f"Committed all records to table {table.name}")
    db.close()