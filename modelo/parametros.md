# Parámetros del modelo nexostock-soporte

## Modelo

- Modelo base: `qwen2.5:7b-instruct`.
- ID en Open WebUI: `nexostock-soporte`.
- Juez opcional: `qwen2.5:7b-instruct`. Si `JUDGE_MODEL` queda vacío, la corrida mide latencia, errores y palabras clave.

## Recuperación

- Colección: `NexoStock soporte`.
- Archivos: los seis markdown de `conocimiento/`.
- `CHUNK_SIZE=500` tokens.
- `CHUNK_OVERLAP=50` tokens.
- `RAG_TOP_K=4` fragmentos por pregunta.
- Etiqueta de la corrida: `v1_chunk500_ov50`.

Esos valores están en `docker-compose.yml` para Open WebUI 0.5.20. Si se cambia el corte, hay que reprocesar la colección y usar otro `RUN_TAG`.

## Generación

- Temperatura de evaluación: 0.2, fija en `evaluate_rag.py`.
- El prompt de sistema está en `modelo/system_prompt.md`. Limita el dominio, prohíbe inventar cifras y pide decir que la función está fuera del alcance cuando no está en la base.

## Eficiencia

Un caso cuenta como correcto cuando la API no falla y la respuesta contiene todas las `required_keywords`. La meta es al menos 70%. El porcentaje sale de `runs/` al ejecutar `python evaluate_rag.py` y queda escrito en el PDF al regenerar el informe.
