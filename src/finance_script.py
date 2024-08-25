import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('data/financial_data.csv', header=None, delimiter="\t")

# Assign custom column names
df.columns = ['PRICE', 'COMPANY', 'DATE', 'DESCRIPTION']

# Convert the 'DATE' column to datetime
df['DATE'] = pd.to_datetime(df['DATE'])

df['PRICE'] = df['PRICE'].str.replace('$', '').str.replace(',', '').astype(float)

# Create a new column for year-month
df['YearMonth'] = df['DATE'].dt.to_period('M')

df['SPENDING'] = df['PRICE'].apply(lambda x: x if x < 0 else None)
df['EARNING'] = df['PRICE'].apply(lambda x: x if x > 0 else None)

# Group by the YearMonth and sum up the prices
monthly_spending = df.groupby('YearMonth')['SPENDING'].sum()
monthly_earnings = df.groupby('YearMonth')['EARNING'].sum()

def plot_monthly_spending():
    # Plot the data
    plt.figure(figsize=(12, 6))
    monthly_spending.plot(kind='bar')
    plt.title('Monthly Spending')
    plt.xlabel('Month')
    plt.ylabel('Total Spending ($)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_monthly_earning():
    # Plot the data
    plt.figure(figsize=(12, 6))
    monthly_earnings.plot(kind='bar')
    plt.title('Monthly Earning')
    plt.xlabel('Month')
    plt.ylabel('Total Earning ($)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_both_monthly_earning_and_spending():
    monthly_summary = df.groupby('YearMonth').agg({'SPENDING': 'sum', 'EARNING': 'sum'})

    # Convert PeriodIndex to string for plotting
    monthly_summary.index = monthly_summary.index.astype(str)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.bar(monthly_summary.index, monthly_summary['EARNING'], color='green', label='Earnings')
    plt.bar(monthly_summary.index, monthly_summary['SPENDING'], color='red', label='Spending')

    plt.title('Monthly Earnings and Spending')
    plt.xlabel('Month')
    plt.ylabel('Amount ($)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, axis='y')
    plt.tight_layout()

    # Show the plot
    plt.show()

plot_both_monthly_earning_and_spending()