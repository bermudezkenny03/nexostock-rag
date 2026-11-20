"""Configuración leída del entorno. El caso de uso no abre .env."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Configuracion:
    base_url: str
    api_key: str
    modelo: str
    juez: str
    etiqueta: str
    dataset: Path
    salida: Path
    meta: float = 70.0

    def exigir_clave(self) -> None:
        if not self.api_key:
            raise RuntimeError("Falta OPENWEBUI_API_KEY en el entorno o en .env")


def cargar_configuracion(raiz: Path) -> Configuracion:
    load_dotenv(raiz / ".env")
    return Configuracion(
        base_url=os.getenv("OPENWEBUI_BASE_URL", "http://localhost:8080/api"),
        api_key=os.getenv("OPENWEBUI_API_KEY", ""),
        modelo=os.getenv("TARGET_MODEL", "nexostock-soporte"),
        juez=os.getenv("JUDGE_MODEL", ""),
        etiqueta=os.getenv("RUN_TAG", "v1_chunk500_ov50"),
        dataset=raiz / "golden_dataset.jsonl",
        salida=raiz / "runs",
    )
