import os
from slack_sdk import WebClient
from flask import Flask, request




class Slackclient:
    
    def __init__(self, clientID, clientSecret, oauthScope):
        self.clientId = clientID
        self.clientSecret = clientSecret
        self.oauthScope = oauthScope
        
    
    
    

app = Flask(__name__)