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
    #frequencies: weekly = 52, bi_weekly = 26, monthly = 12, quarterly = 4, semi_annually = 2, annually = 1
    #user review frequency - user input but assume semi_annually was input
    #review_frequency = semi_annually

    #initiate pandas dataframes for Personal Financial Statement (PFS) with user initial inputs; includes balance sheet and cashflow sections
    #initial user inputs
    balance_sheet = {'Type': ['Asset', 'Asset', 'Asset', 'Liability'], 'Account': ['HSA', '401k', 'Savings', 'Car Loan'], 'Current Balance': ['3000', '10000', '10000', '13000'],
    'Date': ['2020-01-01', '2020-01-01', '2020-01-01', '2020-01-01']}
    bs_df = pd.DataFrame(balance_sheet, columns = ['Type', 'Account', 'Current Balance', 'Date'])
    bs_df['Date'] = pd.to_datetime(bs_df['Date'])
    bs_df['Date'] = bs_df['Date'].dt.date

    #dataframe for liabilities information; collect this information if a liability is listed in the balance sheet; need to configure how!
    bs_liabilities = {'Original Balance': ['15000'],'Next Payment': ['2020-01-15'], 'Required Payment': ['250'], 'Original Term': ['72'], 'Remaining Term': ['68'], 'Frequency': ['12']}
    bs_liabilities_df = pd.DataFrame(bs_liabilities, columns = ['Original Balance', 'Next Payment', 'Required Payment', 'Original Term', 'Remaining Term', 'Frequency'])
    bs_liabilities_df['Next Payment'] = pd.to_datetime(bs_liabilities_df['Next Payment'])
    bs_liabilities_df['Next Payment'] = bs_liabilities_df['Next Payment'].dt.date
    
    #review date user inputs
    balance_sheet_next = {'Type': ['Asset', 'Asset', 'Asset', 'Liability'], 'Account': ['HSA', '401k', 'Savings', 'Car Loan'], 'Current Balance': ['4000', '12000', '12000', '13000'],
    'Date': ['2020-06-01', '2020-06-01', '2020-06-01', '2020-06-01']}
    bs_df_next = pd.DataFrame(balance_sheet_next, columns = ['Type', 'Account', 'Current Balance', 'Date'])
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

        
    #everything above this point is essentially a user input; will need to figure out how to implement; computational code starts with this line

    #break down cashflow into essential and non-essential; cashflow expressed as yearly number
    cashflow_in = 0.0
    cashflow_out = 0.0
    for i in range(len(cashflow_df['Direction'])):
        if(cashflow_df['Direction'][i] == 'In'):
            cashflow_in += round(float(cashflow_df['Amount'][i]), 2)*round(float(cashflow_df['Frequency'][i]))
        else:
            cashflow_out += round(float(cashflow_df['Amount'][i]), 2)*round(float(cashflow_df['Frequency'][i]))
    
    #total remaining income to be spli between essential and non-essential; will require user input to split up between these two; note - need better name than net_income
    net_income = cashflow_in - cashflow_out
    print("Net Income: " + f'{net_income}')
        
    #loop to request inputs for essential and non-essential breakdown and check for errors
    while True:
        try:
            #user input
            essential = round(float(input("Essential: ")), 2)
            non_essential = round(float(input("Non-Essential: ")), 2)
            if(essential + non_essential != net_income):
               print("Error. Essential and Non-Essential numbers do not add up to your total Net Income. Please make sure the totals match.")
            else: 
                break
        
        except: 
            ValueError
            print("Please input numbers only.")
      
    #break down balance sheet to tie back to goals; asset focus - user contribution and asset growth; liability focus - paying down faster or lowering rate
    asset_dict = {'Account': [], 'Contribution': [], 'Growth': [], 'Withdrawal': [], 'Date': []}
    for x in range(len(bs_df_next['Type'])):
        if(bs_df_next['Type'][x] == 'Asset'):
            y = 0
            while True:
                if(cashflow_df['Type'][y] == bs_df['Account'][x]):
                    cont = round(contribution(cashflow_df, y, days_passed(bs_df_next,bs_df, x)), 2)
                    growth = round((float(bs_df_next['Current Balance'][x]) - float(bs_df['Current Balance'][x]) - cont), 2)
                    #note that an assumption is made that if no withdrawal happens or growth > 0, withdrawal variable defaults to 0
                    if(growth < 0):
                        #user input to make sure growth was actually negative and not the result of a withdrawal; also error check inputs
                        variable = bs_df_next['Account'][x]
                        while True:
                            answer = input(f"Did you withdraw money from account {variable}? ")
                            if(answer.lower() == "yes"):
                                while True:
                                    try:
                                        withdrawal = round(float(input("Amount withdrawn: ")), 2)
                                        if(withdrawal <= 0):
                                            print("Input positive numbers only.")
                                        else:
                                            break

                                    except:
                                        ValueError
                                        print("Please input numbers only")
                                    
                                growth += withdrawal
                                asset_dict['Withdrawal'].append(withdrawal)
                                break
                            elif(answer.lower() == "no"):
                                asset_dict['Withdrawal'].append(float(0))
                                break
                        break
                    else:
                        asset_dict['Withdrawal'].append(float(0))
                        break
                else:
                    y += 1
            
            asset_dict['Account'].append(bs_df_next['Account'][x])
            asset_dict['Contribution'].append(cont)
            asset_dict['Growth'].append(growth)
            asset_dict['Date'].append(bs_df_next['Date'][x])

    #cag below stands for contribution and growth; new dataframe to record asset contribution and growth
    cag_df = pd.DataFrame(asset_dict)
            
    print(cag_df)
    #could use something like this to create contribution function:  contribution = int(cashflow_df.iloc[0]['Amount']) * Days passed since last review/int(cashflow_df.iloc[0]['Frequency'])
    #print(contribution(cashflow_df, 2, days_passed(bs_df_next, bs_df, 0)))

# Define function to calculate how many days have passed based on 2 dataframe inputs and row number as integer; the two dataframes are the previous review date and current one
def days_passed(df1, df, row):
    time_passed = np.timedelta64((df1['Date'][row] - df['Date'][row]), 'ns')
    days = time_passed.astype('timedelta64[D]')
    result = days/np.timedelta64(1, 'D')
    return(result)

# Calculate contribution amount for each row based on dataframe input, row input, and days_passed function
def contribution(df, row, days_passed):
    contribution = float(df.iloc[row]['Amount'])*days_passed/int(df.iloc[row]['Frequency'])
    return(contribution)

if __name__ == '__main__':
    main()