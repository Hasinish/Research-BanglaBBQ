from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

spreadsheet_id = '1xZhhKZoZuSy-ZXAWWdhCpq9QLh705ScErcnBZacmZnY'
creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)

meta = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    fields='sheets.properties,sheets.conditionalFormats'
).execute()

sheet_map = {s['properties']['title']: (s['properties']['sheetId'], s.get('conditionalFormats', [])) for s in meta['sheets']}

requests = []

# For both Politics sheets, delete old rules and add new rules for range 1 to 200
for title in ['BanglaBBQ_ENG_Politics', 'BanglaBBQ_BEN_Politics']:
    sheet_id, cfs = sheet_map[title]
    # Delete old rules from highest index to lowest
    for idx in range(len(cfs) - 1, -1, -1):
        requests.append({
            'deleteConditionalFormatRule': {
                'sheetId': sheet_id,
                'index': idx
            }
        })
    
    # Add refreshed rules covering rows 1 to 200
    # Rule 0: ambig (purple)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 200, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'ambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.95, 'green': 0.91, 'blue': 1.0}, # #F3E8FF
                        'textFormat': {'foregroundColor': {'red': 0.42, 'green': 0.13, 'blue': 0.66}, 'bold': True}
                    }
                }
            },
            'index': 0
        }
    })
    # Rule 1: disambig (green)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 200, 'startColumnIndex': 2, 'endColumnIndex': 3}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'disambig'}]},
                    'format': {
                        'backgroundColor': {'red': 0.86, 'green': 0.99, 'blue': 0.91}, # #DCFCE7
                        'textFormat': {'foregroundColor': {'red': 0.09, 'green': 0.40, 'blue': 0.20}, 'bold': True}
                    }
                }
            },
            'index': 1
        }
    })
    # Rule 2: neg (rose)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 200, 'startColumnIndex': 3, 'endColumnIndex': 4}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'neg'}]},
                    'format': {
                        'backgroundColor': {'red': 1.0, 'green': 0.89, 'blue': 0.90}, # #FFE4E6
                        'textFormat': {'foregroundColor': {'red': 0.62, 'green': 0.07, 'blue': 0.22}, 'bold': True}
                    }
                }
            },
            'index': 2
        }
    })
    # Rule 3: nonneg (blue)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 200, 'startColumnIndex': 3, 'endColumnIndex': 4}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'nonneg'}]},
                    'format': {
                        'backgroundColor': {'red': 0.88, 'green': 0.95, 'blue': 1.0}, # #E0F2FE
                        'textFormat': {'foregroundColor': {'red': 0.01, 'green': 0.41, 'blue': 0.63}, 'bold': True}
                    }
                }
            },
            'index': 3
        }
    })
    # Rule 4: NA (violet)
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sheet_id, 'startRowIndex': 1, 'endRowIndex': 200, 'startColumnIndex': 4, 'endColumnIndex': 5}],
                'booleanRule': {
                    'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': 'NA'}]},
                    'format': {
                        'backgroundColor': {'red': 0.93, 'green': 0.91, 'blue': 1.0}, # #EDE9FE
                        'textFormat': {'foregroundColor': {'red': 0.36, 'green': 0.13, 'blue': 0.71}, 'bold': True}
                    }
                }
            },
            'index': 4
        }
    })

print(f"Sending {len(requests)} batchUpdate requests...")
res = service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={'requests': requests}
).execute()

print("Successfully updated conditional formatting rules across all rows!")
