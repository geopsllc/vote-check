#!/usr/bin/env python3

# Imports
from config import *
import sys
import json
import asyncio
import aiohttp
import requests

# Functions
async def api_get(url):

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as resp:
                return await resp.json()

    except asyncio.TimeoutError:
        return 'timeout'

    except:
        return 'error'

def sapi_get():

    try:
        resp = requests.get(sapi, timeout=30)
        return resp.json()

    except requests.exceptions.Timeout:
        return 'timeout'

    except:
        return 'error'

async def vote_check(delegate,share):

    del_info = await api_get(api + '/delegates/' + delegate)
    if del_info == 'error' or del_info == 'timeout':
        return

    votes = int(int(del_info['data']['votes'])/100000000)
    rank = del_info['data']['rank']
    reward = round(vote/(votes+vote)*422*share/100,2)

    if votes+vote < 2000000:
        data.append([reward,share,rank,delegate])

# Get and Check Argument
if len(sys.argv) < 2:
    print("Please supply vote amount!")
    sys.exit()

if sys.argv[1].isdigit():
    vote = int(sys.argv[1])
else:
    print("Please make sure vote amount is an integer!")
    sys.exit()

# Extract data from dutch team's api if enabled
if use_api:
    print("\nGetting Dutch Team's Delegate Sharing Data...\n")
    delegates = {}
    share_info = sapi_get()
    if share_info == 'error' or share_info == 'timeout':
       print("API did not respond within the allotted time. Please try again or disable the API.")
       sys.exit()
    for delegate in share_info['delegates']:
        if (abs(delegate['share'] - delegate['verifierResult']) < 2 or delegate['verifierResult'] > delegate['share']) and delegate['share'] >= 75:
            delegates[delegate['username']] = delegate['share']

# Initialize List
tasks = []
data = []

# Fill in the List
for delegate in delegates:
    share = delegates[delegate]
    tasks.append(asyncio.ensure_future(vote_check(delegate,share)))

# Async Loop
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(asyncio.wait(tasks))

finally:
    loop.close()

# Sort and Print Data
data.sort(reverse=True)

print('Daily Reward | Sharing % | Delegate Rank | Delegate Name')

for i in range(len(data)):
    print('    ' + f'{data[i][0]:<14}' + f'{data[i][1]:<15}' + f'{data[i][2]:<10}' + data[i][3])
