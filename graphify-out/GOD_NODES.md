# God Nodes

I checked the existing graph in `graph.json` by running `graphify query "god nodes"`. The repo graph is very large, and the query surfaced a few obvious hub nodes around the Home Assistant core + Nice G.O. integration:

- NiceGODevice in `coordinator.py:42`
- NiceGOEntity in `entity.py:12`
- HomeAssistant in `core.py:381`
- ConfigEntry in `config_entries.py:391`
- DataUpdateCoordinator in `update_coordinator.py:65`
- CoordinatorEntity in `update_coordinator.py:677`
- DeviceInfo in `device_registry.py:128`

The command output reported:
- Graph: 317271 nodes
- 63 nodes found in the local traversal
- strongest local hub: NiceGODevice, with a dense web of coordinator/entity/core objects around it

This suggests the graph is centered on the integration coordinator/entity pattern and the Home Assistant core lifecycle objects.