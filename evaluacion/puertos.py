"""Contratos. El caso de uso depende de estos, no de Open WebUI ni del disco."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from evaluacion.dominio import CasoPrueba, RespuestaModelo, ResultadoCaso


class Generador(Protocol):
    def responder(self, prompt: str) -> RespuestaModelo: ...


class Juez(Protocol):
    def calificar(self, prompt: str, esperado: str, actual: str) -> tuple[int | None, str]: ...


class FuenteCasos(Protocol):
    def cargar(self) -> list[CasoPrueba]: ...


class Bitacora(Protocol):
    def guardar(self, resultados: list[ResultadoCaso]) -> Path: ...


class Observador(Protocol):
    def caso_listo(self, indice: int, total: int, resultado: ResultadoCaso) -> None: ...
