"""Salida por consola. Separada del caso de uso."""

from __future__ import annotations

from pathlib import Path

from evaluacion.dominio import Resumen, ResultadoCaso


class ObservadorConsola:
    def caso_listo(self, indice: int, total: int, resultado: ResultadoCaso) -> None:
        if resultado.respuesta.error:
            estado = "ERR"
        else:
            estado = f"{resultado.respuesta.latencia_s:.2f}s"
        puntaje = ""
        if resultado.puntaje_juez is not None:
            puntaje = f" | score={resultado.puntaje_juez}/5"
        print(f"[{indice}/{total}] {resultado.caso.id} ({estado}){puntaje}")


def imprimir_resumen(resumen: Resumen, archivo: Path) -> None:
    print("\n=== RESUMEN DE EVALUACIÓN ===")
    print(f"Archivo guardado : {archivo}")
    print(f"Casos totales    : {resumen.total}")
    print(f"Errores HTTP/API : {resumen.errores}")
    if resumen.latencia_promedio is not None and resumen.latencia_mediana is not None:
        print(
            f"Latencia prom.   : {resumen.latencia_promedio:.2f}s | "
            f"Mediana: {resumen.latencia_mediana:.2f}s"
        )
    print(
        f"Keywords OK      : {resumen.eficiencia:.1f}% "
        f"({resumen.aciertos}/{resumen.respondidos})"
    )
    estado = "cumplida" if resumen.cumple_meta else "no cumplida"
    print(f"Meta {resumen.meta:.0f}%        : {estado}")
    if resumen.promedio_juez is not None:
        print(f"Promedio juez    : {resumen.promedio_juez:.2f} / 5.00")
