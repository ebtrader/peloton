## Package Imports

import requests
import pandas as pd
from pathlib import Path
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

print(user_id)

email = query_personal.json()['email']

print(email)

workouts = query_personal.json()['total_pedaling_metric_workouts']
print(workouts)

pw_query_string = r"https://api.onepeloton.com/api/user/{}/workouts?joins=ride&limit=100".format(user_id)

q_personal_workouts = s.get(pw_query_string)

print(pd.json_normalize(q_personal_workouts.json()).columns.values)

## Show an example of information in the 'data' key
print(q_personal_workouts.json()['data'][0].keys())

## Show an example of information in the 'summary' key
print('Workout Summary: ', q_personal_workouts.json()['summary'])

q_per_dict = q_personal_workouts.json()['summary']
sum_of_workouts = sum(q_per_dict.values())
print(sum_of_workouts)

print(q_personal_workouts.json()['data'][0]['id'])

print(q_personal_workouts.json()['data'][1]['id'])

for i in range(sum_of_workouts):
    print(q_personal_workouts.json()['data'][i]['id'])

wo_str = r'https://api.onepeloton.com/api/workout/6e5b75c0addd401ba0206cc834e75722'
q_single_workout = s.get(wo_str).json()

##view individual workout data

print(q_single_workout.keys())
print('created at:', q_single_workout['created_at'])
print('fitness_discipline:', q_single_workout['fitness_discipline'])
print('title:', q_single_workout['title'])
print('total work:', q_single_workout['total_work'])

q_single = s.get(wo_str)
print('has pedaling metrics:', q_single.json()['has_pedaling_metrics'])

workout_ride = s.get('https://api.onepeloton.com/api/workout/6e5b75c0addd401ba0206cc834e75722?joins=ride,ride.instructor&limit=1&page=0').json()
print(workout_ride.keys())
print('title:', workout_ride['title'])

#print(pd.json_normalize(q_single_workout.json()).columns.values)

instructor_limit_60 = s.get('https://api.onepeloton.com/api/instructor?limit=60').json()
df3c = pd.json_normalize(instructor_limit_60['data'])
print(df3c)
df3c.to_csv('instructors3.csv')

instructor_no_limit = s.get('https://api.onepeloton.com/api/instructor?page=2').json()
df3b = pd.json_normalize(instructor_no_limit['data'])
print(df3b)
df3b.to_csv('instructors2.csv')

instructor = s.get('https://api.onepeloton.com/api/instructor').json()
print(instructor.keys())
#print(instructor['data'][20]['id'])

print(instructor)
df3a = pd.json_normalize(instructor)
print(df3a)

print('instructor_sort_by:', instructor['sort_by'])
print('instructor_total:', instructor['total'])
print('instructor_count:', instructor['count'])
print('instructor_data:', instructor['data'])
df3 = pd.json_normalize(instructor['data'])
print(df3)
#df3.to_csv('instructors.csv')

print('show_next', instructor['show_next'])

instructor_id = s.get('https://api.onepeloton.com/api/instructor/b8c2734e18a7496fa146b3a42465da67').json()
print(instructor_id.keys())
print(instructor_id['bio'])

q_performance_graph = s.get('https://api.onepeloton.com/api/workout/6e5b75c0addd401ba0206cc834e75722/performance_graph?every_n=30').json()
# n=30 means split data into 30 second increments

print(q_performance_graph.keys())

print(q_performance_graph['segment_list'])

print('seconds since pedaling start:', q_performance_graph['seconds_since_pedaling_start'])
print(len(q_performance_graph['seconds_since_pedaling_start']))

print(q_performance_graph['average_summaries'])

print(pd.json_normalize(q_performance_graph['average_summaries']))

print(q_performance_graph['summaries'])

print(pd.json_normalize(q_performance_graph['summaries']))

print(q_performance_graph['metrics'])

df = pd.json_normalize(q_performance_graph['metrics'])

print(df)
df.to_csv('metrics.csv')

list_of_speeds = df.at[3, 'values']
print(list_of_speeds)

number_of_speeds = len(list_of_speeds)
print(number_of_speeds)

print(q_performance_graph['splits_metrics'])
df1 = pd.json_normalize(q_performance_graph['muscle_group_score'])
print(df1)

ride = s.get('https://api.onepeloton.com/api/v2/ride/archived?browse_category=cycling').json()
print(ride.keys())

# df6 = pd.json_normalize(ride['instructors'])
# print(df6)
# df6.to_csv('cycling_instructors.csv')
#
# df5 = pd.json_normalize(ride['data'])
# print(df5)
# df5.to_csv('classes.csv')

# df7 = pd.json_normalize(ride['ride_types'])
# print(df7)
# df7.to_csv('ride_types.csv')


instructor_rides = s.get\
    ('https://api.onepeloton.com/api/v2/ride/archived?instructor_id=f6f2d613dc344e4bbf6428cd34697820&&browse_category=cycling&limit=200').json()
df8 = pd.json_normalize(instructor_rides['data'])
print(df8)
df8.to_csv('robyn.csv')

all_ride = s.get('https://api.onepeloton.com/api/v2/ride/archived').json()
print(all_ride.keys())

df9 = pd.json_normalize(all_ride['instructors'])
print(df9)
df9.to_csv('all_instructors.csv')

ride_all = s.get('https://api.onepeloton.com/api/ride/filters/?browse_category=cycling').json()
print(ride_all.keys())
# df10 = pd.json_normalize(ride_all['instructors'])
# print(df10)
# df10.to_csv('ride_all_instructors.csv')

query_calendar = s.get('https://api.onepeloton.com/api/user/c79c34efae2c4669a07c935df1aeb988/calendar').json()
print(query_calendar.keys())
print(query_calendar)
df11 = pd.json_normalize(query_calendar['months'])
print(df11)

query_workouts = s.get('https://api.onepeloton.com/api/user/c79c34efae2c4669a07c935df1aeb988/workouts').json()
print(query_workouts.keys())
df12 = pd.json_normalize(query_workouts['data'])
print(df12)
df12.to_csv('workouts.csv')

df13 = pd.json_normalize(query_workouts['summary'])
print(df13)
df13.to_csv('summary.csv')

print(query_workouts['aggregate_stats'])

query_achieve = s.get('https://api.onepeloton.com/api/user/c79c34efae2c4669a07c935df1aeb988/overview').json()
print(query_achieve)

# df13a = pd.json_normalize(query_achieve['data'])
# print(df13a)
# df13a.to_csv('achievements.csv')
