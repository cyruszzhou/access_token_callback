import os
import json
import webbrowser
import requests
from requests_oauthlib import OAuth2Session
from flask import Flask, request

app = Flask(__name__)


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client_id = "<CLIENT_ID>"
client_secret = "<CLIENT_SECRET>"
redirect_uri = 'http://localhost:5000/callback'
scope = ['https://www.googleapis.com/auth/drive.file']

google = OAuth2Session(client_id, redirect_uri=redirect_uri,
                       scope=scope)

@app.route("/")
def index():
    authorization_url, state = google.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        access_type="offline", prompt="select_account")

    webbrowser.open(authorization_url)
    return "Opened link in your browser"

@app.route("/callback", methods=["GET"])
def callback():
    response = google.fetch_token(
        'https://accounts.google.com/o/oauth2/token',
        authorization_response=request.url,
        client_secret=client_secret)

    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
