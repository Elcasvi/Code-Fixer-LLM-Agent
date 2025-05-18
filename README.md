# Code-Fixer-LLM-Agent

Este proyecto integra herramientas de análisis, compilación y ajuste fino de modelos de lenguaje para la corrección y análisis de código fuente, combinando componentes en C++ y Python, así como notebooks para el fine-tuning de LLMs.

## Estructura del Proyecto

```
.
├── CPP_Compiler/
│   ├── main.cpp
│   ├── CMakeLists.txt
│   ├── lexer/
│   │   ├── Lexer.cpp, Lexer.h, FileReader.cpp, FileReader.h
│   ├── parser/
│   │   ├── Parser.cpp, Parser.h
│   ├── grammar/
│   │   ├── tok.txt
│   │   ├── output.txt
│   │   └── token_mapper.py
├── fine-tuning-LLM/
│   ├── fineTunning.ipynb, fine_tuning.ipynb, unsloth-fine-tuning.ipynb, etc.
│   ├── requirements.txt
│   └── dataset/
│       ├── small_datset.jsonl, code_patch_datasets.xlsx, convert_merge_dataset.py
├── README.md
```

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

## Contribución

1. Haz un fork del repositorio.
2. Crea una rama para tu feature o fix.
3. Haz tus cambios y realiza commits descriptivos.
4. Haz pull request a la rama principal.

## Licencia

MIT
