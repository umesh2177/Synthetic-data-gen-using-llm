
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize Faker
fake = Faker()

# Define metadata
metadata = {
    'columns': ['Customer ID', 'First Name', 'Last Name', 'Age', 'Gender', 'Address', 'City', 'Contact Number', 'Email', 'Account Type', 'Account Balance', 'Date Of Account Opening', 'Last Transaction Date', 'TransactionID', 'Transaction Date', 'Transaction Type', 'Transaction Amount', 'Account Balance After Transaction', 'Branch ID', 'Loan ID', 'Loan Amount', 'Loan Type', 'Interest Rate', 'Loan Term', 'Approval/Rejection Date', 'Loan Status', 'CardID', 'Card Type', 'Credit Limit', 'Credit Card Balance', 'Minimum Payment Due', 'Payment Due Date', 'Last Credit Card Payment Date', 'Rewards Points', 'Feedback ID', 'Feedback Date', 'Feedback Type', 'Resolution Status', 'Resolution Date', 'Anomaly'],
    'num_rows': 5000,
    'num_columns': 40,
    'column_details': {
        'Customer ID': {'datatype': 'id', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'First Name': {'datatype': 'text', 'is_pii': True, 'date_format': None, 'unique_values': None, 'categories': None},
        'Last Name': {'datatype': 'text', 'is_pii': True, 'date_format': None, 'unique_values': None, 'categories': None},
        'Age': {'datatype': 'int64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Gender': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 3, 'categories': ['Male', 'Female', 'Other']},
        'Address': {'datatype': 'text', 'is_pii': True, 'date_format': None, 'unique_values': None, 'categories': None},
        'City': {'datatype': 'text', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Contact Number': {'datatype': 'int64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Email': {'datatype': 'text', 'is_pii': True, 'date_format': None, 'unique_values': None, 'categories': None},
        'Account Type': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 2, 'categories': ['Current', 'Savings']},
        'Account Balance': {'datatype': 'float64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Date Of Account Opening': {'datatype': 'date', 'is_pii': False, 'date_format': '%m/%d/%Y', 'unique_values': None, 'categories': None},
        'Last Transaction Date': {'datatype': 'date', 'is_pii': False, 'date_format': '%m/%d/%Y', 'unique_values': None, 'categories': None},
        'TransactionID': {'datatype': 'id', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Transaction Date': {'datatype': 'date', 'is_pii': False, 'date_format': '%d/%m/%Y', 'unique_values': None, 'categories': None},
        'Transaction Type': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 3, 'categories': ['Withdrawal', 'Deposit', 'Transfer']},
        'Transaction Amount': {'datatype': 'float64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Account Balance After Transaction': {'datatype': 'float64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Branch ID': {'datatype': 'id', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Loan ID': {'datatype': 'id', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Loan Amount': {'datatype': 'float64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Loan Type': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 3, 'categories': ['Mortgage', 'Auto', 'Personal']},
        'Interest Rate': {'datatype': 'float64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Loan Term': {'datatype': 'int64', 'is_pii': False, 'date_format': None, 'unique_values': 5, 'categories': None},
        'Approval/Rejection Date': {'datatype': 'date', 'is_pii': False, 'date_format': '%d/%m/%Y', 'unique_values': None, 'categories': None},
        'Loan Status': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 3, 'categories': ['Rejected', 'Approved', 'Closed']},
        'CardID': {'datatype': 'id', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Card Type': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 3, 'categories': ['AMEX', 'MasterCard', 'Visa']},
        'Credit Limit': {'datatype': 'float64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Credit Card Balance': {'datatype': 'float64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Minimum Payment Due': {'datatype': 'float64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Payment Due Date': {'datatype': 'date', 'is_pii': False, 'date_format': '%m/%d/%Y', 'unique_values': None, 'categories': None},
        'Last Credit Card Payment Date': {'datatype': 'date', 'is_pii': False, 'date_format': '%m/%d/%Y', 'unique_values': None, 'categories': None},
        'Rewards Points': {'datatype': 'int64', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Feedback ID': {'datatype': 'id', 'is_pii': False, 'date_format': None, 'unique_values': None, 'categories': None},
        'Feedback Date': {'datatype': 'date', 'is_pii': False, 'date_format': '%d/%m/%Y', 'unique_values': None, 'categories': None},
        'Feedback Type': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 3, 'categories': ['Suggestion', 'Complaint', 'Praise']},
        'Resolution Status': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 2, 'categories': ['Resolved', 'Pending']},
        'Resolution Date': {'datatype': 'date', 'is_pii': False, 'date_format': '%m/%d/%Y', 'unique_values': None, 'categories': None},
        'Anomaly': {'datatype': 'categorical', 'is_pii': False, 'date_format': None, 'unique_values': 2, 'categories': [1, -1]}
    }
}

# Generate synthetic data
data = {}
for column in metadata['columns']:
    column_details = metadata['column_details'][column]
    if column_details['datatype'] == 'id':
        data[column] = [fake.random_int(1000, 9999) for _ in range(metadata['num_rows'])]
    elif column_details['datatype'] == 'text':
        data[column] = [fake.name() if column in ['First Name', 'Last Name'] else fake.street_address() if column == 'Address' else fake.city() if column == 'City' else fake.email() if column == 'Email' else fake.text() for _ in range(metadata['num_rows'])]
    elif column_details['datatype'] == 'int64':
        data[column] = [fake.random_int(18, 80) if column == 'Age' else fake.random_int(100000, 999999) if column == 'Contact Number' else fake.random_int(100000, 999999) if column == 'Rewards Points' else fake.random_int(100000, 999999) for _ in range(metadata['num_rows'])]
    elif column_details['datatype'] == 'float64':
        data[column] = [
            fake.pyfloat(min_value=1000.0, max_value=9999.0) if column == 'Account Balance' else
             fake.pyfloat(min_value=1000.0, max_value=9999.0) if column == 'Transaction Amount' else 
             fake.pyfloat(min_value=1000.0, max_value=9999.0) if column == 'Loan Amount' else 
             fake.pyfloat(min_value=1000.0, max_value=9999.0) if column == 'Credit Limit' else 
             fake.pyfloat(min_value=1000.0, max_value=9999.0) if column == 'Credit Card Balance' else 
             fake.pyfloat(min_value=1000.0, max_value=9999.0) if column == 'Minimum Payment Due' else
             fake.pyfloat(min_value=1000.0, max_value=9999.0) for _ in range(metadata['num_rows'])]
            
    elif column_details['datatype'] == 'date':
        data[column] = [fake.date_between(start_date='-10y', end_date='today') for _ in range(metadata['num_rows'])]
    elif column_details['datatype'] == 'categorical':
        categories = column_details['categories']
        data[column] = [random.choice(categories) for _ in range(metadata['num_rows'])]

# Create pandas dataframe
df = pd.DataFrame(data)

# Print generated data
print(df.head(10))
df.to_json("synthetic_data_1.json", orient="records")
