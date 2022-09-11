import requests
from requests.exceptions import ConnectionError
import time
import json as js
import numpy as np
import pandas as pd
import matplotlib as mpl 


def jPrint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Get request from API (long-winded in case of server issues)
found = False
i = 0
while i < 30 and not found:
    try:
        r = requests.get(" https://fantasy.premierleague.com/api/bootstrap-static/")
        found = True
    except ConnectionError:
        time.sleep(1)
        i += 1

json = r.json()

# define data frames
elementsDataFrame = pd.DataFrame(json["elements"])
elementsTypesDataFrame = pd.DataFrame(json["element_types"])
teamsDataFrame = pd.DataFrame(json["teams"])

teamsData = teamsDataFrame.get(['name', 'points', 'strength_overall_home', 'strength_overall_away'])

print(teamsData)