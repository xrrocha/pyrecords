# PyRecords

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

## Configuración del Proyecto

### Requisitos

- Python 3.10+

### Instalación para Desarrollo

1. Clonar el repositorio:
   ```bash
   git clone git@github.com:xrrocha/pyrecords.git
   cd pyrecords
   ```

2. Crear entorno virtual:
   ```bash
   python -m venv .venv
   ```

3. Activar entorno virtual:
   ```bash
   # Linux/macOS
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

4. Instalar dependencias de desarrollo:
   ```bash
   pip install -e ".[dev]"
   ```

## Licencia

MIT
