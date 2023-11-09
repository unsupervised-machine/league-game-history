# map_champions_ids_to_names.py
import json
import pickle

with open('../static/champion/champion_details_short.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

champion_data = data['data']
name_to_id_mapping = {}

for key, value in champion_data.items():
    name_to_id_mapping[key] = {
        'name': value['id'],
        'id': value['key']
    }

with open('../static/champion/name_to_id_mapping.pkl', 'wb') as pickle_file:
    pickle.dump(name_to_id_mapping, pickle_file)


