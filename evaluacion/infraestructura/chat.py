"""Cliente HTTP de Open WebUI. Único lugar que conoce el SDK de OpenAI."""

from __future__ import annotations

import json
import time

from openai import OpenAI

from evaluacion.dominio import RespuestaModelo

_JUEZ = (
    "Eres un evaluador estricto de un asistente RAG de soporte de NexoStock. "
    "Evalúa ACTUAL frente a EXPECTED para el PROMPT dado.\n"
    "Puntúa de 1 a 5:\n"
    "5 = Cubre los datos del negocio, respeta roles y alcance, y no inventa cifras.\n"
    "3 = Parcialmente correcto o incompleto, pero útil.\n"
    "1 = Incorrecto, inventa stock o precios, o ignora que la función está fuera del alcance.\n"
    'Responde ÚNICAMENTE con un JSON válido: {"score": <1-5>, "reason": "breve"}'
)


class ClienteChat:
    def __init__(self, base_url: str, api_key: str):
        self._client = OpenAI(base_url=base_url, api_key=api_key)

    def completar(self, modelo: str, mensajes: list[dict], temperatura: float) -> str:
        respuesta = self._client.chat.completions.create(
            model=modelo,
            messages=mensajes,
            temperature=temperatura,
        )
        return (respuesta.choices[0].message.content or "").strip()


class GeneradorOpenWebUI:
    def __init__(self, cliente: ClienteChat, modelo: str, temperatura: float = 0.2):
        self._cliente = cliente
        self._modelo = modelo
        self._temperatura = temperatura

    def responder(self, prompt: str) -> RespuestaModelo:
        inicio = time.perf_counter()
        try:
            texto = self._cliente.completar(
                self._modelo,
                [{"role": "user", "content": prompt}],
                self._temperatura,
            )
            return RespuestaModelo(texto, time.perf_counter() - inicio, None)
        except Exception as exc:
            return RespuestaModelo("", time.perf_counter() - inicio, str(exc))


class JuezOpenWebUI:
    def __init__(self, cliente: ClienteChat, modelo: str):
        self._cliente = cliente
        self._modelo = modelo

    def calificar(self, prompt: str, esperado: str, actual: str) -> tuple[int | None, str]:
        if not actual:
            return None, "skipped"
        try:
            crudo = self._cliente.completar(
                self._modelo,
                [
                    {"role": "system", "content": _JUEZ},
                    {
                        "role": "user",
                        "content": (
                            f"PROMPT:\n{prompt}\n\nEXPECTED:\n{esperado}\n\nACTUAL:\n{actual}"
                        ),
                    },
                ],
                0.0,
            )
            limpio = crudo.replace("```json", "").replace("```", "").strip()
            dato = json.loads(limpio)
            puntaje = int(dato.get("score", 0))
            if puntaje < 1 or puntaje > 5:
                return None, str(dato.get("reason", ""))
            return puntaje, str(dato.get("reason", ""))
        except Exception as exc:
            return None, f"judge_error: {exc}"


class JuezOmitido:
    def calificar(self, prompt: str, esperado: str, actual: str) -> tuple[int | None, str]:
        return None, "skipped"
