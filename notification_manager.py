import smtplib
import pandas


user_data = pandas.read_csv("user_data.csv")
email_list = [item for item in user_data.user_email]

my_email = "placeholder@placeholder.com"
password = "placeholder"


class NotificationManager:
    def send_mail(self, email, msg):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(my_email, password)
            connection.sendmail(my_email, to_addrs=email, msg=f"Subject: Low price plane ticket alert!\n\n{msg}")

