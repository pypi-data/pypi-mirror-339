# Author: syrud

import os
""" Instructions for email setup down below, if you want to
use your own email instead of my junk mail """
#mailto:   julian hasanemail@gmail.com
#631055291 eteacher
#  2128974857 lw
#  2504827468 ljw
#  1137473345 lyx
#  3418415707 qpj
#  1295901287 yq
# gabby 970152562@qq.com
# 19313026 rb
# 1761548327@qq.com bz
# 1508842652@qq.com cj
#2576637800 tq
#2975662067 zbl
#1622521612 zyy
#3232300599 gc
#1361448379 dy
#1679160726@qq.com wjl
# 2395488648
# 3119555212@qq.com
#<--------------- Start of Program --------------->

#EmailSender.py;
#The best way to spam your friends with emails;

#<--------------- Imports --------------->
import sys
import smtplib
from email.mime.text import MIMEText

#<--------------- Helper Functions --------------->

"""
Send 'n' number of identical emails to the receiver;
@param:
server - the gmail/yahoo server host and port;
sender - the displayed name of the email sender;
targets - the people that will be receiving the email(s)
          (stores an email address);
msg - the message that will be sent to the target(s);
"""
def functionOne(server, sender, targets, msg):
    number = int(input("How many emails would you like to send?: "))
    count = 0
    while count < number:
        server.sendmail(sender, targets, msg.as_string())
        count = count + 1
        print(count)
    print("It is finished!")



"""
Sends emails to the receiver letter by letter;
@param:
server;
sender;
targets;
subject - the subject of the message;
"""
def functionTwo(server, sender, targets, subject):
    paragraphText = input("\nType the sentence you would like to send letter by letter:\n")
    message = paragraphText[::-1]
    msg = MIMEText('')
    print("It will take " + str(len(paragraphText)) + " emails")
    count = 0
    for letter in message:
        msg = MIMEText(letter)
        msg['Subject'] = str(subject)
        msg['From'] = sender
        msg['To'] = ', '.join(targets)
        server.sendmail(sender, targets, msg.as_string())
        count = count + 1
        print(count)
    print("It is finished!")


"""
Sends identical emails to receiver when the 'enter' key is pressed;
Quits the process when 'Q' is entered in response to the prompt;
@param:
server;
sender;
targets;
msg;
"""
def functionThree(server, sender, targets, msg):
    count = 0
    while True:
        response = input("Enter 'Q' to quit, or input anything else to continue: ")
        if response in ['Q', 'q']:
            break
        else:
            server.sendmail(sender, targets, msg.as_string())
            count = count + 1
            print("Emails sent: " + str(count))
    print("It is finished!")


"""
Sends distinct emails to receiver per-request by the user;
Can send multiple emails, with different text in each email;
@param:
server;
sender;
targets;
msg;
"""
def functionFour(server, sender, targets, msg):
    count = 0
    while True:
        server.sendmail(sender, targets, msg.as_string())
        count = count + 1
        print("Emails sent: " + str(count))
        response = input("Do you want to send another email?(Yes or No): ")
        if response in ['Yes', 'yes']:
            msg = MIMEText(paragraphWrite())
        else:
            break
    print("It is finished!")


"""
Sends an infinite number of identical emails to the receiver;
@param:
server - the gmail/yahoo server host and port;
sender - the displayed name of the email sender;
targets - the people that will be receiving the email(s)
          (stores an email address);
msg - the message that will be sent to the target(s);
"""
def functionFive(server, sender, targets, msg):
    count = 0
    while True:
        server.sendmail(sender, targets, msg.as_string())
        count = count + 1
        print(count)
    print("It is finished!")


"""
Sends emails to the receiver word by word;
@param:
server;
sender;
targets;
subject - the subject of the message;
"""
def functionSix(server, sender, targets, subject):
    paragraphText = input("\nType the sentence you would like to send word by word:\n")
    message = paragraphText[::-1] + " "
    msg = MIMEText('')
    number = 0
    for letter in message:
        if (letter == " "):
            number = number + 1

    print("It will take " + str(number) + " emails")

    count = 0
    word = ""
    reverseWord = ""
    for letter in message:
        if (letter == " "):
            msg = MIMEText(reverseWord)
            msg['Subject'] = str(subject)
            msg['From'] = sender
            msg['To'] = ', '.join(targets)
            server.sendmail(sender, targets, msg.as_string())
            count = count + 1
            print(count)
            word = ""
            reverseWord = ""
        else:
            word = word + letter
            reverseWord = word[::-1]
    print("It is finished!")


"""
Displays a prompt that allows the user to enter what they would like to write in the email
"""
def paragraphWrite():
    print("\nWhat would you like to send?\nEnter an empty paragraph to finish your email:")
    message = """"""
    while True:
        line = input("")
        if line == "":
            break
        else:
            message = message + line + "\n"
    return message

#<--------------- Main Function --------------->


# Main function that runs the whole program;
# 'def main()' was created to make it recursive;
def main():

# Asks user for what email-spamming function they would like to use;
    start = input("""Enter 1 if you would like to send multiple emails
Enter 2 if you would like to send a sentence in the form of an email (a letter at a time)
Enter 3 if you would like to continuously send emails until you want to stop
Enter 4 if you would like to send distinct emails separately, one at a time
Enter 5 if you would like to send emails indefinitely
Enter 6 if you would like to send a sentence in the form of an email (a word at a time)
""")

# Checks to see if the number option is valid
# If the number option is not valid, the program runs itself again (start over);
    if start not in ['1', '2', '3', '4', '5', '6']:
        print(str(start) + " is not a valid number\n")
        main()

# Gmail server information;
# Yahoo server address: smtp.mail.yahoo.com;
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465


     #INSTRUCTIONS FOR CHANGING LOGIN INFO:
     #1) Log in
     #2) Go to 'Google Account'
     #3) Go to the 'Security' tab
     #4) Turn on 2-Step Verification
     #5) Turn on "App Passwords"
     #6) Get the App Password, and Email Address and replace the below Login information

# Account information for login;
    username = "j49938032"
    password = "umzhhahtgjbcqopr"
    sender = "j49938032@gmail.com"
# Logging in the account;
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)

# Prompts user for the receivers email as well as the email subject;
    targets = [input("Enter the receiver's email: ")]
    subject = input("Enter the email subject: ")

# functionTwo is vastly different from the other two functions;
# A part of the program was dedicated to this specific option;
    if (start == '2'):
        functionTwo(server, sender, targets, subject)

    elif (start == '6'):
        functionSix(server, sender, targets, subject)

# The other functions are all run through this else statement;
    else:
        message = paragraphWrite()
        msg = MIMEText(message)
        msg['Subject'] = str(subject)
        msg['From'] = sender
        msg['To'] = ', '.join(targets)

        if (start == '1'):
            functionOne(server, sender, targets, msg)

        elif (start == '3'):
            functionThree(server, sender, targets, msg)

        elif (start == '4'):
            functionFour(server, sender, targets, msg)

        elif (start == '5'):
            functionFive(server, sender, targets, msg)

# Not logging out sucks;
    server.quit()

# Runs program upon startup;
# main()