import sys
import json

from sqlalchemy import select
from types import SimpleNamespace
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy import create_engine

from models import Base
from models import WidgetVisit

# engine = create_engine("sqlite://", echo=True)
engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

fileLocation = input('Please provide the file location: ')

# FIXME:
fileLocation = 'sample.json'
# FIXME:


# There is an inconsistency in the docs for the open function. https://docs.python.org/3/library/functions.html#open
# open() takes a second argument, mode. There are two different parameters marked as default :)
file = open(fileLocation)
# Decided on using a list because it's changable and orderable, I'll need to order it using its built in sort func
logs = []

for data in file:
    # widgetVisit = json.loads(data) 
    # {
    #     "httpRequest": {
    #         "cacheHit": true,
    #         "cacheLookup": true,
    #         "latency": "0.002054s",
    #         "requestMethod": "GET",
    #         "requestSize": "204",
    #         "requestUrl": "https://embedsocial.com/api/pro_hashtag/b4671a7b49a1f8145df2b8c758/",
    #         "responseSize": "20994",
    #         "status": 200
    #     },
    #     "timestamp": "2023-05-03T00:00:03.567794Z",
    #     "severity": "INFO"
    # }
    # user = json.loads(json_obj, object_hook = User)
    # print(f"User {user.name}, age {user.age}, email {user.email}")
    widgetVisit = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

    widgetRef = widgetVisit.httpRequest.requestUrl[len('https://embedsocial.com/api/pro_hashtag/'):].split('/')[0].strip()
    visits_date = datetime.fromisoformat(widgetVisit.timestamp[:-1] + '+00:00')

    widgetVisit = WidgetVisit(
        1, 
        'Widget', 
        widgetRef, 
        widgetVisit.httpRequest.requestUrl, 
        visits_date
    )

    logs.append(widgetVisit)

# Why do I have to use logs.append for appending elements but len(logs) to get the length of the list :(
# print(logs[0])


with Session(engine) as session:
    session.add_all(logs)
    session.commit()

session = Session(engine)
stmt = select(WidgetVisit).where(WidgetVisit.widget_ref.in_(["d66cc4b5bbd5cd8025cdb2b183"]))

# for widgetVisit in session.scalars(stmt):
#     print(widgetVisit)
#     break

# Write a command line app with a file name as parameter. Read json objects from the file, and convert them to a DTO. Process this later and write it in the database.

# The goal is to write in the widget_visit table (in the embedsocial db), sorted by date, and increment the number of visits for each widget. The original plan was to use pubsub, but I decided to remove it. It has a steep learning curve and will take a few days to setup (this is better used testing the languages).

# Each entry in the db should be grouped by date, and incremented if it already exists. It's fine to use a sample owner id, but it's better to get the real owner and widget type from the db.

# Follow the code in the MessageHandler in PubSub bundle, and add all necessary constants files and libraries.