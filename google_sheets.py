import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)



def update_google_sheet(trades, sheet_name):
    if not trades:
        print(f"No trades to update for {sheet_name}.")
        return

    try:
        spreadsheet = client.open(sheet_name)
        print(f"Google Sheet found: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
        sheet = spreadsheet.sheet1
    except gspread.SpreadsheetNotFound:
        print(f"Spreadsheet '{sheet_name}' not found. Creating new spreadsheet.")
        spreadsheet = client.create(sheet_name)
        print(f"New Google Sheet created: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
        sheet = spreadsheet.sheet1

    headers = ['Entry Date', 'Exit Date', 'Entry Price', 'Exit Price', 'Profit']
    sheet.clear()
    sheet.append_row(headers)

    for trade in trades:
        row = [str(trade['Entry Date']), str(trade['Exit Date']), trade['Entry Price'], trade['Exit Price'], trade['Profit']]
        sheet.append_row(row)
