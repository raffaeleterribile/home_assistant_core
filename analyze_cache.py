import json
from pathlib import Path

cache_dir = Path('graphify-out/cache')
if cache_dir.exists():
    json_files = list(cache_dir.glob('*.json'))
    print(f"Cache contains {len(json_files)} extracted node files")
    
    # Count nodes and edges across cache
    total_nodes = 0
    total_edges = 0
    node_types = {}
    
    count = 0
    for jf in json_files:
        if count > 100:  # Sample first 100
            break
        try:
            data = json.loads(jf.read_text(encoding='utf-8'))
            total_nodes += len(data.get('nodes', []))
            total_edges += len(data.get('edges', []))
            for node in data.get('nodes', []):
                kind = node.get('kind', 'unknown')
                node_types[kind] = node_types.get(kind, 0) + 1
            count += 1
        except:
            pass
    
    print(f"\nSample analysis (first 100 cache files):")
    print(f"  Nodes extracted: ~{total_nodes}")
    print(f"  Edges extracted: ~{total_edges}")
    print(f"  Node types found:")
    for ntype in sorted(node_types.keys()):
        print(f"    - {ntype}: {node_types[ntype]}")
