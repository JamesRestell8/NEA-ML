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

stats = pd.read_csv("Master2223.csv")