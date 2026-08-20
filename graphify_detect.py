import json
from graphify.detect import detect
from pathlib import Path

result = detect(Path('.'))
Path('graphify-out/.graphify_detect.json').write_text(
    json.dumps(result, ensure_ascii=False), 
    encoding='utf-8'
)

print(f'Detected {result.get("total_files", 0)} files')
print(f'Total words: ~{result.get("total_words", 0):,}')
print()
print('Corpus breakdown:')
for ftype in ['code', 'document', 'paper', 'image', 'video']:
    count = result.get('file_count', {}).get(ftype, 0)
    if count > 0:
        print(f'  {ftype}: {count} files')
