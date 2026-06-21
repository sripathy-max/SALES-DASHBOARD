import os
import json
from google.oauth2 import service_account

# Read the JSON from the environment variable we set in Render
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = service_account.Credentials.from_service_account_info(creds_dict)

# Now use this 'creds' object to connect to gspread/sheets
client = gspread.authorize(creds)
