#!/usr/bin/env python3

# Imports
from config import *
import sys
import json
import asyncio
import aiohttp

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

async def vote_check(delegate,share):

    del_info = await api_get(api + '/delegates/' + delegate)
    if del_info == 'error' or del_info == 'timeout':
        return

    votes = int(int(del_info['data']['votes'])/100000000)
    rank = del_info['data']['rank']
    reward = round(vote/(votes+vote)*422*share/100,2)

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
