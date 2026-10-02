# Verificación de la integración — 2 de octubre de 2026

[Índice](../README.md)

Se verificaron los 12 archivos del respaldo local mediante SHA-256 contra `kit/fuentes.json`. Los originales y las salidas están excluidos del repositorio. No se volvieron a descargar fuentes remotas durante esta integración.

Se ejecutaron correctamente `perfil`, `calidad`, `consultas`, `benchmark`, `geografia`, `clima` y `modelo` con el entorno local disponible en macOS. Esta prueba no equivale a validar una instalación desde cero con requirements.txt en cada plataforma.

| Control observado | Resultado |
|---|---|
| Perfil | 57 columnas |
| AGROSAVIA | 92 738 registros; 92 727 aptos para pH; 11 en revisión |
| Enlace territorial pendiente | 2 138 registros |
| EVA | 166 732 registros; 159 616 aptos para cociente |
| Integración | 107 620 grupos; 55 498 con pH agregado |
| Geografía | 1 122 municipios y 15 intersecciones de las muestras IGAC |
| NASA | 31 días; 67,69 mm acumulados |
| Persistencia 2024 | 15 267 pares; MAE 0,791782 t/ha |
| Persistencia 2025 | 15 503 pares; MAE 0,815013 t/ha |

Los dos formatos del benchmark produjeron conteos iguales y sumas dentro de la tolerancia del script. Sus tiempos dependen del equipo y no constituyen una garantía de rendimiento.

Los scripts Python se revisaron sintácticamente. **Spark por lotes y streaming no se ejecutaron en esta integración porque no hay un Java disponible en el entorno utilizado. Windows y la práctica visual de QGIS tampoco se validaron.** Las consignas respectivas describen actividades y controles esperados, no resultados certificados de esta ejecución.

Los controles de calidad del corte están disponibles en [controles_referencia.json](../kit/controles_referencia.json). El libro y las presentaciones en elaboración no se incorporaron a esta versión.
