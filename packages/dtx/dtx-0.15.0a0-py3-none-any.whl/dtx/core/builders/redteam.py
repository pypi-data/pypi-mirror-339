from typing import Union
from ..repo.plugin import PluginRepo
from ..models.scope import Agent, PluginInScopeConfig, RedTeamScope, RedTeamSettings, PluginsInScope

class RedTeamScopeBuilder:
    """
    Builder class for RedTeamScope with all plugins enabled by default.
    """
    def __init__(self):
        self.agent = None
        self.plugins = PluginsInScope(plugins=[
            plugin for plugin in PluginRepo.get_all_plugins() if isinstance(plugin, str)
        ])
        self.num_tests = 5

    def set_agent(self, agent: Agent):
        self.agent = agent
        return self

    def set_num_tests(self, num_tests: int):
        self.num_tests = num_tests
        return self

    def add_plugin(self, plugin: Union[str, PluginInScopeConfig]):
        """Allows adding a plugin either as a string (ID) or a PluginInScopeConfig object."""
        if isinstance(plugin, str):
            self.plugins.append(PluginInScopeConfig(id=plugin))
        elif isinstance(plugin, PluginInScopeConfig):
            self.plugins.append(plugin)
        return self

    def build(self) -> RedTeamScope:
        if not self.agent:
            raise ValueError("Agent must be set before building RedTeamScope.")

        return RedTeamScope(
            agent=self.agent,
            redteam=RedTeamSettings(num_tests=self.num_tests, plugins=self.plugins)
        )
