"""Punto de entrada. Aquí se arman las piezas; la regla de eficiencia vive en el dominio."""

from pathlib import Path

from evaluacion.aplicacion.evaluar import evaluar
from evaluacion.dominio import resumir
from evaluacion.infraestructura.archivos import BitacoraJsonl, DatasetJsonl
from evaluacion.infraestructura.chat import ClienteChat, GeneradorOpenWebUI, JuezOmitido, JuezOpenWebUI
from evaluacion.infraestructura.entorno import cargar_configuracion
from evaluacion.presentacion import ObservadorConsola, imprimir_resumen

RAIZ = Path(__file__).resolve().parent


def main() -> None:
    configuracion = cargar_configuracion(RAIZ)
    configuracion.exigir_clave()
    casos = DatasetJsonl(configuracion.dataset).cargar()
    print(
        f"Ejecutando {len(casos)} casos | Modelo: {configuracion.modelo} | "
        f"Tag: {configuracion.etiqueta}"
    )
    cliente = ClienteChat(configuracion.base_url, configuracion.api_key)
    generador = GeneradorOpenWebUI(cliente, configuracion.modelo)
    if configuracion.juez:
        juez = JuezOpenWebUI(cliente, configuracion.juez)
    else:
        juez = JuezOmitido()
    resultados = evaluar(casos, generador, juez, ObservadorConsola())
    archivo = BitacoraJsonl(configuracion.salida, configuracion.etiqueta).guardar(resultados)
    imprimir_resumen(resumir(resultados, configuracion.meta), archivo)


if __name__ == "__main__":
    main()
