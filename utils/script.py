import requests
import pandas as pd
from IPython.display import display
import os

def clear():                      
    '''
    defining 'clear' method which erase all previous information from the screen
    '''
    if os.name == 'nt':     # for windows
        _ = os.system('cls')
    else:                   # for mac and linux(here, os.name is 'posix')
        _ = os.system('clear')

def request():
    '''
    making an API request to get current currencies rates
    '''
    api_key = "6641341fcdf34fb7989f2e682ec6b5c0"
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    r = requests.get(url)
    return r

def preprocessing(r):
    '''
    Preprocessing data. Printing currencies rates in Pandas dataframe.
    @return er: Pandas dataframe.
    '''
    data = r.json()
    er = pd.DataFrame.from_dict({"rates": data["rates"]}, orient="index")
    print('Exchanging rates of currencies to 1 USD:')
    columns_per_row = 10
    # Get the number of columns in the DataFrame
    num_columns = len(er.columns)
    # Loop through the columns and display them in sets of 'columns_per_row'
    for i in range(0, num_columns, columns_per_row):
        display(er.iloc[:, i:i + columns_per_row])
        print("\n")  # Add a newline between each set of columns
    return er

def check_amount(amount):
    '''
    Checking amount if it was input properly. If amount is not numeric value it raturns False boolean.
    @param amount: input value.
    @return: boolean.
    '''
    try:
        val = int(amount) 
        return True
    except ValueError:
        try:
           val = float(amount)
           return True
        except ValueError:
           return False

def req_to_give(er):
    '''
    Gets the user's input for the currency they want to exchange, the amount they want to exchange, and the currency they want to receive.
    @param er: The Pandas DataFrame containing the exchange rates.
    @return: The currency being converted from, the amount being converted, and the currency being converted to.
    '''
    currency = input('Which currency do you want to exchange? Input 3 letters as in the dataframe above:')
    currency = currency.upper()
    while currency not in er.columns:
        currency = input("You've input a wrong value. Please, inut 3 letters as in the dataframe above:")
        currency = currency.upper()
    amount = input("You've input {}. Please, input an amount you want to exchange:".format(currency))
    while check_amount(amount) == False:
        amount = input("Pleasem enter a numerical value. Try again...")
    else:
        currency_rec = input("You've input {} {}. Please, input currency you want to receive:".format(amount, currency))
        currency_rec = currency_rec.upper()
        while currency_rec not in er.columns:
            currency_rec = input("You've input a wrong value. Please, inut 3 letters as in the dataframe above:")
            currency_rec = currency_rec.upper()
    return currency, amount, currency_rec

def calculation(currency, amount, currency_rec, er):
    """
    Performs the currency conversion.
    @param currency: The currency being converted from.
    @param amount: The amount being converted.
    @param currency_rec: The currency being converted to.
    @param er: The Pandas DataFrame containing the exchange rates.
    @return: The converted amount.
    """
    if currency == "USD":
        amount_rec = float(amount) * er.at['rates', currency_rec]
        return round(amount_rec, 2)
    elif currency_rec == 'USD':
        amount_rec = float(amount) / er.at['rates', currency]
        return round(amount_rec, 2)
    else:
        amount_in_usd = float(amount) / er.at['rates', currency]
        amount_rec = amount_in_usd * er.loc['rates', currency_rec]
        return round(amount_rec, 2)