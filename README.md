# PyRecords

<p align="center">
  <img src="docs/img/pyrecords-logo.png" alt="PyRecords Logo" width="200">
</p>

**Framework pedagógico de copia de registros en Python**

## Descripción

PyRecords es un framework declarativo para copiar registros entre diferentes formatos (CSV, bases de datos, archivos de ancho fijo, etc.). Más allá de su utilidad práctica, PyRecords es un **proyecto pedagógico** diseñado para enseñar principios de diseño de frameworks a desarrolladores Python hispanohablantes.

## Propósito Educativo

Este proyecto demuestra el patrón de diseño **puntos calientes / puntos congelados** (*hot spots / frozen spots*):

- **Puntos Congelados**: El algoritmo invariante que define el framework. En PyRecords, es el ciclo de copia:
  ```
  abrir fuente y destino
  para cada registro en fuente:
      si filtro acepta registro:
          transformar registro
          escribir en destino
  cerrar fuente y destino
  ```

- **Puntos Calientes**: Los puntos de extensión donde los usuarios conectan su comportamiento específico:
  - `Fuente`: De dónde vienen los registros
  - `Filtro`: Cuáles registros procesar
  - `Transformador`: Cómo modificar los registros
  - `Destino`: A dónde van los registros

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        Copiador                             │
│  ┌─────────┐  ┌────────┐  ┌───────────────┐  ┌───────────┐ │
│  │ Fuente  │→ │ Filtro │→ │ Transformador │→ │  Destino  │ │
│  └─────────┘  └────────┘  └───────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Formatos Soportados

- CSV (archivos delimitados)
- Archivos de ancho fijo
- Bases de datos (SQLite, PostgreSQL vía DB-API)

## Configuración

PyRecords soporta configuración declarativa vía YAML:

```yaml
fuente: !csv
  archivo: datos/entrada.csv
  campos:
    - { indice: 0, nombre: id, formato: !entero }
    - { indice: 1, nombre: nombre, formato: !texto }

filtro: !expresion "estado == 'activo'"

transformador: !renombrar
  campos: { id: ID, nombre: NOMBRE }

destino: !base_de_datos
  tabla: CLIENTES
  campos: [ID, NOMBRE]
```

## Configuración del Entorno

### Requisitos

- Python 3.10+
- Git

### Instalación para Desarrollo

1. **Clonar el repositorio:**
   ```bash
   git clone git@github.com:xrrocha/pyrecords.git
   cd pyrecords
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

### Flujo de Desarrollo

Usa `tareas.py` para las operaciones comunes (funciona en Windows, macOS y Linux):

```bash
python tareas.py dev      # Editar notebooks en Marimo
python tareas.py build    # Exportar a WASM
python tareas.py serve    # Servir WASM localmente (http://localhost:8000)
python tareas.py help     # Ver todos los comandos
```

#### Comandos manuales (referencia)

Si prefieres ejecutar los comandos directamente:

```bash
# Editar notebooks (desde directorio notebooks/)
cd notebooks
marimo edit 00_tuberia_nula.py

# Exportar a WASM
cd notebooks
marimo export html-wasm 00_tuberia_nula.py -o ../dist --mode run

# Servir localmente
python -m http.server --directory dist 8000
```

Opciones de modo para export:
- `--mode run`: Solo lectura (estudiantes ven output)
- `--mode edit`: Estudiantes pueden modificar y re-ejecutar celdas

### Estructura del Proyecto

```
pyrecords/
├── notebooks/           # Lecciones Marimo
│   ├── 00_tuberia_nula.py
│   └── entrada.csv      # Datos de ejemplo
├── src/pyrecords/       # Código del framework
├── tests/               # Pruebas
├── dist/                # Export WASM (gitignored)
├── requirements.txt     # Dependencias Python
├── tareas.py            # Script de tareas (cross-platform)
└── README.md
```

### Agregar Dependencias

Al instalar nuevos paquetes, **siempre** actualizar `requirements.txt`:

```bash
pip install <paquete>
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Agregar dependencia: <paquete>"
```

## Licencia

MIT
