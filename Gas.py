from time import sleep
import RPi.GPIO as GPIO
from twilio.rest import Client

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

LedOut = 27
Flamein = 22
msgcounter1=0
#Switch Pin
GPIO.setup(Flamein, GPIO.IN)

#Switch Led
GPIO.setup(LedOut, GPIO.OUT)
count = 0

ACCOUNT_SID = 'AC29a985e0cccf5be9d83dbafca050b819'
AUTH_TOKEN = '9720cc9c7416fe310d84f0e334d3b207'
TWILIO_PHONE ='+13126266284'
RECEIVER_PHONE = '+917259370404'
client1 = Client(ACCOUNT_SID,AUTH_TOKEN)

while True:
    try:
        if (GPIO.input(Flamein) == True):
            print 'fire in your house'
            GPIO.output(LedOut, 1)
            sleep(0.1)
            GPIO.output(LedOut, 0)
            sleep(0.1)
            GPIO.output(LedOut, 1)
            if msgcounter1==0:
                client1.api.account.messages.create(to=RECEIVER_PHONE, from_=TWILIO_PHONE, body="Attention!! Your warehouse is on fire!!!")
                msgcounter1=msgcounter1+1
          
        else:
            print 'you are safe'
            msgcounter=0
            GPIO.output(LedOut, 0)
          
    except KeyboardInterrupt:
        exit()
GPIO.cleanup()
