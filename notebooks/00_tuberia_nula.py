import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # La Tubería Nula

    > *"Para entender qué hace algo, primero hay que ver qué pasa cuando no hace nada."*

    Vamos a copiar registros de un archivo CSV a otro. Sin filtrar. Sin transformar.
    Solo **leer → escribir**. La tubería más simple posible.

    ¿Por qué empezar así? Porque esta operación "trivial" nos enseña:

    1. Qué es un **registro** (una fila de datos, representada como diccionario)
    2. Qué significa **streaming** (procesar uno a la vez, sin cargar todo en memoria)
    3. La forma básica de toda tubería: **origen → destino**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Nuestros datos: Pablo Espresso ☕

    Tenemos un archivo `entrada.csv` con productos de una cafetería ficticia:
    """)
    return


@app.cell
def _():
    # Veamos el contenido del archivo
    with open("entrada.csv", encoding="utf-8") as f:
        contenido = f.read()
    print(contenido)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Intento 1: El enfoque "ingenuo" 💀

    Parece fácil, ¿no? Leemos línea por línea, separamos por comas...
    """)
    return


@app.cell
def _():
    def copiar_ingenuo(entrada: str, salida: str) -> int:
        """Intento ingenuo de copiar CSV. ¿Funcionará?"""
        with open(entrada, encoding="utf-8") as archivo_entrada:
            lineas = archivo_entrada.readlines()

        # Primera línea = encabezados
        encabezados = lineas[0].strip().split(",")
        print(f"Encabezados detectados: {encabezados}")

        registros = []
        for linea in lineas[1:]:
            valores = linea.strip().split(",")
            registro = dict(zip(encabezados, valores))
            registros.append(registro)
            print(f"Registro: {registro}")

        return len(registros)

    # Ejecutemos...
    copiar_ingenuo("entrada.csv", "salida_ingenua.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ¡Problema! 🔥

    Mira el campo `descripcion` del primer registro. Dice `"Café negro"`, pero debería decir `"Café negro, intenso"`!

    **¿Qué pasó?** La coma *dentro* del valor confundió a `split(",")`.
    El formato CSV usa comillas para proteger valores con comas, pero nuestro código no sabe eso.

    Podríamos arreglar esto... pero tendríamos que manejar:
    - Comillas dentro de comillas (`"\"`)
    - Saltos de línea dentro de valores
    - Diferentes encodings (UTF-8, Latin-1...)

    **Alguien ya resolvió esto.** Se llama el módulo `csv`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Intento 2: Usando `csv.DictReader` 💡

    Python incluye un módulo `csv` que maneja todas las complejidades del formato:
    """)
    return


@app.cell
def _():
    import csv

    def mostrar_registros(entrada: str) -> None:
        """Lee y muestra registros correctamente."""
        with open(entrada, newline="", encoding="utf-8") as archivo_entrada:
            lector = csv.DictReader(archivo_entrada)
            for registro in lector:
                print(dict(registro))  # Convertimos a dict normal para visualizar

    mostrar_registros("entrada.csv")
    return (csv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ¡Ahora sí! `"Café negro, intenso"` aparece completo.

    Observa algo importante: usamos un **`for`** sobre el lector.
    No cargamos todos los registros en una lista. Los procesamos *uno a uno*.

    Esto es **streaming**: si el archivo tuviera 10 millones de registros,
    seguiríamos usando la misma cantidad de memoria.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## La Tubería Nula: Copiar sin modificar

    Ahora sí, nuestra tubería completa. Lee de `entrada.csv`, escribe a `salida.csv`, sin cambiar nada:
    """)
    return


@app.cell
def _(csv):
    Registro = dict[str, str]

    def copiar_csv(entrada: str, salida: str) -> int:
        """
        Copia registros de un CSV a otro, sin modificación.

        Esta es la "tubería nula": origen → destino, sin filtros ni transformaciones.
        Procesa en streaming: un registro a la vez, sin cargar todo en memoria.
        """
        with open(entrada, newline="", encoding="utf-8") as archivo_entrada:
            lector = csv.DictReader(archivo_entrada)

            with open(salida, "w", newline="", encoding="utf-8") as archivo_salida:
                escritor = None
                cuenta = 0

                for registro in lector:
                    if escritor is None:
                        # Primer registro: inicializamos el escritor con los nombres de campo
                        escritor = csv.DictWriter(
                            archivo_salida, fieldnames=registro.keys()
                        )
                        escritor.writeheader()

                    escritor.writerow(registro)
                    cuenta += 1

        return cuenta

    # Ejecutamos la copia
    total = copiar_csv("entrada.csv", "salida.csv")
    print(f"Registros copiados: {total}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Verificación: ¿Son iguales?
    """)
    return


@app.cell
def _():
    # Comparamos los archivos
    with open("entrada.csv", encoding="utf-8") as f1:
        original = f1.read()

    with open("salida.csv", encoding="utf-8") as f2:
        copia = f2.read()

    if original == copia:
        print("✅ Los archivos son idénticos")
    else:
        print("❌ Los archivos difieren")
        print("\n--- Original ---")
        print(original)
        print("\n--- Copia ---")
        print(copia)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ¿Qué aprendimos?

    1. **Registro = diccionario**: Cada fila es un `dict[str, str]` donde las claves son los encabezados
    2. **Streaming**: Procesamos uno a la vez con `for registro in lector`
    3. **No reinventar la rueda**: `csv.DictReader` maneja las complejidades del formato
    4. **La tubería nula**: `origen → destino` es la forma más simple — y la base de todo lo que sigue

    ---

    ### ¿Y ahora qué?

    Esta tubería no hace nada útil... todavía. En las siguientes lecciones agregaremos:

    - **Filtros**: Seleccionar solo algunos registros (`filtrar`)
    - **Transformaciones**: Modificar o agregar campos (`derivar`, `seleccionar`)
    - **Otros formatos**: Bases de datos, JSON, archivos de ancho fijo

    La estructura siempre será la misma: **origen → [filtros/transformaciones] → destino**
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
