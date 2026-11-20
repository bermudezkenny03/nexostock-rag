"""Lectura del golden dataset y escritura de la corrida."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

from evaluacion.dominio import CasoPrueba, ResultadoCaso


class DatasetJsonl:
    def __init__(self, ruta: Path):
        self._ruta = ruta

    def cargar(self) -> list[CasoPrueba]:
        if not self._ruta.exists():
            raise FileNotFoundError(f"No se encontró {self._ruta}")
        casos: list[CasoPrueba] = []
        with self._ruta.open("r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if not linea:
                    continue
                fila = json.loads(linea)
                palabras = tuple(fila.get("required_keywords") or [])
                casos.append(
                    CasoPrueba(
                        id=str(fila.get("id") or f"case_{numero:03d}"),
                        categoria=str(fila.get("category") or "general"),
                        prompt=str(fila.get("prompt") or ""),
                        respuesta_esperada=str(fila.get("expected_answer") or ""),
                        palabras_clave=palabras,
                    )
                )
        return casos


class BitacoraJsonl:
    def __init__(self, carpeta: Path, etiqueta: str):
        self._carpeta = carpeta
        self._etiqueta = etiqueta

    def guardar(self, resultados: list[ResultadoCaso]) -> Path:
        self._carpeta.mkdir(parents=True, exist_ok=True)
        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = self._carpeta / f"eval_{self._etiqueta}_{marca}.jsonl"
        with destino.open("w", encoding="utf-8") as archivo:
            for resultado in resultados:
                archivo.write(json.dumps(resultado.a_dict(), ensure_ascii=False) + "\n")
        return destino
