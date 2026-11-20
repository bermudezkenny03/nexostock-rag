"""Reglas de la evaluación. No conocen Open WebUI ni archivos."""

from __future__ import annotations

from dataclasses import dataclass
import statistics


@dataclass(frozen=True)
class CasoPrueba:
    id: str
    categoria: str
    prompt: str
    respuesta_esperada: str
    palabras_clave: tuple[str, ...]


@dataclass(frozen=True)
class RespuestaModelo:
    texto: str
    latencia_s: float
    error: str | None


@dataclass(frozen=True)
class ResultadoCaso:
    caso: CasoPrueba
    respuesta: RespuestaModelo
    palabras: dict[str, bool]
    palabras_ok: bool
    puntaje_juez: int | None
    razon_juez: str

    def a_dict(self) -> dict:
        return {
            "id": self.caso.id,
            "category": self.caso.categoria,
            "prompt": self.caso.prompt,
            "expected_answer": self.caso.respuesta_esperada,
            "actual_answer": self.respuesta.texto,
            "latency_s": round(self.respuesta.latencia_s, 3),
            "error": self.respuesta.error,
            "keywords_check": self.palabras,
            "keywords_passed": self.palabras_ok,
            "judge_score": self.puntaje_juez,
            "judge_reason": self.razon_juez,
        }


@dataclass(frozen=True)
class Resumen:
    total: int
    errores: int
    respondidos: int
    aciertos: int
    eficiencia: float
    meta: float
    latencia_promedio: float | None
    latencia_mediana: float | None
    promedio_juez: float | None

    @property
    def cumple_meta(self) -> bool:
        return self.eficiencia >= self.meta


def revisar_palabras(texto: str, palabras: tuple[str, ...]) -> dict[str, bool]:
    contenido = texto.lower()
    return {palabra: palabra.lower() in contenido for palabra in palabras}


def palabras_cumplidas(revisiones: dict[str, bool]) -> bool:
    if not revisiones:
        return True
    return all(revisiones.values())


def resumir(resultados: list[ResultadoCaso], meta: float) -> Resumen:
    total = len(resultados)
    errores = sum(1 for item in resultados if item.respuesta.error)
    respondidos = max(total - errores, 1)
    aciertos = sum(
        1
        for item in resultados
        if item.respuesta.error is None and item.palabras_ok
    )
    latencias = [
        item.respuesta.latencia_s
        for item in resultados
        if item.respuesta.error is None
    ]
    puntajes = [
        item.puntaje_juez
        for item in resultados
        if item.puntaje_juez is not None
    ]
    return Resumen(
        total=total,
        errores=errores,
        respondidos=respondidos,
        aciertos=aciertos,
        eficiencia=aciertos / respondidos * 100,
        meta=meta,
        latencia_promedio=statistics.mean(latencias) if latencias else None,
        latencia_mediana=statistics.median(latencias) if latencias else None,
        promedio_juez=statistics.mean(puntajes) if puntajes else None,
    )
