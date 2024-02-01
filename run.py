import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('2love_sandwiches')

def get_sales_data():
    while True:
        """ Get the sales figure inputs from user """
        print("Please enter sales data from the last market day.")
        print("there should be 6 numbers separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print("The data is valid!")
            break
    return sales_data

def validate_data(values):
    """ This will validate the data given """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are needed, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data {e}, please try again\n")
        return False
    return True
def update_sales(data):
    """ Updates the sales data sheet """
    print("Updating sales worksheet now! ... \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Worksheet updated \n")
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def main():
    """ Main function to call rest of code"""
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales(sales_data)

print("Welcome to the Love Sandwiches automation system")
main()