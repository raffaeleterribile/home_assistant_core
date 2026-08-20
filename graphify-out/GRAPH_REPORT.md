# Graph Report - HomeAssistantCore  (2026-08-20)

## Corpus Check
- 24076 files · ~50,000,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 327663 nodes · 828306 edges · 1 communities
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 53685 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0

## God Nodes (most connected - your core abstractions)
1. `HomeAssistant` - 68623 edges
2. `MockConfigEntry` - 21290 edges
3. `FlowResultType` - 9111 edges
4. `callback()` - 7558 edges
5. `fixture()` - 7022 edges
6. `async_setup_component()` - 6334 edges
7. `AddConfigEntryEntitiesCallback` - 5697 edges
8. `EntityRegistry` - 4801 edges
9. `ConfigFlowResult` - 4449 edges
10. `ConfigEntry` - 3774 edges

## Surprising Connections (you probably didn't know these)
- `test_install_addon()` --uses--> `AddonManager`  [INFERRED]
  tests/components/hassio/test_addon_manager.py → homeassistant/components/hassio/addon_manager.py
- `test_restart_addon()` --uses--> `AddonManager`  [INFERRED]
  tests/components/hassio/test_addon_manager.py → homeassistant/components/hassio/addon_manager.py
- `test_start_addon()` --uses--> `AddonManager`  [INFERRED]
  tests/components/hassio/test_addon_manager.py → homeassistant/components/hassio/addon_manager.py
- `test_stop_addon()` --uses--> `AddonManager`  [INFERRED]
  tests/components/hassio/test_addon_manager.py → homeassistant/components/hassio/addon_manager.py
- `user()` --calls--> `User`  [INFERRED]
  tests/components/aseko_pool_live/conftest.py → homeassistant/auth/models.py

## Import Cycles
- 3-file cycle: `homeassistant/components/unifi/__init__.py -> homeassistant/components/unifi/hub/__init__.py -> homeassistant/components/unifi/hub/hub.py -> homeassistant/components/unifi/__init__.py`
- 3-file cycle: `homeassistant/components/tplink_omada/__init__.py -> homeassistant/components/tplink_omada/controller.py -> homeassistant/components/tplink_omada/coordinator.py -> homeassistant/components/tplink_omada/__init__.py`
- 3-file cycle: `homeassistant/components/reolink/coordinator.py -> homeassistant/components/reolink/host.py -> homeassistant/components/reolink/util.py -> homeassistant/components/reolink/coordinator.py`
- 3-file cycle: `homeassistant/components/renault/coordinator.py -> homeassistant/components/renault/renault_hub.py -> homeassistant/components/renault/renault_vehicle.py -> homeassistant/components/renault/coordinator.py`
- 3-file cycle: `homeassistant/components/onkyo/__init__.py -> homeassistant/components/onkyo/coordinator.py -> homeassistant/components/onkyo/receiver.py -> homeassistant/components/onkyo/__init__.py`
- 3-file cycle: `homeassistant/components/onkyo/__init__.py -> homeassistant/components/onkyo/services.py -> homeassistant/components/onkyo/media_player.py -> homeassistant/components/onkyo/__init__.py`
- 3-file cycle: `homeassistant/components/mysensors/__init__.py -> homeassistant/components/mysensors/entity.py -> homeassistant/components/mysensors/sensor.py -> homeassistant/components/mysensors/__init__.py`
- 3-file cycle: `homeassistant/components/pglab/__init__.py -> homeassistant/components/pglab/discovery.py -> homeassistant/components/pglab/coordinator.py -> homeassistant/components/pglab/__init__.py`
- 3-file cycle: `homeassistant/components/sonos/__init__.py -> homeassistant/components/sonos/services.py -> homeassistant/components/sonos/media_player.py -> homeassistant/components/sonos/__init__.py`
- 3-file cycle: `homeassistant/components/lifx/const.py -> homeassistant/components/lifx/manager.py -> homeassistant/components/lifx/coordinator.py -> homeassistant/components/lifx/const.py`
- 3-file cycle: `homeassistant/components/lifx/const.py -> homeassistant/components/lifx/manager.py -> homeassistant/components/lifx/util.py -> homeassistant/components/lifx/const.py`
- 3-file cycle: `homeassistant/components/otbr/__init__.py -> homeassistant/components/otbr/types.py -> homeassistant/components/otbr/util.py -> homeassistant/components/otbr/__init__.py`
- 3-file cycle: `homeassistant/components/otbr/__init__.py -> homeassistant/components/otbr/websocket_api.py -> homeassistant/components/otbr/util.py -> homeassistant/components/otbr/__init__.py`
- 3-file cycle: `homeassistant/components/zha/__init__.py -> homeassistant/components/zha/repairs/network_settings_inconsistent.py -> homeassistant/components/zha/radio_manager.py -> homeassistant/components/zha/__init__.py`
- 3-file cycle: `homeassistant/components/zha/radio_manager.py -> homeassistant/components/zha/repairs/__init__.py -> homeassistant/components/zha/repairs/network_settings_inconsistent.py -> homeassistant/components/zha/radio_manager.py`
- 3-file cycle: `homeassistant/components/wemo/__init__.py -> homeassistant/components/wemo/coordinator.py -> homeassistant/components/wemo/models.py -> homeassistant/components/wemo/__init__.py`
- 3-file cycle: `homeassistant/components/matter/climate.py -> homeassistant/components/matter/entity.py -> homeassistant/components/matter/discovery.py -> homeassistant/components/matter/climate.py`
- 3-file cycle: `homeassistant/components/matter/discovery.py -> homeassistant/components/matter/siren.py -> homeassistant/components/matter/entity.py -> homeassistant/components/matter/discovery.py`
- 3-file cycle: `homeassistant/components/matter/discovery.py -> homeassistant/components/matter/number.py -> homeassistant/components/matter/entity.py -> homeassistant/components/matter/discovery.py`
- 3-file cycle: `homeassistant/components/matter/discovery.py -> homeassistant/components/matter/sensor.py -> homeassistant/components/matter/entity.py -> homeassistant/components/matter/discovery.py`

## Communities (1 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.00
Nodes (264765): get_pypi_data(), find_github_repo(), check_github_tag(), main(), $schema, extends, config:recommended, enabledManagers (+264757 more)

## Knowledge Gaps
- **13825 isolated node(s):** `$schema`, `config:recommended`, `pep621`, `pip_requirements`, `pre-commit` (+13820 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 90 inferred relationships involving `HomeAssistant` (e.g. with `async_check_ha_config_file()` and `async_create_default_config()`) actually correct?**
  _`HomeAssistant` has 90 INFERRED edges - model-reasoned connections that need verification._
- **Are the 50 inferred relationships involving `MockConfigEntry` (e.g. with `test_v2_api_credentials_trigger_reauth()` and `test_v3_api_credentials_work()`) actually correct?**
  _`MockConfigEntry` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8145 inferred relationships involving `FlowResultType` (e.g. with `AuthManagerFlowManager` and `_async_import()`) actually correct?**
  _`FlowResultType` has 8145 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `callback()` (e.g. with `mock_add_config_entry()` and `mock_add_config_entry()`) actually correct?**
  _`callback()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `fixture()` (e.g. with `FlowResultType` and `hass_client_no_auth()`) actually correct?**
  _`fixture()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `config:recommended`, `pep621` to the rest of the system?**
  _13825 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 1.5430049592919425e-05 - nodes in this community are weakly interconnected._