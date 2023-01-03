## Package Imports

import requests
import pandas as pd
from pathlib import Path
import datetime
from datetime import timedelta
from pandas.io.json import json_normalize
import json
# import numpy as np
import pprint

# https://python.plainenglish.io/becoming-a-data-swolentist-visualizing-peloton-stats-with-plotly-express-271f0b2d4907

# https://github.com/geudrik/peloton-client-library/blob/master/API_DOCS.md

# https://github.com/jckeith/Peltoton/blob/main/Peloton(Onepeloton)API_Walkthrough.ipynb

# https://app.swaggerhub.com/apis/DovOps/peloton-unofficial-api/0.3.0

s = requests.Session()

# with open('host.txt') as g:
#     hostname = g.read()
#
# with open('dbname.txt') as f:
#     var = f.read()
#

raw_path = r'C:\Users\Owner\OneDrive\Documents\Python'

formatted_path = raw_path.replace("\\", "/")

filepath = Path(formatted_path)

pwd_path = filepath / 'pwd.txt'

username_path = filepath / 'username.txt'

with open(username_path) as h:
    username = h.read()
#
with open(pwd_path) as i:
    pwd = i.read()

# with open('pwd.txt') as i:
#     pwd = i.read()
#
payload = {'username_or_email':username, 'password':pwd}
s.post('https://api.onepeloton.com/auth/login', json=payload)

query_personal = s.get('https://api.onepeloton.com/api/me')

print(pd.json_normalize(query_personal.json()).columns.values)

user_id = query_personal.json()['id']

print('User ID: ', user_id)

email = query_personal.json()['email']

print('User Email: ', email)

weight = query_personal.json()['weight']

print('User Weight: ', weight)

height = query_personal.json()['height']

print('User Height (in): ', height)

birthday = query_personal.json()['birthday']

birthday_datetime = datetime.datetime.fromtimestamp(birthday) + timedelta(days=1)

print(birthday_datetime)

total_workouts = query_personal.json()['total_workouts']

print('Total Workouts: ', total_workouts)

gender = query_personal.json()['gender']

print('Gender: ', gender)

location = query_personal.json()['location']

print('Location: ', location)

# personal workout query string
pw_query_string = r"https://api.onepeloton.com/api/user/{}/workouts?joins=ride&limit=100".format(user_id)

q_personal_workouts = s.get(pw_query_string)

print(pd.json_normalize(q_personal_workouts.json()).columns.values)

## Show an example of information in the 'data' key
print(q_personal_workouts.json()['data'][0].keys())

print(q_personal_workouts.json()['data'][0]['id'])

print(q_personal_workouts.json()['data'][0]['created_at'])

print(q_personal_workouts.json()['data'][0]['device_type'])

print(q_personal_workouts.json()['data'][0]['end_time'])
