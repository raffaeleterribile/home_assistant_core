import json
from pathlib import Path
from collections import defaultdict, Counter
import heapq

# Load the graph
graph_file = Path('graphify-out/graph.json')
with open(graph_file, 'r', encoding='utf-8') as f:
    graph = json.load(f)

nodes = graph.get('nodes', [])
edges = graph.get('edges', [])

print("\n" + "=" * 80)
print("HOME ASSISTANT CORE - DETAILED ARCHITECTURE ANALYSIS")
print("=" * 80 + "\n")

# Build index of node IDs
node_index = {n.get('id'): n for n in nodes}
print(f"✓ Loaded {len(nodes):,} nodes, {len(edges):,} edges\n")

# Calculate node degree (centrality)
node_degree = defaultdict(int)
for edge in edges:
    src = edge.get('source')
    tgt = edge.get('target')
    if src:
        node_degree[src] += 1
    if tgt:
        node_degree[tgt] += 1

# Find top god nodes (most connected)
print("📊 CRITICAL NODES (by connections):")
print("-" * 80)
top_gods = heapq.nlargest(20, node_degree.items(), key=lambda x: x[1])
for i, (node_id, degree) in enumerate(top_gods, 1):
    node = node_index.get(node_id, {})
    label = node.get('label', node_id)
    file_info = ""
    if 'source_file' in node:
        src = node['source_file']
        if 'homeassistant' in src:
            parts = src.split('/')
            idx = parts.index('homeassistant')
            file_info = f" [{'/'.join(parts[idx:idx+3])}]"
    print(f"  {i:2}. {label:40} {degree:6,} connections{file_info}")

print("\n" + "=" * 80)
print("COMPONENT ARCHITECTURE")
print("=" * 80 + "\n")

# Group nodes by component
component_graph = defaultdict(lambda: {'nodes': set(), 'external_edges': 0})
component_internal_edges = defaultdict(int)

for node in nodes:
    src_file = node.get('source_file', '')
    if 'components/' in src_file:
        parts = src_file.split('/')
        idx = parts.index('components')
        if idx + 1 < len(parts):
            comp = parts[idx + 1]
            component_graph[comp]['nodes'].add(node.get('id'))

# Count edges within and between components
for edge in edges:
    src = edge.get('source')
    tgt = edge.get('target')
    src_node = node_index.get(src, {})
    tgt_node = node_index.get(tgt, {})
    
    src_file = src_node.get('source_file', '')
    tgt_file = tgt_node.get('source_file', '')
    
    src_comp = None
    tgt_comp = None
    
    if 'components/' in src_file:
        parts = src_file.split('/')
        if 'components' in parts:
            idx = parts.index('components')
            if idx + 1 < len(parts):
                src_comp = parts[idx + 1]
    
    if 'components/' in tgt_file:
        parts = tgt_file.split('/')
        if 'components' in parts:
            idx = parts.index('components')
            if idx + 1 < len(parts):
                tgt_comp = parts[idx + 1]
    
    if src_comp and tgt_comp:
        if src_comp == tgt_comp:
            component_internal_edges[src_comp] += 1
        else:
            component_graph[src_comp]['external_edges'] += 1
            component_graph[tgt_comp]['external_edges'] += 1

print("TOP COMPONENTS (by internal complexity):")
print("-" * 80)
comp_stats = []
for comp, data in component_graph.items():
    internal = component_internal_edges.get(comp, 0)
    external = data['external_edges']
    nodes_count = len(data['nodes'])
    comp_stats.append((comp, nodes_count, internal, external))

comp_stats.sort(key=lambda x: x[1], reverse=True)
for i, (comp, n_nodes, internal, external) in enumerate(comp_stats[:20], 1):
    print(f"  {i:2}. {comp:30} {n_nodes:5,} nodes  |  "
          f"{internal:6,} internal edges  |  {external:6,} external deps")

print("\n" + "=" * 80)
print("CORE MODULES (outside components)")
print("=" * 80 + "\n")

core_modules = Counter()
for node in nodes:
    src_file = node.get('source_file', '')
    if 'homeassistant/' in src_file and 'components/' not in src_file:
        parts = src_file.split('/')
        if len(parts) > 1:
            # Get the main module (helpers, auth, core, etc.)
            for part in parts[1:]:
                if part and not part.endswith('.py'):
                    core_modules[part] += 1
                    break

print("Core Modules by Size:")
for module, count in core_modules.most_common(12):
    print(f"  {module:25} {count:6,} nodes")

print("\n" + "=" * 80)
