from dotenv import load_dotenv
load_dotenv()

from app.models import Event, User
from app import db

USERS = [
    {
        "first_name": "James",
        "surname": "Edgecombe",
        "nickname": "Jal",
        "email": "j.m.edgecombe@gmail.com"
    },
    {
        "first_name": "James",
        "surname": "Marvin",
        "nickname": "Marv",
        "email": "j_marvin@mail.com"
    },
    {
        "first_name": "Dylan",
        "surname": "Drake",
        "nickname": "Dyl",
        "email": "dylandrake@me.com"
    },
    {
        "first_name": "Sam",
        "surname": "Hollinsworth",
        "nickname": "Holli",
        "email": "sam@gmail.com"
    },
    {
        "first_name": "Dave",
        "surname": "Foster",
        "nickname": "Dave",
        "email": "dave@gmail.com"
    },
    {
        "first_name": "Will",
        "surname": "Dyer",
        "nickname": "Will Dyer",
        "email": "will@gmail.com"
    },
]

EVENTS = [
    {"name": "BBQ",
     "start_date": "2019-12-01",
     "start_time": "12:00",
     "end_date": "2019-12-01",
     "end_time": "14:00",
     "location": "Marv's",
     "status": "Open",
     "created_at": "2019-10-05 10:00:05",
     "organised_by": 2
     },
    {"name": "Catan",
     "start_date": "2019-10-02",
     "start_time": "20:30",
     "end_date": "2019-10-02",
     "end_time": "21:30",
     "location": "Jal's",
     "status": "Open",
     "created_at": "2019-10-01 09:30:00",
     "organised_by": 1
     },
    {"name": "Baby Shower",
     "start_date": "2020-04-01",
     "start_time": "13:00",
     "end_date": "2020-04-01",
     "end_time": "14:00",
     "location": "Sam's",
     "status": "Open",
     "created_at": "2019-10-04 10:00:05",
     "organised_by": 4
     },
    {"name": "IHKN",
     "start_date": "2019-11-30",
     "start_time": "20:00",
     "end_date": "2019-12-01",
     "end_time": "00:00",
     "location": "Dyl's",
     "status": "Open",
     "created_at": "2019-10-05 10:00:05",
     "organised_by": 3
     }
]

RESPONSES = [
    {
        "response_datetime": "2019-10-06 10:00:05",
        "response": "Accept",
        "response_status": "Closed",
        "event": 1,
        "user": 2
    },
    {
        "response_datetime": "2019-10-06 10:10:05",
        "response": "Decline",
        "response_status": "Open",
        "event": 1,
        "user": 2
    },
    {
        "response_datetime": "2019-10-06 11:10:05",
        "response": "Accept",
        "response_status": "Open",
        "event": 2,
        "user": 4
    }
]

# TODO add more responses and 

for user in USERS:
    u = User(first_name=user["first_name"], surname=user["surname"], nickname=user["nickname"], email=user["email"])
    u.set_password("password")
    db.session.add(u)
    db.session.commit()

for event in EVENTS:
    e = Event(name=event["name"], start_date=event["start_date"],
              start_time=event["start_time"], end_date=event["end_date"],
              end_time=event["end_time"], location=event["location"],
              status=event["status"], created_at=event["created_at"],
              organised_by=event["organised_by"])
    db.session.add(e)
    db.session.commit()




