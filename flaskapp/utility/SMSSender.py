#from twilio.rest import TwilioRestClient
from flask import Flask
#from credentials import account_sid, auth_token, my_cell, my_twilio
from twilio.rest import Client

def send_sms(my_cell, link):
    account_sid = 'ACf195a4a322c2202c338a44184feef865'
    auth_token = '8282e1b53bd0680347fd7fb90c676b59'
    my_twilio = '+19388008292'
    my_msg = f'[NOTICE] Click on this link after the incident has been resolved. {link}', 
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=my_cell, from_=my_twilio, body=my_msg)
    return "FUCKING APP IS FUCKING WORKING LA CCB"