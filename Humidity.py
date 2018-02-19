#!/usr/bin/python
import sys
import json
import Adafruit_DHT
from twilio.rest import Client
import requests
#gpio pin no. 4
ACCOUNT_SID = 'hidden'
AUTH_TOKEN = 'hidden'
TWILIO_PHONE ='hidden'
RECEIVER_PHONE = 'hidden'
client1 = Client(ACCOUNT_SID,AUTH_TOKEN)
msgcounter=0
temperature0=0
humidity0=0
while True:

    humidity, temperature = Adafruit_DHT.read_retry(11,4)
    if temperature==None or humidity==None:
        temperature=0
        humidity=0
    if temperature!=temperature0:
        requests.put('https://iot-smart-village1.firebaseio.com/'+'/temperature.json',data=json.dumps(temperature))
        temperature0=temperature
    elif humidity0!=humidity:
        requests.put('https://iot-smart-village1.firebaseio.com/'+'/humidity.json',data=json.dumps(humidity))
        humidity0=humidity
    if temperature!=0 and humidity!=0:
        print ("Temp: " + str(temperature)  + " Humidity: " + str(humidity))
    else:
        print "unable to read data"        

    if temperature>25 or humidity>25:
        if msgcounter==0:
            client1.api.account.messages.create(to=RECEIVER_PHONE, from_=TWILIO_PHONE, body="Attention!! "+" Temp: "+str(temperature) +"Humidity: "+str(humidity))
            msgcounter=msgcounter+1
        
    
