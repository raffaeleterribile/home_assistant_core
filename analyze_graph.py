import json
from pathlib import Path
from collections import Counter

# Load the graph
graph_file = Path('graphify-out/graph.json')
with open(graph_file, 'r', encoding='utf-8') as f:
    graph = json.load(f)

print("=" * 70)
print("HOME ASSISTANT CORE - KNOWLEDGE GRAPH ANALYSIS")
print("=" * 70)
print()

# Basic stats
nodes = graph.get('nodes', [])
edges = graph.get('edges', [])

print(f"Total Nodes: {len(nodes):,}")
print(f"Total Edges: {len(edges):,}")
print()

# Node types
node_types = Counter(n.get('kind', 'unknown') for n in nodes)
print("NODE TYPES (Top 20):")
for kind, count in node_types.most_common(20):
    print(f"  {kind:30} {count:6,}")
print()

# Find top modules/components
print("TOP MODULES BY NODE COUNT:")
modules = Counter()
for node in nodes:
    if 'source_file' in node:
        # Extract component name from path
        path = node['source_file']
        parts = path.split('/')
        if len(parts) > 1 and 'homeassistant' in parts:
            idx = parts.index('homeassistant')
            if idx + 1 < len(parts):
                component = parts[idx + 1]
                if component == 'components' and idx + 2 < len(parts):
                    component = f"components/{parts[idx + 2]}"
                modules[component] += 1

for module, count in modules.most_common(15):
    print(f"  {module:40} {count:6,} nodes")
print()

# Edge type analysis
edge_types = Counter(e.get('kind', 'unknown') for e in edges)
print("EDGE TYPES (Top 10):")
for etype, count in edge_types.most_common(10):
    print(f"  {etype:30} {count:6,}")
print()

print("=" * 70)
print(f"Graph successfully analyzed. Output: {graph_file}")
print(f"File size: {graph_file.stat().st_size / 1024 / 1024:.1f} MB")
print("=" * 70)
