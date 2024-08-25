import pandas as pd

# Load the CSV file
df = pd.read_csv('financial_history.csv')

# Convert the 'DATE' column to datetime
df['DATE'] = pd.to_datetime(df['DATE'])

# Filter data for a specific month and year
year = 2024
month = 8
filtered_df = df[(df['DATE'].dt.year == year) & (df['DATE'].dt.month == month)]

# Calculate the total expenditure
total_spent = filtered_df['PRICE'].sum()

print(f"Total spent in {month}/{year}: ${total_spent}")
