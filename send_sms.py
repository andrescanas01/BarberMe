# we import the Twilio client from the dependency we just installed
from twilio.rest import Client


def send_test(phonenumber, username,  shopname):
    # the following line needs your Twilio Account SID and Auth Token
    client = Client("AC5f6458b512771845e6e1a551d6a46555", "a18a11b7b1401459d62ca9a28985c75b")

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    num = "+1" + str(phonenumber)
    message = "hi " + username + "! " + shopname + " has something new to show you!"
    # account to send SMS to any phone number
    client.messages.create(to=num,
                           from_="+12392014995",
                           body=message)