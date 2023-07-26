# from random import randint 
import random as rd
from requests import get

def your_num():
  age = int(input('how old are u ?'))
#   random_age = randint(1, 50);
  random_age = rd.randint(1, 50);
  if age > 20:
    print('20 over')
  elif age < 20:
    print('20 under')
  else :
    print('age = 20')
    print(random_age)

# your_num()

results = {} 

websites = (
  'google.com',
  'airbnb.com',
  'https://twitter.com',
  'facebook.com',
  'naver.com'
)

for web in websites:
  if not web.startswith('https://'):
    web = f'https://{web}'
  res = get(web)
  if res.status_code == 200:
    results[web] = 'status_code is 200'
  else:
    results[web] = 'status_code is not pip200'

print(results)