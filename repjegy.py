from flight_search2 import FlightSearch
from notification_manager import NotificationManager
import pandas


flight_search = FlightSearch()
notification_manager = NotificationManager()

#####   VIE,BTS    #####
#####   BHX,SOU,BOH,CWL,EXT,LHR,LTN,LGW,STN,LCY    ######


def add_user():
    first_name = input("What is your first name?  ")
    last_name = input("What is your last name?  ")
    user_email = input("What is your email?  ")
    user_email_confirmation = input("Type your email again.  ")
    start = input("From where do you want to fly?   ")
    end = input("Where do you want to fly to?   ")
    new_data = {
            "first_name": [first_name],
            "last_name": [last_name],
            "user_email": [user_email],
            "from": [start],
            "to": [end]
    }

    if user_email == user_email_confirmation:
        print("You have successfully registered!")
        data = pandas.DataFrame(new_data)
        data.to_csv("user_data.csv", mode="a",index=False, header=False)


data = pandas.read_csv("user_data.csv")
for index, row in data.iterrows():
    flight = flight_search.get_flights(row["from"], row["to"])
    msg = ""
    for i in flight:
        print(i.price)
        if i.price < 700000:
            msg += f"Low price alert!\nOnly {i.price} HUF to fly from {i.origin_city}-{i.origin_airport} with {i.out_airline} to {i.destination_city}-{i.destination_airport}, from {i.out_date} to {i.return_date} for 2 adults!"
            if i.stop_overs > 0:
                msg += f"\n\nFlight has {i.stop_overs} stop over, via {i.via_city}."
            msg += f"\n\nLink to purchase:\n{i.link}\n\n"
    if not flight:
        msg = f"No flight found to {row['to']}."
    notification_manager.send_mail(email=row["user_email"], msg=msg)
