import unittest
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker
import configparser
import datetime

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

DATABASE_URL = config['database']['url']
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

current_date = datetime.datetime.now().date()

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the table schema
        resource_id = config['api']['resource_id']
        cls.table_name = f'auction_results_{resource_id[:8]}'
        cls.table = Table(cls.table_name, metadata, autoload_with=engine)
        cls.session = SessionLocal()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_table_exists(self):
        inspector = inspect(engine)
        self.assertTrue(inspector.has_table(self.table_name), f"Table {self.table_name} does not exist")

    def test_record_format(self):
        # Fetch some records to test
        records = self.session.query(self.table).limit(10).all()
        for record in records:
            # Check if _id is an integer
            self.assertIsInstance(record._id, int, f"_id is not an integer in record {record}")
            # Check if deliveryStart is a datetime object
            self.assertIsInstance(record.deliveryStart, datetime.datetime, f"deliveryStart is not a datetime object in record {record}")
            # Check if deliveryEnd is a datetime object
            self.assertIsInstance(record.deliveryEnd, datetime.datetime, f"deliveryEnd is not a datetime object in record {record}")
            # Add more checks as needed for other fields...
            self.assertIsInstance(record.clearingPrice, float, f"clearingPrice is not a float in record {record}")

    def test_record_data(self):
        # Fetch some records to test
        records = self.session.query(self.table).limit(10).all()
        for record in records:
            # Check if deliveryStart and deliveryEnd are logical (e.g., deliveryStart should be before deliveryEnd)
            self.assertLess(record.deliveryStart, record.deliveryEnd, f"deliveryStart is not before deliveryEnd in record {record}")
            # Check if deliveryEnd is equal to the current date
            self.assertEqual(record.deliveryEnd.date(), current_date, f"deliveryEnd is not equal to the current date in record {record}")
            # Check specific business rules
            self.assertGreaterEqual(record.executedQuantity, 0, f"executedQuantity is negative in record {record}")

if __name__ == '__main__':
    unittest.main()
