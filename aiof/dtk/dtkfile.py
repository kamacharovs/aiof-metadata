#Assumptions made:
    #User inputs everything in the beginning/first time
    #Upon review:
        #if any changes to cashflow in or out, what changed? Amount, frequency, etc. would be user inputs
        #user has to input final asset value (e.g., upon review date, has to input current balance for savings account)
        #user does not need to input liabilities balance
        #if non-recurring contribution/payment has been made, user has to input amount for both assets and liabilities
        #once changes to existing Personal Financial Statement (Cashflow and Balance Sheet) have been discussed, address any new additions (if any)
import pandas as pd
import numpy as np

def main():
    #frequencies
    weekly = 52
    bi_weekly = 26
    monthly = 12
    quarterly = 4
    semi_annually = 2
    annually = 1

    #user review frequency - user input but assume quarterly was input
    review_frequency = quarterly

    #initiate pandas dataframes for Personal Financial Statement (PFS) with user initial inputs; includes balance sheet and cashflow sections
    balance_sheet = {'Type': ['Asset', 'Asset', 'Asset', 'Liability'], 'Account': ['HSA', '401k', 'Savings', 'Car Loan'], 'Balance': ['3000', '10000', '10000', '15000'],
    'Date': ['2020-01-01', '2020-01-01', '2020-01-01', '2020-01-01']}
    bs_df = pd.DataFrame(balance_sheet, columns = ['Type', 'Account', 'Balance', 'Date'])
    bs_df['Date'] = pd.to_datetime(bs_df['Date'])
    bs_df['Date'] = bs_df['Date'].dt.date

    balance_sheet_next = {'Type': ['Asset', 'Asset', 'Asset', 'Liability'], 'Account': ['HSA', '401k', 'Savings', 'Car Loan'], 'Balance': ['4000', '12000', '12000', '13000'],
    'Date': ['2020-04-01', '2020-04-01', '2020-04-01', '2020-04-01']}
    bs_df_next = pd.DataFrame(balance_sheet_next, columns = ['Type', 'Account', 'Balance', 'Date'])
    bs_df_next['Date'] = pd.to_datetime(bs_df_next['Date'])
    bs_df_next['Date'] = bs_df_next['Date'].dt.date

    #note: when creating user input section, if recurring is selected as "No", then the initial amount inputted from the user should be an estimate
    #Paycheck is net after taxes, deductions, etc. The amount that goes into your bank account
    #Cashflow direction - if it is not coming in the checking account, the direction is "Out"
    cashflow = {'Type': ['Paycheck', 'Bonus', 'HSA', '401k', 'Savings', 'Car Loan'], 'Direction': ['In', 'In', 'Out', 'Out', 'Out', 'Out'], 'Amount': ['2000', '10000', '75', '500',
    '200', '300'], 'Recurring': ['Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes'], 'Frequency': ['26', '1', '26', '26', '12', '12'], 'Date': ['2020-01-01','2020-01-01', '2020-01-01', '2020-01-01',
    '2020-01-01', '2020-01-01']}
    cashflow_df = pd.DataFrame(cashflow, columns = ['Type', 'Direction', 'Amount', 'Recurring', 'Frequency', 'Date'])
    cashflow_df['Date'] = pd.to_datetime(cashflow_df['Date'])

    #could use something like this to create contribution function:  contribution = int(cashflow_df.iloc[0]['Amount']) * Days passed since last review/int(cashflow_df.iloc[0]['Frequency'])
    print(contribution(cashflow_df, 2, days_passed(bs_df_next, bs_df, 0)))

# Define function to calculate how many days have passed based on 2 dataframe inputs and row number as integer; the two dataframes are the previous review date and current one
def days_passed(df1, df, row):
    time_passed = np.timedelta64((df1['Date'][row] - df['Date'][row]), 'ns')
    days = time_passed.astype('timedelta64[D]')
    result = days/np.timedelta64(1, 'D')
    return(result)

# Calculate contribution amount for each row based on dataframe input, row input, and days_passed function
def contribution(df, row, days_passed):
    contribution = int(df.iloc[row]['Amount'])*days_passed/int(df.iloc[row]['Frequency'])
    return(contribution)

if __name__ == '__main__':
    main()