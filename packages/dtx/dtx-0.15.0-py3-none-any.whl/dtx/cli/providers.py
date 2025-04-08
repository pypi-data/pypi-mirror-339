from dtx.config import globals
from dtx.core.builders.provider_vars import ProviderVarsBuilder
from dtx.core.models.providers.base import ProviderType
from dtx.core.models.providers.ollama import OllamaProvider, OllamaProviderConfig
from dtx.core.models.scope import RedTeamScope
from dtx.plugins.providers.dummy.echo import EchoAgent
from dtx.plugins.providers.eliza.agent import ElizaAgent
from dtx.plugins.providers.gradio.agent import GradioAgent
from dtx.plugins.providers.hf.agent import HFAgent
from dtx.plugins.providers.http.agent import HttpAgent
from dtx.plugins.providers.ollama.agent import OllamaAgent


class ProviderFactory:
    @staticmethod
    def get_agent(
        scope: RedTeamScope,
        provider_type: ProviderType,
        url: str = "",
    ):
        if provider_type == ProviderType.ECHO:
            return EchoAgent()
        elif provider_type == ProviderType.ELIZA:
            return ElizaAgent(url)
        elif provider_type == ProviderType.HF_MODEL:
            model = globals.get_llm_models().get_huggingface_model(url)
            return HFAgent(model)
        elif provider_type == ProviderType.HTTP:
            env_vars = next(ProviderVarsBuilder(scope.environments[0]).build(), {})
            return HttpAgent(provider=scope.providers[0], vars=env_vars)
        elif provider_type == ProviderType.GRADIO:
            env_vars = next(ProviderVarsBuilder(scope.environments[0]).build(), {})
            return GradioAgent(provider=scope.providers[0], vars=env_vars)
        elif provider_type == ProviderType.OLLAMA:
            config = OllamaProviderConfig(model=url)
            provider = OllamaProvider(config=config)
            return OllamaAgent(provider)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
