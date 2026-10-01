import requests

from src.ollama_client import OllamaClient


def test_is_ready_requires_selected_model(monkeypatch):
    client = OllamaClient(model="qwen2.5:3b")
    monkeypatch.setattr(
        OllamaClient,
        "available_models",
        lambda self: ["llama3.2:3b"],
    )
    assert client.is_ready() is False

    monkeypatch.setattr(
        OllamaClient,
        "available_models",
        lambda self: ["qwen2.5:3b"],
    )
    assert client.is_ready() is True


def test_is_ready_handles_connection_failure(monkeypatch):
    client = OllamaClient()

    def fail(self):
        raise requests.ConnectionError("offline")

    monkeypatch.setattr(OllamaClient, "available_models", fail)
    assert client.is_ready() is False
