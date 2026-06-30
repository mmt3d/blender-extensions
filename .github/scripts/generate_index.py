import os
import json


metadata_dir = 'metadata'
index_data = {'version': 'v1', 'blocklist': [], 'data': []}

if os.path.exists(metadata_dir):
    json_files = sorted([f for f in os.listdir(metadata_dir) if f.endswith('.json')])
    for json_file in json_files:
        with open(os.path.join(metadata_dir, json_file), 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        index_data['data'] = [ext for ext in index_data['data'] if ext['id'] != manifest['id']]
        index_data['data'].append(manifest)

with open('index.json', 'w', encoding='utf-8') as f:
    json.dump(index_data, f, indent=2, ensure_ascii=False)
print('index.json を再構築しました。')
