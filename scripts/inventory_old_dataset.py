import os
import json

base_dir = "Dataset_ BanglaBBQ_Old"
subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

print(f"{'Category/Folder':<25} | {'Filename':<35} | {'Rows':<6} | {'Types'}")
print("-" * 85)
for d in sorted(subdirs):
    folder_path = os.path.join(base_dir, d)
    for f in os.listdir(folder_path):
        if f.endswith('.jsonl') or f.endswith('.csv'):
            fpath = os.path.join(folder_path, f)
            count = 0
            types = set()
            if f.endswith('.jsonl'):
                try:
                    with open(fpath, 'r', encoding='utf-8') as jf:
                        for line in jf:
                            if line.strip():
                                count += 1
                                try:
                                    data = json.loads(line)
                                    if 'type' in data:
                                        types.add(data['type'])
                                except:
                                    pass
                except Exception as e:
                    count = f"ERR: {e}"
            else:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as cf:
                    count = sum(1 for _ in cf)
            print(f"{d:<25} | {f:<35} | {str(count):<6} | {types}")
