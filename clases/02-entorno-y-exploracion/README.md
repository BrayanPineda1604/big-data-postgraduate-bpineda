# Clase 02 — Entorno, datos sintéticos y exploración

[Índice del curso](../../README.md) · [Entorno](../../docs/entorno.md) · [Proyecto y evaluación](../../proyecto/README.md)

**Fin de semana 1 · Sábado · 7 h 30 min efectivos · RA1.**

## Objetivo

Preparar el entorno e interpretar el conjunto de pedidos.

## Preparación

Revisar las evidencias de la clase anterior y conservar las salidas de los laboratorios. Consultar las dependencias de ejecución en la guía de entorno.

## Bloques de la clase

| Segmento | Temas y actividades |
|---|---|
| Mañana · antes del receso | Entorno Python y Java, dependencias y verificación de instalación; registro de versiones e incidencias. Ejercicio 02.1. |
| Mañana · después del receso y antes del almuerzo | Generación de pedidos sintéticos, reproducibilidad y lectura de pedidos.csv y esperado.json. Ejercicio 02.2. |
| Tarde · después del almuerzo y antes del receso | Perfilado de tipos, nulos, duplicados, ciudades y categorías; diferencias entre duplicados y registros inválidos. Ejercicio 02.3. |
| Tarde · después del receso | Diccionario de datos, unidades y rangos; interpretación del perfil y revisión de la ficha del problema para E1. Cierre del ejercicio 02.3. |

## Ejercicios propuestos

### 02.1 — Verificación del entorno

Comprobar Python, Java y bibliotecas con la guía de entorno. Registrar versiones y cualquier incidencia.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 02.2 — Generación reproducible

Ejecutar el generador con 20 000 registros; revisar pedidos.csv y esperado.json. Explicar por qué aparecen más de 20 000 filas.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 02.3 — Perfil y diccionario

Calcular filas, tipos, nulos, duplicados, ciudades y categorías; describir columnas, unidades y rangos. Distinguir duplicados de registros inválidos.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

## Material y ejecución

[Programa académico](../../01_Programa_academico_Big_Data_64_horas.docx) · [Guía docente](../../02_Guia_academica_Big_Data_material_docente.docx). La guía docente contiene orientaciones y respuestas.

- [01_generar_datos.py](../../material_practico/01_generar_datos.py)

Desde `material_practico/`, con el entorno del curso activo y los prerrequisitos disponibles:

```sh
python 01_generar_datos.py --n 20000
```

## Entrega y revisión

E1: ficha del problema, perfil inicial y diccionario de datos.

E1: 10 % del curso. Se revisa corrección, evidencia, reproducibilidad y razonamiento; ejecutar sin explicar no completa la actividad.

## Trabajo autónomo

45 min después de esta clase: precisar el problema y completar el diccionario para E1.
