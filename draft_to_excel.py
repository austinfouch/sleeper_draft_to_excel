from sleeper_wrapper import User
import requests
import pandas as pd
from pandas.io.json import json_normalize
from openpyxl import load_workbook

with open ("./user.txt", "r") as hfile:
  sp = hfile.read()
line = sp.split("=")
user = line[1]

user = User(username)
latest_draft_id = user.get_all_drafts("nfl", 2020)[0]['draft_id']
URL = "https://api.sleeper.app/v1/draft/" + latest_draft_id + "/picks"
latest_draft = requests.get(URL).json()

# for the picks in the latest draft, grab those that belong to user and build their draft out
my_picks = {}
i = 0
for pick in latest_draft:
    if pick['picked_by'] == user.get_user_id():
        my_pick = {}
        my_pick['round'] = pick['round']
        my_pick['pick_no'] = pick['pick_no']
        my_pick['name'] = pick['metadata']['first_name'] + " " + pick['metadata']['last_name']
        my_pick['team'] = pick['metadata']['team']
        my_pick['position'] = pick['metadata']['position']
        my_picks[i] = my_pick
    i += 1

path = './sleeper_drafts.xlsx'
book = load_workbook(path)
writer = pd.ExcelWriter(path, enginer='openpyxl')
writer.book = book
df = pd.DataFrame(my_picks).transpose()
df.to_excel(writer, index=False, sheet_name=latest_draft_id)
writer.save()
writer.close()
