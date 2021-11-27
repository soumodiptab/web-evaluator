import smtplib

def sendEmail(event_name, to_users, start_date, end_date, url=""):
    gmail_user = "webusability.ssd@gmail.com"
    gmail_password = "Ea6thorq5FM*jxvJ"

    sent_from = str(gmail_user)
    to = to_users
    # url = "https://www.google.com"
    message = """\
Subject: Your usability test has been scheduled

Hi there,
Your test for website usability evaluation has been scheduled.
Name : {event_name}
Start time : {start_date}
End time :  {end_date}
Please visit our website on the test date to start

Cheers,
Usability team.""".format(start_date=start_date, end_date=end_date, url=url, event_name=event_name)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, message)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

    return

def main():
    sendEmail('test subject', 'arshad4000@gmail.com', '1-1-2021')
    return

if __name__ == "__main__":
    main()
