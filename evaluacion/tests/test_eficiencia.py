import unittest

from evaluacion.dominio import (
    CasoPrueba,
    RespuestaModelo,
    ResultadoCaso,
    palabras_cumplidas,
    resumir,
    revisar_palabras,
)


def _resultado(texto: str, palabras: tuple[str, ...], error: str | None = None) -> ResultadoCaso:
    caso = CasoPrueba("case_001", "roles", "pregunta", "esperado", palabras)
    revisiones = revisar_palabras(texto, palabras)
    return ResultadoCaso(
        caso=caso,
        respuesta=RespuestaModelo(texto, 0.4, error),
        palabras=revisiones,
        palabras_ok=palabras_cumplidas(revisiones),
        puntaje_juez=None,
        razon_juez="skipped",
    )


class EficienciaTest(unittest.TestCase):
    def test_la_palabra_clave_no_distingue_mayusculas(self):
        revisiones = revisar_palabras("El Propietario administra el negocio", ("propietario",))
        self.assertTrue(revisiones["propietario"])

    def test_faltan_palabras_y_el_caso_no_pasa(self):
        self.assertFalse(palabras_cumplidas({"inventario": True, "ventas": False}))

    def test_sin_palabras_exigidas_el_caso_pasa(self):
        self.assertTrue(palabras_cumplidas({}))

    def test_la_eficiencia_usa_solo_respuestas_sin_error(self):
        resultados = [
            _resultado("propietario activo", ("propietario activo",)),
            _resultado("otro tema", ("propietario activo",)),
            _resultado("", ("propietario activo",), error="timeout"),
        ]
        resumen = resumir(resultados, 70)
        self.assertEqual(resumen.aciertos, 1)
        self.assertEqual(resumen.respondidos, 2)
        self.assertEqual(resumen.eficiencia, 50)
        self.assertEqual(resumen.errores, 1)
        self.assertFalse(resumen.cumple_meta)

    def test_la_meta_se_cumple_en_el_limite(self):
        resultados = [
            _resultado("plan free", ("plan free",)),
            _resultado("plan free tambien", ("plan free",)),
        ]
        resumen = resumir(resultados, 70)
        self.assertEqual(resumen.eficiencia, 100)
        self.assertTrue(resumen.cumple_meta)


if __name__ == "__main__":
    unittest.main()
