"""Genera Informe-modelo-rag-nexostock.pdf con formato de trabajo estudiantil APA 7.ª edición."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib.colors import black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "Informe-modelo-rag-nexostock.pdf"
RUNS = ROOT / "runs"
MARGIN = 2.54 * cm


class ArchitectureDiagram(Flowable):
    def __init__(self, width: float, height: float):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self) -> None:
        canvas = self.canv
        canvas.setStrokeColor(black)
        canvas.setFillColor(white)
        canvas.rect(0, 0, self.width, self.height, fill=1, stroke=1)

        def box(x, y, w, h, line1, line2=""):
            canvas.setFillColor(white)
            canvas.rect(x, y, w, h, fill=1, stroke=1)
            canvas.setFillColor(black)
            canvas.setFont("Times-Bold", 9)
            canvas.drawCentredString(x + w / 2, y + h / 2 + (4 if line2 else 0), line1)
            if line2:
                canvas.setFont("Times-Roman", 8)
                canvas.drawCentredString(x + w / 2, y + h / 2 - 8, line2)

        box(12, 138, 120, 40, "Usuario")
        box(156, 138, 140, 40, "Open WebUI", "puerto 8080")
        box(320, 138, 150, 40, "qwen2.5:7b-instruct", "modelo base")
        box(156, 62, 150, 46, "Colección NexoStock", "corte 500 / solape 50")
        box(330, 62, 140, 46, "Seis documentos", "conocimiento/")
        box(12, 12, 230, 34, "evaluate_rag.py", "50 casos, meta 70%")
        canvas.setStrokeColor(black)
        canvas.line(132, 158, 156, 158)
        canvas.line(296, 158, 320, 158)
        canvas.line(226, 138, 226, 108)
        canvas.line(306, 85, 330, 85)


def latest_run() -> dict | None:
    files = sorted(RUNS.glob("eval_*.jsonl"))
    if not files:
        return None
    records = []
    for line in files[-1].read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    if not records:
        return None
    total = len(records)
    errors = sum(1 for row in records if row.get("error"))
    answered = max(total - errors, 1)
    hits = sum(
        1
        for row in records
        if not row.get("error") and row.get("keywords_passed")
    )
    latencies = [row["latency_s"] for row in records if not row.get("error")]
    return {
        "file": files[-1].name,
        "total": total,
        "errors": errors,
        "rate": hits / answered * 100,
        "hits": hits,
        "answered": answered,
        "latency": sum(latencies) / len(latencies) if latencies else None,
    }


def styles():
    base = getSampleStyleSheet()
    common = dict(fontName="Times-Roman", fontSize=12, leading=24, textColor=black)
    base.add(ParagraphStyle(
        name="CoverLine",
        alignment=TA_CENTER,
        spaceAfter=0,
        **common,
    ))
    base.add(ParagraphStyle(
        name="CoverTitle",
        fontName="Times-Bold",
        fontSize=12,
        leading=24,
        alignment=TA_CENTER,
        textColor=black,
        spaceAfter=0,
    ))
    base.add(ParagraphStyle(
        name="H1",
        fontName="Times-Bold",
        fontSize=12,
        leading=24,
        alignment=TA_CENTER,
        textColor=black,
        spaceBefore=0,
        spaceAfter=0,
    ))
    base.add(ParagraphStyle(
        name="H2",
        fontName="Times-Bold",
        fontSize=12,
        leading=24,
        alignment=TA_LEFT,
        textColor=black,
        spaceBefore=0,
        spaceAfter=0,
    ))
    base.add(ParagraphStyle(
        name="Body",
        alignment=TA_LEFT,
        firstLineIndent=0.5 * inch,
        spaceAfter=0,
        **common,
    ))
    base.add(ParagraphStyle(
        name="IndexItem",
        alignment=TA_LEFT,
        firstLineIndent=0,
        leftIndent=0,
        spaceAfter=0,
        **common,
    ))
    base.add(ParagraphStyle(
        name="FigLabel",
        fontName="Times-Bold",
        fontSize=12,
        leading=24,
        alignment=TA_LEFT,
        textColor=black,
        spaceAfter=0,
    ))
    base.add(ParagraphStyle(
        name="FigTitle",
        fontName="Times-Italic",
        fontSize=12,
        leading=24,
        alignment=TA_LEFT,
        textColor=black,
        spaceAfter=0,
    ))
    base.add(ParagraphStyle(
        name="Note",
        fontName="Times-Roman",
        fontSize=12,
        leading=24,
        alignment=TA_LEFT,
        textColor=black,
        firstLineIndent=0,
        spaceAfter=0,
    ))
    base.add(ParagraphStyle(
        name="Reference",
        alignment=TA_LEFT,
        fontName="Times-Roman",
        fontSize=12,
        leading=24,
        textColor=black,
        firstLineIndent=-0.5 * inch,
        leftIndent=0.5 * inch,
        spaceAfter=0,
    ))
    return base


def celdas(filas: list[list[str]], encabezado: bool = True) -> list[list[Paragraph]]:
    cuerpo = ParagraphStyle(
        "Celda",
        fontName="Times-Roman",
        fontSize=8,
        leading=10,
        textColor=black,
    )
    titulo = ParagraphStyle(
        "CeldaTitulo",
        fontName="Times-Bold",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=black,
    )
    salida = []
    for indice, fila in enumerate(filas):
        estilo = titulo if encabezado and indice == 0 else cuerpo
        salida.append([Paragraph(texto, estilo) for texto in fila])
    return salida


def tabla(filas: list[list[str]], anchos: list[float]) -> Table:
    tabla_flow = Table(celdas(filas), colWidths=anchos, repeatRows=1)
    tabla_flow.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), white),
        ("TEXTCOLOR", (0, 0), (-1, -1), black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, black),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return tabla_flow


def casos_dataset() -> list[dict]:
    ruta = ROOT / "golden_dataset.jsonl"
    return [
        json.loads(linea)
        for linea in ruta.read_text(encoding="utf-8").splitlines()
        if linea.strip()
    ]


def number_page(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Times-Roman", 12)
    canvas.drawRightString(A4[0] - MARGIN, A4[1] - 1.5 * cm, str(doc.page))
    canvas.restoreState()


def build() -> None:
    run = latest_run()
    style = styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="Servicio de IA generativa con recuperación para el soporte de NexoStock",
        author="Kenny Bermúdez, Valeria Sanchez Pizo, Andrés Benavides, Yudy Alexandra Fuertes Cuasapud y Libio Belalcazar",
    )
    story = []

    story.append(Spacer(1, 3.2 * cm))
    story.append(Paragraph(
        "Servicio de IA generativa con recuperación para el soporte de NexoStock",
        style["CoverTitle"],
    ))
    story.append(Spacer(1, 1.4 * cm))
    for line in [
        "Kenny Bermúdez",
        "Valeria Sanchez Pizo",
        "Andrés Benavides",
        "Yudy Alexandra Fuertes Cuasapud",
        "Libio Belalcazar",
    ]:
        story.append(Paragraph(line, style["CoverLine"]))
    story.append(Spacer(1, 1.1 * cm))
    for line in [
        "Corporación Universitaria Unicomfacauca",
        "Programa de Ingeniería de Sistemas",
        "Diplomado CloudFord 5.0",
    ]:
        story.append(Paragraph(line, style["CoverLine"]))
    story.append(Spacer(1, 1.1 * cm))
    for line in [
        "Actividad 2, módulo 6",
        "Diego Fernando Rivera Vasquez",
        "19 de noviembre de 2026",
    ]:
        story.append(Paragraph(line, style["CoverLine"]))
    story.append(PageBreak())

    story.append(Paragraph("B. Índice", style["H1"]))
    for line in [
        "A. Portada",
        "B. Índice",
        "C. Introducción",
        "D. Problema que resuelve",
        "E. Definición del modelo",
        "F. Implementación y análisis de pruebas",
        "G. Conclusiones y trabajos futuros",
        "Referencias",
    ]:
        story.append(Paragraph(line, style["IndexItem"]))
    story.append(PageBreak())

    story.append(Paragraph("C. Introducción", style["H1"]))
    story.append(Paragraph(
        "Este informe presenta el servicio de soporte de NexoStock, desarrollado como actividad de inteligencia artificial generativa del Diplomado CloudFord 5.0. El servicio responde preguntas de uso del producto mínimo viable usando solo los documentos del proyecto. No reemplaza el sistema de inventario ni consulta PostgreSQL. Si la pregunta no está en la base, debe indicar que la función está fuera del alcance.",
        style["Body"],
    ))
    story.append(Paragraph(
        "La actividad sigue el esquema de recuperación aumentada (Lewis et al., 2020) visto en clase con Open WebUI (Open WebUI, s. f.) y el ejemplo de laboratorio (FerchoRV, s. f.). El servicio usa una colección de documentos, un modelo personalizado con prompt de sistema, un conjunto de 50 casos y el script evaluate_rag.py para medir latencia, errores y palabras clave.",
        style["Body"],
    ))
    story.append(Paragraph(
        "El documento define el problema de soporte, las decisiones del modelo, la evidencia de las pruebas de eficiencia y el conjunto de casos con el que se mide el chat. La meta de la actividad es obtener al menos 70% de eficiencia.",
        style["Body"],
    ))
    story.append(PageBreak())

    story.append(Paragraph("D. Problema que resuelve", style["H1"]))
    story.append(Paragraph(
        "El dueño o el empleado de un negocio pequeño necesita saber cómo registrar productos, mover existencias, vender sin dejar el stock en negativo y entender por qué no ve reportes. Esas reglas ya están en el producto mínimo viable: roles, planes Free, Basic y Pro, y el alcance que deja fuera la factura electrónica o las sucursales. El servicio las concentra en un chat de soporte para no depender de recorrer el código en cada duda.",
        style["Body"],
    ))
    story.append(Paragraph(
        "Sin esa ayuda, el propietario consulta de memoria quién puede crear un producto, quién registra una entrada y por qué un plan Free no muestra reportes. El empleado de ventas puede intentar cambiar un precio o registrar una entrada que su rol no permite. El chat debe decir qué rol sí puede hacerlo y no inventar un procedimiento.",
        style["Body"],
    ))
    story.append(Paragraph(
        "El asistente no informa el precio ni la existencia de un producto concreto. Esa cifra vive en el panel del negocio. Inventarla sería un error de soporte. Tampoco emite factura electrónica, no abre sucursales y no predice la demanda: esas funciones están fuera del alcance del producto mínimo viable.",
        style["Body"],
    ))
    story.append(PageBreak())

    story.append(Paragraph("E. Definición del modelo", style["H1"]))
    story.append(Paragraph("Modelo base y prompt", style["H2"]))
    story.append(Paragraph(
        "El modelo base es qwen2.5:7b-instruct (Qwen Team, 2024). El identificador del modelo personalizado en Open WebUI es nexostock-soporte. El prompt de sistema obliga a responder en español, a no inventar cifras, a respetar el rol (propietario, administrador de inventario o empleado de ventas) y a declarar fuera del alcance lo que el producto mínimo viable no hace. También impide revelar tokens, contraseñas o datos de otro negocio, porque cada sesión queda limitada al businessId del JWT.",
        style["Body"],
    ))
    story.append(Paragraph("Tabla 1", style["FigLabel"]))
    story.append(Paragraph("Parámetros del modelo nexostock-soporte", style["FigTitle"]))
    story.append(tabla([
        ["Parámetro", "Valor"],
        ["Modelo base", "qwen2.5:7b-instruct"],
        ["Identificador", "nexostock-soporte"],
        ["Corte", "500 tokens"],
        ["Solapamiento", "50 tokens"],
        ["Fragmentos recuperados", "4"],
        ["Temperatura de prueba", "0,2"],
        ["Meta de eficiencia", "70%"],
    ], [7.2 * cm, 8.3 * cm]))
    story.append(Paragraph(
        "<i>Nota.</i> El corte y el solapamiento se aplican al indexar la colección en Open WebUI 0.5.20.",
        style["Note"],
    ))
    story.append(Paragraph("Base de conocimiento y corte", style["H2"]))
    story.append(Paragraph(
        "La base tiene seis documentos: producto y roles, productos y categorías, inventario, ventas, reportes y arquitectura. Open WebUI los parte con un tamaño de corte de 500 tokens y un solapamiento de 50, y recupera cuatro fragmentos por pregunta. La temperatura de las pruebas es 0,2. La etiqueta de esa configuración es v1_chunk500_ov50.",
        style["Body"],
    ))
    story.append(Paragraph(
        "Open WebUI se publica en el puerto 8080. El puerto 3000 queda libre para el API Gateway de NexoStock. Ollama atiende en el puerto 11434 y solo lo usa Open WebUI.",
        style["Body"],
    ))
    story.append(Spacer(1, 12))
    story.append(KeepTogether([
        Paragraph("Figura 1", style["FigLabel"]),
        Paragraph(
            "Flujo del servicio de soporte con recuperación",
            style["FigTitle"],
        ),
        Spacer(1, 8),
        ArchitectureDiagram(15 * cm, 5.8 * cm),
        Paragraph(
            "<i>Nota.</i> El usuario consulta Open WebUI; el modelo base responde con fragmentos de la colección y evaluate_rag.py mide los 50 casos por la API.",
            style["Note"],
        ),
    ]))
    story.append(PageBreak())

    story.append(Paragraph("F. Implementación y análisis de pruebas", style["H1"]))
    story.append(Paragraph("Procedimiento", style["H2"]))
    story.append(Paragraph(
        "La evidencia tiene dos capas. La primera comprueba la regla de eficiencia sin levantar el modelo: cinco pruebas unitarias del dominio. La segunda es el conjunto de 50 casos que evaluate_rag.py envía al modelo nexostock-soporte por la API de Open WebUI. Un caso de esa segunda capa es eficiente cuando la API no falla y la respuesta contiene todas las palabras clave. La meta es al menos 70%.",
        style["Body"],
    ))
    story.append(Paragraph("Pruebas unitarias de la eficiencia", style["H2"]))
    story.append(Paragraph(
        "Se ejecutó python -m unittest evaluacion.tests.test_eficiencia. Las cinco pruebas terminaron en OK. Comprueban que la palabra clave no distingue mayúsculas, que falta una clave para reprobar el caso, que un caso sin claves exigidas se acepta, que un error de API no entra en el porcentaje y que la meta se evalúa en el límite.",
        style["Body"],
    ))
    story.append(Paragraph("Tabla 2", style["FigLabel"]))
    story.append(Paragraph("Resultado de las pruebas unitarias de eficiencia", style["FigTitle"]))
    story.append(tabla([
        ["Prueba", "Criterio", "Resultado"],
        ["Mayúsculas", "Propietario equivale a propietario", "OK"],
        ["Clave faltante", "Si falta una palabra, el caso no pasa", "OK"],
        ["Sin claves", "Sin palabras exigidas, el caso pasa", "OK"],
        ["Error de API", "El error no cuenta como acierto", "OK"],
        ["Meta", "Dos aciertos de dos cumplen 70%", "OK"],
    ], [3.6 * cm, 8.4 * cm, 3.5 * cm]))
    captura = ROOT / "evidencias" / "pruebas-unitarias.png"
    if captura.exists():
        story.append(Spacer(1, 10))
        story.append(Paragraph("Figura 2", style["FigLabel"]))
        story.append(Paragraph(
            "Salida de las cinco pruebas unitarias de eficiencia",
            style["FigTitle"],
        ))
        story.append(Image(str(captura), width=14.8 * cm, height=14.8 * cm * 392 / 1106))
        story.append(Paragraph(
            "<i>Nota.</i> La salida corresponde a la ejecución local de las pruebas de dominio. No usa Open WebUI.",
            style["Note"],
        ))
    story.append(Paragraph("Conjunto de 50 casos", style["H2"]))
    casos = casos_dataset()
    nombres = {
        "roles": "Roles y planes",
        "productos": "Productos",
        "inventario": "Inventario",
        "ventas": "Ventas",
        "reportes": "Reportes",
        "arquitectura": "Arquitectura",
    }
    conteo: dict[str, int] = {}
    for caso in casos:
        conteo[caso["category"]] = conteo.get(caso["category"], 0) + 1
    filas_conteo = [["Categoría", "Casos"]]
    for clave in nombres:
        filas_conteo.append([nombres[clave], str(conteo.get(clave, 0))])
    filas_conteo.append(["Total", str(len(casos))])
    story.append(Paragraph(
        f"El archivo golden_dataset.jsonl reúne {len(casos)} casos. Cada uno trae la pregunta, la respuesta esperada y las palabras que la respuesta del modelo debe contener. Hay casos de rechazo, como la factura electrónica, las sucursales y la predicción de demanda.",
        style["Body"],
    ))
    story.append(Paragraph("Tabla 3", style["FigLabel"]))
    story.append(Paragraph("Distribución del conjunto de prueba", style["FigTitle"]))
    story.append(tabla(filas_conteo, [10 * cm, 5.5 * cm]))
    filas_casos = [["Caso", "Categoría", "Pregunta", "Palabras clave"]]
    for caso in casos:
        palabras = ", ".join(caso.get("required_keywords") or [])
        filas_casos.append([
            caso["id"].replace("case_", ""),
            nombres.get(caso["category"], caso["category"]),
            caso["prompt"].replace("&", "&amp;"),
            palabras.replace("&", "&amp;"),
        ])
    story.append(Spacer(1, 8))
    story.append(Paragraph("Tabla 4", style["FigLabel"]))
    story.append(Paragraph("Casos del conjunto de prueba y palabras clave exigidas", style["FigTitle"]))
    story.append(tabla(filas_casos, [1.5 * cm, 3.2 * cm, 6.6 * cm, 4.2 * cm]))
    story.append(Paragraph(
        "<i>Nota.</i> La tabla reproduce el dataset usado por evaluate_rag.py. Un caso cuenta como acierto solo si aparecen todas las palabras de la última columna.",
        style["Note"],
    ))
    story.append(Paragraph("Resultado de la API", style["H2"]))
    if run is None:
        story.append(Paragraph(
            "La corrida de los 50 casos contra el modelo todavía no está en la carpeta runs. Por eso este informe no publica un porcentaje de eficiencia del chat. Ese dato se incorpora al ejecutar evaluate_rag.py y volver a generar el PDF. La evidencia ya disponible es la de la Tabla 2, la Figura 2 y el conjunto completo de la Tabla 4.",
            style["Body"],
        ))
    else:
        latency = f"{run['latency']:.2f} s" if run["latency"] is not None else "sin datos"
        story.append(Paragraph(
            f"En la corrida {run['file']}, {run['hits']} de {run['answered']} respuestas contuvieron las palabras clave ({run['rate']:.1f}%). Hubo {run['errors']} errores de API y la latencia media fue {latency}. La meta de 70% {'se cumplió' if run['rate'] >= 70 else 'queda pendiente de ajuste'}.",
            style["Body"],
        ))
    story.append(PageBreak())

    story.append(Paragraph("G. Conclusiones y trabajos futuros", style["H1"]))
    story.append(Paragraph(
        "El servicio queda definido sobre el producto real: roles, planes, reglas de stock, ventas con precio del catálogo y clave de idempotencia, y el límite de lo que NexoStock todavía no hace.",
        style["Body"],
    ))
    story.append(Paragraph(
        "Si el porcentaje de palabras clave queda bajo 70%, se ajusta el prompt o el conjunto de casos y se repite la corrida con otra etiqueta. Las capturas de Open WebUI se incorporan al cerrar la actividad. Open WebUI usa el puerto 8080 y el API Gateway de NexoStock usa el puerto 3000. La clave de API permanece en el archivo de entorno local y no forma parte de este informe.",
        style["Body"],
    ))

    story.append(PageBreak())
    story.append(Paragraph("Referencias", style["H1"]))
    references = [
        "FerchoRV. (s. f.). <i>ejemplo-rag-openwebui</i> [Repositorio de código]. GitHub. https://github.com/FerchoRV/ejemplo-rag-openwebui",
        "Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S. y Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. <i>Advances in Neural Information Processing Systems, 33</i>, 9459-9474. https://arxiv.org/abs/2005.11401",
        "Open WebUI. (s. f.). <i>Open WebUI</i> (Versión 0.5.20) [Programa de computador]. https://github.com/open-webui/open-webui",
        "Qwen Team. (2024). <i>Qwen2.5 technical report</i>. arXiv. https://arxiv.org/abs/2412.15115",
    ]
    for reference in references:
        story.append(Paragraph(reference, style["Reference"]))

    doc.build(story, onFirstPage=number_page, onLaterPages=number_page)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
