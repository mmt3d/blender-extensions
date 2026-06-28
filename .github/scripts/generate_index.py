import os
import json
import zipfile
import hashlib
import tomllib


def calculate_sha256(filepath):
  sha256_hash = hashlib.sha256()
  with open(filepath, 'rb') as f:
      for byte_block in iter(lambda: f.read(4096), b''):
          sha256_hash.update(byte_block)
  return sha256_hash.hexdigest()


zips_dir = 'zips'
dist_repo_owner = 'mmt3d'
dist_repo_name = 'blender-extensions'

index_data = {'version': 'v1', 'blocklist': [], 'data': []}
zip_files = sorted([f for f in os.listdir(zips_dir) if f.endswith('.zip')]) if os.path.exists(zips_dir) else []

for zip_file in zip_files:
    zip_path = os.path.join(zips_dir, zip_file)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        with zf.open('blender_manifest.toml') as mf:
            manifest = tomllib.load(mf)

    manifest['archive_url'] = f'https://{dist_repo_owner}.github.io/{dist_repo_name}/zips/{zip_file}'
    manifest['archive_size'] = os.path.getsize(zip_path)
    manifest['archive_hash'] = f'sha256:{calculate_sha256(zip_path)}'

    index_data['data'] = [ext for ext in index_data['data'] if ext['id'] != manifest['id']]
    index_data['data'].append(manifest)

with open('index.json', 'w', encoding='utf-8') as f:
    json.dump(index_data, f, indent=2, ensure_ascii=False)
print('index.json を再構築しました。')

# for archive
html_lines = [
  '<!DOCTYPE html>', '<html>', '<head>', '<meta charset=\"utf-8\">',
  '<title>Blender Extensions Archive</title>',
  '<style>body { font-family: sans-serif; padding: 20px; line-height: 1.6; } a { color: #0066cc; text-decoration: none; } a:hover { text-decoration: underline; }</style>',
  '</head>', '<body>', '<h1>Blender アドオン過去バージョンアーカイブ</h1>',
  '<p>最新版で不具合が発生した場合は、対象の過去バージョン（ZIP）を直接ダウンロードし、Blenderの「ファイルからインストール」で上書きしてください。</p>',
  '<ul>'
]
for zip_file in sorted(zip_files, reverse=True):
  html_lines.append(f'    <li><a href=\"./zips/{zip_file}\">{zip_file}</a></li>')
html_lines.extend(['</ul>', '</body>', '</html>'])

with open('index.html', 'w', encoding='utf-8') as f:
  f.write('\n'.join(html_lines) + '\n')
print('index.html を再構築しました。')
