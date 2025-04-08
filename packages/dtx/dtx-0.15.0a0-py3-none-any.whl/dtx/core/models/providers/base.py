from enum import Enum


class ProviderType(str, Enum):
    ECHO = "echo"
    ELIZA = "eliza"
    HF_MODEL = "hf_model"
    HTTP = "http"
    GRADIO = "gradio"
    OLLAMA = "ollama"

    def __str__(self):
        return self.value  # Ensures correct YAML serialization

    @classmethod
    def values(cls):
        return [member.value for member in cls]
