import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import matplotlib.pyplot as plt
import requests
from requests.exceptions import ConnectionError
import time
from understat import Understat
import asyncio
from json import dumps
import aiohttp
import nest_asyncio
from pandas.io.json import json_normalize
import plotly.express as px

pd.options.mode.chained_assignment = None


url = "https://fantasy.premierleague.com/api/bootstrap-static/"
found = False
i = 0
while i < 30 and not found:
    try:
        r = requests.get(url)
        found = True
    except ConnectionError:
        time.sleep(1)
        i += 1
json = r.json()

stats_df = pd.DataFrame(json['elements'])

stats_data = stats_df[['code', 'first_name', 'second_name', 'team', 'element_type', 'now_cost', 'total_points', 
                        'points_per_game', 'minutes', 'goals_scored', 'assists', 'goals_conceded', 'clean_sheets', 'influence', 
                        'creativity', 'threat']]
stats_data['full_name'] = stats_data['first_name'] + " " + stats_data['second_name']

del stats_data['first_name']
del stats_data['second_name']

cols = stats_data.columns.tolist()
cols = cols[-1:] + cols[:-1]
stats_data = stats_data[cols]

print(stats_data.head())

# UNDERSTAT START
async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        player = await understat.get_league_players(
        "epl", 2022
    )
    return dumps(player)

loop = asyncio.get_event_loop()
allPlayerStats = loop.run_until_complete(main())
print(allPlayerStats)
allPlayerStats = pd.read_json(allPlayerStats)

del allPlayerStats['games']
del allPlayerStats['assists']
del allPlayerStats['red_cards']
del allPlayerStats['position']
del allPlayerStats['team_title']
del allPlayerStats['npg']
del allPlayerStats['goals']

allPlayerStats.drop(allPlayerStats[allPlayerStats.time < 30].index, inplace=True)
stats_data.drop(stats_data[stats_data.minutes < 30].index, inplace=True)

stats_data.to_csv("FPL2223.csv")
allPlayerStats.to_csv("Understat2223.csv")
