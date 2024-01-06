#
# This script needs transaction report from fidelity
# It will add 3 columns to the report. closing price, profit/loss, profit/loss %
# Report can be of last 7 days, 30days or x days
import pandas as pd
import requests
import time
import argparse

# Polygon.io API key. Here its my free account key (bsrinivasa). Only 5 REST API calls per min allowed, hence 1min delay after polling 5 symbols
api_key = 'j6SIzVk6DtprIxAnmRPr2h6GRBduN75C'

# Function to calculate profit or loss
def calculate_profit_loss(row):
    closing_price = row['Closing Price']
    quantity = row['Quantity']
    purchase_price = row['Price ($)']
    if pd.notna(closing_price):
        current_value = closing_price * quantity
        cost_basis = purchase_price * quantity
        return current_value - cost_basis
    return None

# Function to calculate profit or loss percentage and round to integer
def calculate_profit_loss_percentage(row):
    profit_loss = row['Profit/Loss']
    if pd.notna(profit_loss):
        cost_basis = row['Price ($)'] * row['Quantity']
        profit_loss_percent = (profit_loss / cost_basis) * 100
        return round(profit_loss_percent)  # Round to the nearest integer
    return None

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Update Excel file with stock closing prices and calculate profit/loss.')
parser.add_argument('excel_file', help='Path to the Excel file to update')
args = parser.parse_args()

# Load the Excel file into a DataFrame
excel_file = args.excel_file
df = pd.read_excel(excel_file)

# Define the base URL for the Polygon.io API
base_url = 'https://api.polygon.io/v2/aggs/ticker/'

# Counter to keep track of symbols processed
symbol_counter = 0

# Iterate through the symbols in the "Symbol" column
for i, symbol in enumerate(df['Symbol'], 1):
    # Define the stock symbol
    stock_symbol = symbol.strip()

    print("Checking Symbol:", stock_symbol)

    # Build the URL for the API request
    url = f'{base_url}{stock_symbol}/prev?adjusted=true'

    params = {"apiKey": api_key}

    # Define the Authorization header with your API key
    headers = {'Authorization': f'Bearer {api_key}'}

    # Make the API request with the Authorization header
    response = requests.get(url, params=params, headers=headers)
    print("URL is:", url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the closing price from the response
        closing_price = data['results'][0]['c']
        print("Closing Price of %s is %f" % (stock_symbol, data['results'][0]['c']))

        # Add a new column "Closing Price" to the DataFrame for the current symbol
        df.at[i - 1, 'Closing Price'] = closing_price

        # Calculate profit or loss and add a new column "Profit/Loss" to the DataFrame
        df.at[i - 1, 'Profit/Loss'] = calculate_profit_loss(df.iloc[i - 1])

        # Calculate profit or loss percentage and add a new column "Profit/Loss %" to the DataFrame
        df.at[i - 1, 'Profit/Loss %'] = calculate_profit_loss_percentage(df.iloc[i - 1])

        # Increment the symbol counter
        symbol_counter += 1

        # Delay for 1 minute after every 5 symbols
        if symbol_counter % 5 == 0:
            print("Waiting for 1 minute...")
            time.sleep(60)  # Sleep for 60 seconds (1 minute)

# Save the updated DataFrame back to the Excel file
df.to_excel(excel_file, index=False)
