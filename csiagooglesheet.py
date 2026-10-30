import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Global variables
username_values = []
password_values = []
security_values = []
sheet = []
service = []
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")
num_users = 0

beveragename = []
beverageprice = []
dessertname = []
dessertprice = []
foodname = []
foodprice = []

username = []
finish = []
purchase_details = []
date_ordered = []


def main():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    if not SPREADSHEET_ID:
        raise RuntimeError("Set the SPREADSHEET_ID environment variable (see .env.example).")

    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            CLIENT_SECRET_FILE = os.environ.get("GOOGLE_CREDENTIALS_FILE", "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        global sheet
        global service
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Fetch usernames
        username_results = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="login screen!A2:A").execute()
        global username_values
        username_values = [row[0] for row in username_results.get("values", [])[0:]]
        
        password_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="login screen!B2:B").execute()
        global password_values
        password_values = [row[0] for row in password_result.get("values", [])[0:]]

        security_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="login screen!C2:C").execute()
        global security_values
        security_values = [row[0] for row in security_result.get("values", [])[0:]]
        
        global num_users
        num_users = len(username_values)

        global beveragename, beverageprice
        beveragename_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A3:A8").execute()
        beveragename = [row[0] for row in beveragename_result.get("values", [])[0:]]
        beverageprice_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!B3:B8").execute()
        beverageprice = [row[0] for row in beverageprice_result.get("values", [])[0:]]

        global dessertname, dessertprice
        dessertname_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A12:A17").execute()
        dessertname = [row[0] for row in dessertname_result.get("values", [])[0:]]
        dessertprice_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!B12:B17").execute()
        dessertprice = [row[0] for row in dessertprice_result.get("values", [])[0:]]

        global foodname, foodprice
        foodname_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!A21:A26").execute()
        foodname = [row[0] for row in foodname_result.get("values", [])[0:]]
        foodprice_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="menu page!B21:B26").execute()
        foodprice = [row[0] for row in foodprice_result.get("values", [])[0:]]

        global username, finish, purchase_details, date_ordered
        username_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="manager page!A2:A").execute().get('values', [])
        username = [item[0] for item in username_result]
        finish_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="manager page!B2:B").execute().get('values', [])
        finish = [item[0] for item in finish_result]
        purchase_details_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="manager page!C2:C").execute().get('values', [])
        purchase_details = [item[0] for item in purchase_details_result]
        date_ordered_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="manager page!D2:D").execute().get('values', [])
        date_ordered = [item[0] for item in date_ordered_result]

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()

def getvariables():
    return username_values, password_values, security_values, sheet, SPREADSHEET_ID, num_users
def getmenuvariables():
    return sheet, SPREADSHEET_ID, beveragename, beverageprice, dessertname, dessertprice, foodname, foodprice
def getusername():
    return username_values
def getsheetinfo():
    return sheet, SPREADSHEET_ID
def getsheetinfofinal():
    return sheet, SPREADSHEET_ID, service
def getmanagerpage():
    return username, finish, purchase_details, date_ordered