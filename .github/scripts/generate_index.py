import os
import json
from jinja2 import Environment, FileSystemLoader


metadata_dir = 'metadata'
index_data = {'version': 'v1', 'blocklist': [], 'data': []}
addons = {}

def parse_version(version: str):
    try:
        return tuple(map(int, version.split('.')))
    except ValueError:
        return 0, 0, 0

if os.path.exists(metadata_dir):
    json_files = sorted([f for f in os.listdir(metadata_dir) if f.endswith('.json')])
    for json_file in json_files:
        with open(os.path.join(metadata_dir, json_file), 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        addon_id = manifest['id']
        if addon_id not in addons:
            addons[addon_id] = manifest
        else:
            latest_version = addons[addon_id]['version']
            if parse_version(manifest['version']) > parse_version(latest_version):
                addons[addon_id] = manifest
    index_data['data'] = [
        {k: v for k, v in addon.items() if k != 'extra'}
        for addon in addons.values()
    ]

with open('index.json', 'w', encoding='utf-8') as f:
    json.dump(index_data, f, indent=2, ensure_ascii=False)
print('index.json を再構築しました。')

env = Environment(loader=FileSystemLoader('.'))
tmple = env.get_template('index.html.j2')
html = templ.render(addons=addons.values())
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html を再構築しました。')
