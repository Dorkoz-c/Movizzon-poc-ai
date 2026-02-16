 PoC: Sistema de Consultas IA para Documentación Interna
Esta Prueba de Concepto (PoC) utiliza un enfoque RAG (Retrieval-Augmented Generation) para responder preguntas basadas en manuales, PDFs y textos con datos numéricos o caracteres especiales almacenados de forma local.

1. Requisitos Previos
Python 3.9 o superior.

OpenAI API Key: Necesaria para los modelos de lenguaje y embeddings.

Documentos: Archivos PDF dentro de la carpeta /docs.

2. Instalación y Configuración
Sigue estos pasos para preparar el entorno local:

Clonar el repositorio
Bash

git clone https://github.com/Dorkoz-c/Movizzon-poc-ai.git
cd poc-ai-fastapi
Crear y activar el entorno virtual
Bash

# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate

Para que el sistema funcione con soporte de IA y documentos, ejecuta los siguientes comandos en tu terminal (con el entorno virtual activo):

Framework de la API:
pip install fastapi

Servidor para ejecutar la API:
pip install uvicorn

Conector de OpenAI:
pip install -U langchain-openai

Librerías de soporte para documentos y vectores:
pip install langchain pypdf chromadb python-dotenv

Estructura de Archivos del Proyecto

Movizzon-poc-ai/
├── docs/                # <-- COLOCA AQUÍ TUS PDFs
│   └── manual_tecnico.pdf
├── main.py              # Código fuente de la API
├── .env                 # Tu llave de OpenAI
├── .gitignore           # Archivos excluidos de Git
└── requirements.txt     # Lista de dependencias

Configuración de la IA
Antes de iniciar, asegúrate de que tu archivo .env tenga tu llave de acceso:
OPENAI_API_KEY=tu_llave_de_openai_aqui


Cómo iniciar la PoC
Una vez instaladas las librerías y colocados los documentos en la carpeta docs/, inicia el servicio con:
uvicorn main:app --reload

Acceso y Visualización en el Navegador
Una vez que ejecutas el comando uvicorn main:app --reload, el servidor se iniciará localmente.

Puerto por defecto: 8000

Dirección local: http://127.0.0.1:8000

Interfaz de Pruebas (Swagger UI)
FastAPI genera automáticamente una interfaz visual para probar la IA sin usar herramientas externas. Para acceder, abre tu navegador y ve a:

http://127.0.0.1:8000/docs

Pasos para probar en el navegador:

Busca el botón azul del endpoint POST /ask.

Haz clic en el botón "Try it out".

En el cuadro de texto (JSON), escribe tu pregunta:


Resolución de Problemas de Puerto
Si al ejecutar el comando recibes un error que dice [Errno 98] Address already in use, significa que el puerto 8000 está ocupado por otra aplicación.

Puedes cambiar el puerto fácilmente usando este comando:

Bash

uvicorn main:app --reload --port 8080
En ese caso, deberás acceder a: http://127.0.0.1:8080/docs

