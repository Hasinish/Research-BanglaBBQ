import os
import sys
import wsgiref.simple_server
from google_auth_oauthlib.flow import InstalledAppFlow, _RedirectWSGIApp, _ExclusiveWSGIServer, _WSGIRequestHandler

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]

cred_path = r'D:\cattle-health-monitoring-multi-task-model\credentials.json'

flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)

host = 'localhost'
wsgi_app = _RedirectWSGIApp("Authentication complete! You can close this window now.")
local_server = wsgiref.simple_server.make_server(
    host,
    0,
    wsgi_app,
    server_class=_ExclusiveWSGIServer,
    handler_class=_WSGIRequestHandler,
)

flow.redirect_uri = f"http://{host}:{local_server.server_port}/"
auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

with open('auth_url.txt', 'w', encoding='utf-8') as f:
    f.write(auth_url)

print("AUTH_URL=" + auth_url, flush=True)

try:
    os.startfile(auth_url)
    print("LAUNCHED_BROWSER", flush=True)
except Exception as e:
    print(f"FAILED_TO_LAUNCH: {e}", flush=True)

local_server.handle_request()

auth_response = wsgi_app.last_request_uri.replace("http", "https")
flow.fetch_token(authorization_response=auth_response)

token_data = flow.credentials.to_json()

with open(r'D:\cattle-health-monitoring-multi-task-model\token.json', 'w', encoding='utf-8') as f:
    f.write(token_data)

with open('token.json', 'w', encoding='utf-8') as f:
    f.write(token_data)

print("TOKEN_SAVED_SUCCESSFULLY", flush=True)
