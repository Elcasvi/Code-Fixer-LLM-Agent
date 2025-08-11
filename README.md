# Code-Fixer-LLM-Agent

Este proyecto integra herramientas de análisis, compilación y ajuste fino de modelos de lenguaje para la corrección y análisis de código fuente, combinando componentes en C++ y Python, así como notebooks para el fine-tuning de LLMs.


## Descripción de Componentes

### 1. CPP_Compiler

Contiene un compilador y analizador de código fuente en C++:

- **lexer/**: Implementa el análisis léxico (tokenización) del código fuente.
- **parser/**: Implementa el análisis sintáctico.
- **grammar/tok.txt**: Lista de tokens reconocidos por el compilador.
- **grammar/output.txt**: Secuencia de índices de tokens generados por el lexer.
- **grammar/token_mapper.py**: Script en Python que mapea los índices de `output.txt` a los nombres de tokens de `tok.txt`, imprimiendo la secuencia de tokens y respetando los saltos de línea (`NEWLINE`).

#### Uso de token_mapper.py

Desde la raíz del proyecto o desde la carpeta `CPP_Compiler/grammar/`:

```bash
python3 CPP_Compiler/grammar/token_mapper.py
```

El script imprimirá la secuencia de tokens correspondiente a los índices de `output.txt`, separando en líneas cada vez que encuentre el token `NEWLINE`.

### 2. fine-tuning-LLM

Contiene notebooks y scripts para el ajuste fino de modelos de lenguaje (LLM):

- **Notebooks**: Ejemplos y experimentos de fine-tuning usando distintos frameworks y datasets.
- **dataset/**: Conjuntos de datos y scripts para preparar los datos de entrenamiento.

#### Requisitos

Instala las dependencias necesarias para el fine-tuning con:

```bash
pip install -r fine-tuning-LLM/requirements.txt
```


