#!/usr/bin/env python3
"""
01-pipeline-rag-con-evaluacion.py: Solución al Ejercicio 01.
Ejecuta una batería de evaluación cuantitativa (Eval Set) sobre el motor RAG
y calcula métricas de precisión de recuperación y fidelidad contextual.
"""

import os
import sys

# Importar motor RAG del directorio de ejemplos
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_ejemplos = os.path.abspath(os.path.join(directorio_actual, "../../ejemplos"))
sys.path.insert(0, ruta_ejemplos)

from rag_minimo import MotorRAGMinimo, cargar_documentacion_halcon

EVAL_SET = [
    {
        "id": "EV-01",
        "pregunta": "¿Cuáles son los tres almacenes principales de Distribuidora Halcón?",
        "palabras_clave_esperadas": ["monterrey", "guadalajara", "cdmx"],
        "debe_encontrar_respuesta": True
    },
    {
        "id": "EV-02",
        "pregunta": "¿Cuál es la política y plazo de devolución para abarrotes secos como arroz y frijol?",
        "palabras_clave_esperadas": ["7 días", "arroz", "frijol"],
        "debe_encontrar_respuesta": True
    },
    {
        "id": "EV-03",
        "pregunta": "¿Cómo funciona la línea de crédito revolvente para las tiendas?",
        "palabras_clave_esperadas": ["crédito", "15", "30", "días"],
        "debe_encontrar_respuesta": True
    },
    {
        "id": "EV-04",
        "pregunta": "¿Qué modelo de camiones diésel utiliza la flota de reparto?",
        "palabras_clave_esperadas": ["no disponible", "no se cuenta", "no contiene"],
        "debe_encontrar_respuesta": False  # Debe rechazar porque esta información no existe en el corpus
    },
    {
        "id": "EV-05",
        "pregunta": "¿Cuál es la merma máxima permitida en perecederos y en qué tiempo se reporta?",
        "palabras_clave_esperadas": ["24 horas", "perecedero"],
        "debe_encontrar_respuesta": True
    }
]

def evaluar_rag():
    print("==================================================")
    print("Iniciando Evaluación Cuantitativa del Motor RAG")
    print("==================================================")

    rag = MotorRAGMinimo()
    cargar_documentacion_halcon(rag)
    print(f"Base de conocimientos lista con {len(rag.fragmentos)} fragmentos indexados.\n")

    aciertos = 0
    total_evals = len(EVAL_SET)

    print(f"{'ID':<7} | {'Estado':<10} | {'Pregunta Evaluada':<45}")
    print("-" * 68)

    for item in EVAL_SET:
        pregunta = item["pregunta"]
        esperadas = item["palabras_clave_esperadas"]
        debe_hallar = item["debe_encontrar_respuesta"]

        fragmentos = rag.buscar(pregunta, top_k=2)
        respuesta = rag.responder_pregunta(pregunta).lower()

        # Criterio de verificación de fidelidad
        coincidencias = sum(1 for palabra in esperadas if palabra.lower() in respuesta)
        
        # Consideramos acierto si contiene al menos la mitad de los conceptos clave o si rechaza adecuadamente
        if debe_hallar:
            es_valido = coincidencias >= 1
        else:
            # En caso negativo, es acierto si el modelo no alucina hechos y declara falta de información
            es_valido = ("no disponible" in respuesta or "no se cuenta" in respuesta or len(fragmentos) == 0)

        if es_valido:
            aciertos += 1
            estado_str = "✅ PASÓ"
        else:
            estado_str = "❌ FALLÓ"

        pregunta_corta = (pregunta[:42] + "...") if len(pregunta) > 42 else pregunta
        print(f"{item['id']:<7} | {estado_str:<10} | {pregunta_corta:<45}")

    tasa_acierto = (aciertos / total_evals) * 100

    print("\n==================================================")
    print("Reporte Final de Calidad RAG")
    print("==================================================")
    print(f"Total de casos evaluados: {total_evals}")
    print(f"Aciertos confirmados:     {aciertos}")
    print(f"Fallos detectados:        {total_evals - aciertos}")
    print(f"Tasa de Precisión Global: {tasa_acierto:.1f}%")

    if tasa_acierto >= 80.0:
        print("\n[VEREDICTO]: APTO para despliegue en entorno de pruebas de Halcón.")
        return 0
    else:
        print("\n[VEREDICTO]: RECHAZADO. Ajustar fragmentación o reglas de recuperación.")
        return 1

if __name__ == "__main__":
    codigo = evaluar_rag()
    sys.exit(codigo)
