import utils.script as scr

# Clear the screen
scr.clear()

# Make an API request and get the exchange rates
response = scr.request()
exchange_rates = scr.preprocessing(response)

# Get the user's input for the currency they want to exchange, the amount they want to exchange, and the currency they want to receive
currency_give, amount_give, currency_receive = scr.req_to_give(exchange_rates)

# Calculate the amount of currency the user will receive
amount_receive = scr.calculation(currency_give, amount_give, currency_receive, exchange_rates)

# Print the results
print("For {} {} you will receive {} {}".format(amount_give, currency_give, amount_receive, currency_receive))
