import json
from pprint import pprint

with open('dict.json') as json_data:
    d = json.load(json_data)
    print(len(d[1]))