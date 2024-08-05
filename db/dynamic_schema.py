from sqlalchemy import create_engine, MetaData, Table, Column, Integer, inspect
from sqlalchemy.orm import sessionmaker
import datetime
import configparser
import logging

# Configure logging
logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
resource_id = config['api']['resource_id']
table_name = f'auction_results_{resource_id[:8]}'

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

    return dynamic_table

def convert_dates(record):
    """
    Convert string dates in the record to datetime objects.

    Parameters:
    record (dict): The record containing data to be inserted.

    Returns:
    dict: The record with dates converted to datetime objects.
    """
    for key in ['deliveryStart', 'deliveryEnd', 'orderEntryTime']:
        if key in record and isinstance(record[key], str):
            try:
                record[key] = datetime.datetime.fromisoformat(record[key])
            except ValueError as e:
                logging.error(f"Error converting date for record {record}: {e}")
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
                db.execute(ins)
            except Exception as e:
                logging.error(f"Error inserting record {record}: {e}")
    db.commit()
    db.close()