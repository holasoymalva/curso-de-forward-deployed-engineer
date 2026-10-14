#!/usr/bin/env python3
"""
rag_minimo.py: Implementación de Generación Aumentada por Recuperación (RAG)
utilizando exclusivamente la biblioteca estándar de Python (TF-IDF léxico).
Indexa documentación del caso de estudio de Distribuidora Halcón y responde preguntas.
"""

import os
import sys
import math
import re
from collections import Counter

# Importar el cliente LLM local
directorio_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, directorio_actual)
from cliente_llm_simulado import ClienteLLM

STOPWORDS_ESPANOL = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con",
    "no", "una", "su", "al", "lo", "como", "mas", "más", "pero", "sus", "le", "ya", "o", "este",
    "si", "porque", "esta", "son", "entre", "esta", "cuando", "muy", "sin", "sobre", "tambien", "también"
}

def tokenizar(texto: str) -> list:
    """Extrae palabras en minúsculas filtrando signos de puntuación y stopwords."""
    palabras = re.findall(r"\b[a-záéíóúñ0-9_-]{3,}\b", texto.lower())
    return [p for p in palabras if p not in STOPWORDS_ESPANOL]

class MotorRAGMinimo:
    def __init__(self):
        self.fragmentos = []  # Lista de dicts: {"id": int, "fuente": str, "texto": str, "tokens": list}
        self.idf = {}         # Mapeo: palabra -> inverse document frequency
        self.llm = ClienteLLM()

    def agregar_documento(self, fuente: str, texto_completo: str, tamano_chunk_lineas: int = 4):
        """Divide un documento en fragmentos por párrafos preservando el origen."""
        parrafos = [p.strip() for p in texto_completo.split("\n\n") if len(p.strip()) > 40]
        
        for idx, parrafo in enumerate(parrafos):
            tokens = tokenizar(parrafo)
            if tokens:
                self.fragmentos.append({
                    "id": len(self.fragmentos),
                    "fuente": fuente,
                    "texto": parrafo,
                    "tokens": tokens
                })

    def compilar_indice(self):
        """Calcula los pesos IDF (Inverse Document Frequency) sobre todos los fragmentos indexados."""
        total_docs = len(self.fragmentos)
        if total_docs == 0:
            return

        conteo_documentos = Counter()
        for doc in self.fragmentos:
            palabras_unicas = set(doc["tokens"])
            for p in palabras_unicas:
                conteo_documentos[p] += 1

        for palabra, conteo in conteo_documentos.items():
            # Fórmula IDF estándar con suavizado
            self.idf[palabra] = math.log((total_docs + 1) / (conteo + 1)) + 1.0

    def buscar(self, consulta: str, top_k: int = 3) -> list:
        """Puntúa y recupera los fragmentos más relevantes usando similitud coseno simplificada TF-IDF."""
        tokens_consulta = tokenizar(consulta)
        if not tokens_consulta:
            return []

        puntuaciones = []

        for doc in self.fragmentos:
            tf = Counter(doc["tokens"])
            total_palabras = len(doc["tokens"])
            score = 0.0

            for t in tokens_consulta:
                if t in tf:
                    # TF normalizado * IDF
                    tf_norm = tf[t] / total_palabras
                    score += tf_norm * self.idf.get(t, 1.0)

            if score > 0:
                puntuaciones.append((score, doc))

        # Ordenar de mayor a menor relevancia
        puntuaciones.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in puntuaciones[:top_k]]

    def responder_pregunta(self, pregunta: str) -> str:
        """Pipeline RAG completo: Recupera contexto, ensambla prompt e invoca al LLM."""
        mejores_fragmentos = self.buscar(pregunta, top_k=2)

        # Si el score de los fragmentos recuperados es nulo o irrelevante para la consulta
        tokens_q = tokenizar(pregunta)
        tiene_coincidencias_reales = False
        if mejores_fragmentos:
            for f in mejores_fragmentos:
                if any(t in f["tokens"] for t in tokens_q if t not in {"que", "cual", "cuales", "como", "donde"}):
                    tiene_coincidencias_reales = True
                    break

        if not mejores_fragmentos or not tiene_coincidencias_reales:
            return "Información no disponible en la documentación oficial de Distribuidora Halcón."
        else:
            partes = []
            for f in mejores_fragmentos:
                partes.append(f"[{f['fuente']}]:\n{f['texto']}")
            contexto_str = "\n\n".join(partes)

        prompt_sistema = (
            "Eres un asistente técnico para Distribuidora Halcón. "
            "Responde a la pregunta del usuario utilizando EXCLUSIVAMENTE los fragmentos de contexto proporcionados abajo. "
            "Si el contexto no contiene la respuesta, di textualmente: 'Información no disponible en la documentación oficial'."
        )

        prompt_usuario = (
            f"--- CONTEXTO RECUPERADO ---\n{contexto_str}\n--- FIN DE CONTEXTO ---\n\n"
            f"Pregunta: {pregunta}"
        )

        mensajes = [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]

        print(f"\n[RAG Retrieval]: Se recuperaron {len(mejores_fragmentos)} fragmentos relevantes.")
        for idx, f in enumerate(mejores_fragmentos, 1):
            print(f"  {idx}. Fuente: {f['fuente']} (Tokens: {len(f['tokens'])})")

        return self.llm.completar_chat(mensajes, temperatura=0.0)

def cargar_documentacion_halcon(motor: MotorRAGMinimo):
    """Carga los documentos reales generados en el módulo 05 o un corpus base embebido."""
    ruta_modulo05 = os.path.abspath(
        os.path.join(directorio_actual, "../../05-descubrimiento-con-clientes/ejemplos")
    )

    archivos_a_cargar = [
        "documento_descubrimiento_halcon.md",
        "transcripcion_entrevista_halcon.md"
    ]

    cargados = 0
    for nombre in archivos_a_cargar:
        ruta = os.path.join(ruta_modulo05, nombre)
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                motor.agregar_documento(nombre, f.read())
            cargados += 1

    if cargados == 0:
        # Corpus de respaldo si se ejecuta aislado
        corpus_respaldo = """
        Distribuidora Halcón opera con tres almacenes principales: Monterrey (MTY), Guadalajara (GDL) y Ciudad de México (CDMX).
        El almacén de Monterrey abastece a 600 tiendas del noreste y presenta un retraso de 4 horas en el cierre nocturno del ERP.

        Las políticas de crédito estipulan que los clientes tienen un límite revolvente de 15 a 30 días, con corte los días viernes.
        Las devoluciones de abarrotes secos (arroz, frijol) deben tramitarse antes de 7 días naturales con sello del supervisor.
        """
        motor.agregar_documento("politicas_halcon_respaldo.md", corpus_respaldo)

    motor.compilar_indice()

if __name__ == "__main__":
    print("=== Inicializando Motor RAG Mínimo (Zero-Dependency) ===")
    rag = MotorRAGMinimo()
    cargar_documentacion_halcon(rag)
    print(f"Total de fragmentos indexados: {len(rag.fragmentos)}")

    preguntas_ejemplo = [
        "¿Cuáles son los almacenes de Halcón y qué problemática tienen?",
        "¿Cuál es el plazo para devoluciones de abarrotes secos?"
    ]

    for p in preguntas_ejemplo:
        print(f"\n==================================================")
        print(f"Pregunta: {p}")
        respuesta = rag.responder_pregunta(p)
        print(f"\nRespuesta del Asistente RAG:\n{respuesta}")
