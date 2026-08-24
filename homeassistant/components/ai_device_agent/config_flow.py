"""Config flow for the AI device agent integration."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DEFAULT_TITLE, DOMAIN


class AiDeviceAgentConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AI device agent."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=DEFAULT_TITLE, data={})

        return self.async_show_form(step_id="user")
