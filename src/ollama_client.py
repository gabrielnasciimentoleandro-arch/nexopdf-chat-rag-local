"""Cliente mínimo para geração local por meio do Ollama."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import requests


@dataclass(slots=True)
class OllamaClient:
    base_url: str = field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    )
    model: str = "qwen2.5:3b"
    timeout: int = 120

    def available_models(self) -> list[str]:
        response = requests.get(f"{self.base_url}/api/tags", timeout=2)
        response.raise_for_status()
        return [item["name"] for item in response.json().get("models", [])]

    def is_ready(self) -> bool:
        """Confirma que o servidor responde e que o modelo selecionado está instalado."""
        try:
            models = self.available_models()
            return self.model in models
        except (requests.RequestException, ValueError, KeyError):
            return False

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "stream": False,
                "options": {"temperature": 0.1, "num_ctx": 4096},
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "").strip()
        if not content:
            raise RuntimeError("O Ollama retornou uma resposta vazia.")
        return content
