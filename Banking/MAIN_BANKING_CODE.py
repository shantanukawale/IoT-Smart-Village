#import cv2
import numpy as np
import json
import requests
import urllib2
import RPi.GPIO as GPIO
import MFRC522
import signal
import sys

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    #print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the IoT Banking Service"
#print "Press Ctrl-C to stop."
print ""
print ""
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
        print ""
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        #print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"


    flag=0

    x = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
    i=1
    url = 'https://iot-smart-village.firebaseio.com/'+str(i)+'/UID.json'
    json_object = json.load(urllib2.urlopen(url))

    while True:
        while(json_object!=None):
            if x == str(json_object):
                url0 = 'https://iot-smart-village.firebaseio.com/'+str(i)+'/Aadhar.json'
                url1 = 'https://iot-smart-village.firebaseio.com/'+str(i)+'/Address.json'
                url2 = 'https://iot-smart-village.firebaseio.com/'+str(i)+'/Name.json'
                url3 = 'https://iot-smart-village.firebaseio.com/'+str(i)+'/Pin.json'
                url4 = 'https://iot-smart-village.firebaseio.com/'+str(i)+'/Balance.json'
                url5 = 'https://iot-smart-village1.firebaseio.com/'+'validationPin.json'
                z=i
                json_object0 = json.load(urllib2.urlopen(url0))
                json_object1 = json.load(urllib2.urlopen(url1))
                json_object2 = json.load(urllib2.urlopen(url2))
                json_object3 = json.load(urllib2.urlopen(url3))
                json_object4 = json.load(urllib2.urlopen(url4))
                json_object5 = json.load(urllib2.urlopen(url5))
            
                print "Name: " + json_object2
                print "Address: " + json_object1
                print "Aadhar no: " + str(json_object0)
                print ""
                pin=raw_input("Please enter your pin:")
                #print json_object3

                if(json_object3 == str(pin)):
                    print "Your current balance is Rs." + str(json_object4) + "."
                    q = raw_input("Do you wish to make a transaction? Y/N \n")

                    if q=='y' or q=='Y':
                        print "Please select the type of transaction."
                        print "1.Deposit"
                        print "2.Withdrawal"
                        dorw=raw_input()

                        if dorw == '1':
                            dep=int(raw_input ("Please hand over the money to the bank representative and enter the amount:"))
                            #print (type(dep))
                            vpin=raw_input("Bank representative's validation Pin:")
                            #print type(vpin)
                            #print int(json_object5)
                            validationPin=int(json_object5)
                            bal=int(json_object4)

                            if int(vpin)==validationPin:
                                bal=bal+dep
                                json_object4=str(bal)
                                print ("Your new balance is Rs. "+str(bal))
                                print("Thank You for visiting")
                                requests.put('https://iot-smart-village.firebaseio.com/'+ str(z) + '/Balance.json',data=json.dumps(json_object4))

                            else:
                                print "Invalid Validation Pin."
                                print("Thank You for visiting")
                        elif dorw=='2':
                            #print int(json_object4)
                            wit=int(raw_input("Enter the withdrawal amount:"))
                            bal=int(json_object4)

                            if bal>=wit:
                                bal=bal-wit
                                json_object4=str(bal)
                                print ("Your new balance is Rs. "+str(bal))
                                print("Please collect the amount from the bank representative")
                                print("Thank You for visiting")
                                requests.put('https://iot-smart-village.firebaseio.com/'+ str(z) + '/Balance.json',data=json.dumps(json_object4))

                            else:
                                print "Your balance is less than the amount you want to withdraw. Please enter a smaller amount."
                                print("Thank You for visiting")

                        else:
                            print ("Invalid  Option")
                            print("Thank You for visiting")

                    else:
                        print "Thank you for visiting"

                else:
                    print "Invalid Pin "
                    print("Thank You for visiting")
        
                flag=1
                break
            break
        
    
        i+=1
        z=i
        url = 'https://iot-smart-village.firebaseio.com/'+str(i)+'/UID.json'
        json_object = json.load(urllib2.urlopen(url))
    


    if flag==0:
        print "Invalid Card. Please contact our customer-care for more details."
        print("Thank You for visiting")
    break
sys.exit()    


















