"""Caso de uso: recorre el dataset y deja cada caso medido."""

from __future__ import annotations

from evaluacion.dominio import CasoPrueba, ResultadoCaso, palabras_cumplidas, revisar_palabras
from evaluacion.puertos import Generador, Juez, Observador


class _SinObservador:
    def caso_listo(self, indice: int, total: int, resultado: ResultadoCaso) -> None:
        return None


def evaluar(
    casos: list[CasoPrueba],
    generador: Generador,
    juez: Juez,
    observador: Observador | None = None,
) -> list[ResultadoCaso]:
    aviso = observador or _SinObservador()
    resultados: list[ResultadoCaso] = []
    total = len(casos)
    for indice, caso in enumerate(casos, start=1):
        respuesta = generador.responder(caso.prompt)
        palabras = revisar_palabras(respuesta.texto, caso.palabras_clave)
        puntaje, razon = juez.calificar(
            caso.prompt, caso.respuesta_esperada, respuesta.texto
        )
        resultado = ResultadoCaso(
            caso=caso,
            respuesta=respuesta,
            palabras=palabras,
            palabras_ok=palabras_cumplidas(palabras),
            puntaje_juez=puntaje,
            razon_juez=razon,
        )
        resultados.append(resultado)
        aviso.caso_listo(indice, total, resultado)
    return resultados
