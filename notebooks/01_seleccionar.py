import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Seleccionar: Eligiendo y Reordenando Columnas

    > *"La misma información, diferente forma."*

    En la lección anterior copiamos registros sin modificarlos.
    Ahora aprenderemos nuestra primera **transformación**: `seleccionar`.

    `seleccionar` nos permite:
    - Elegir qué columnas incluir
    - Cambiar el orden de las columnas
    - Descartar columnas que no necesitamos

    La forma del registro cambia. El contenido permanece igual.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recordatorio: Nuestros datos

    Seguimos trabajando con el menú de Pablo Espresso ☕
    """)
    return


@app.cell
def _():
    import csv

    # Veamos qué tenemos
    with open("entrada.csv", encoding="utf-8") as f:
        contenido = f.read()
    print(contenido)
    return (csv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Columnas actuales: `id, producto, precio, descripcion`

    ¿Y si necesitamos otro orden? Por ejemplo, para un reporte donde
    la descripción va primero:

    ```
    descripcion, producto, precio, id
    ```

    Esto es exactamente lo que hace `seleccionar`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## La transformación `seleccionar`

    La idea es simple: dado un registro, creamos uno nuevo con solo las claves que queremos,
    en el orden que queremos.
    """)
    return


@app.cell
def _():
    def seleccionar(registro: dict, campos: list[str]) -> dict:
        """
        Crea un nuevo registro con solo los campos especificados, en ese orden.

        Args:
            registro: El registro original
            campos: Lista de campos a incluir, en el orden deseado

        Returns:
            Nuevo registro con solo los campos seleccionados
        """
        return {campo: registro[campo] for campo in campos}

    # Ejemplo
    ejemplo = {"id": "1", "producto": "Espresso", "precio": "2.50", "descripcion": "Café negro, intenso"}
    campos_deseados = ["descripcion", "producto", "precio", "id"]

    resultado = seleccionar(ejemplo, campos_deseados)
    print(f"Original: {ejemplo}")
    print(f"Seleccionado: {resultado}")
    return (seleccionar,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ¡Observa! El contenido es el mismo, pero las claves están en diferente orden.

    En Python 3.7+, los diccionarios preservan el orden de inserción.
    Esto nos permite controlar exactamente cómo aparecen las columnas en el CSV de salida.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Aplicando `seleccionar` a toda la tubería

    Ahora integremos esto en nuestra copia de registros:
    """)
    return


@app.cell
def _(csv, seleccionar):
    def copiar_con_seleccion(entrada: str, salida: str, campos: list[str]) -> int:
        """
        Copia registros seleccionando y reordenando columnas.
        """
        with open(entrada, newline="", encoding="utf-8") as archivo_entrada:
            lector = csv.DictReader(archivo_entrada)

            with open(salida, "w", newline="", encoding="utf-8") as archivo_salida:
                escritor = csv.DictWriter(archivo_salida, fieldnames=campos)
                escritor.writeheader()

                cuenta = 0
                for registro in lector:
                    nuevo = seleccionar(registro, campos)
                    escritor.writerow(nuevo)
                    cuenta += 1

        return cuenta

    # Ejecutar
    campos_salida = ["descripcion", "producto", "precio", "id"]
    total = copiar_con_seleccion("entrada.csv", "salida.csv", campos_salida)
    print(f"Registros procesados: {total}")
    return (copiar_con_seleccion,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Verificación
    """)
    return


@app.cell
def _():
    # Veamos el resultado
    with open("salida.csv", encoding="utf-8") as f:
        print(f.read())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Las columnas ahora aparecen en el orden que especificamos.
    El **contenido** es idéntico; la **forma** cambió.

    ---

    ## ¿Qué aprendimos?

    | Concepto | Descripción |
    |----------|-------------|
    | `seleccionar` | Elige y reordena columnas |
    | Dict comprehension | `{k: d[k] for k in campos}` preserva orden |
    | Forma vs Contenido | Transformamos estructura, no valores |

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🎯 Ejercicio: Tu turno

    Modifica la función `mi_seleccion` para que el archivo `ejercicio.csv` tenga
    las columnas en este orden:

    ```
    producto, precio
    ```

    (Solo dos columnas: producto y precio, sin id ni descripcion)

    <details>
    <summary>💡 Pista 1</summary>

    La lista de campos determina qué columnas aparecen y en qué orden.
    </details>

    <details>
    <summary>💡 Pista 2</summary>

    ```python
    campos = ["producto", "precio"]
    ```
    </details>
    """)
    return


@app.cell
def _(csv, seleccionar):
    # ═══════════════════════════════════════════════════════════════
    # TU CÓDIGO AQUÍ
    # Cambia la lista de campos para incluir solo "producto" y "precio"
    # ═══════════════════════════════════════════════════════════════

    mis_campos = ["id", "producto", "precio", "descripcion"]  # ← Modifica esta línea

    # ═══════════════════════════════════════════════════════════════

    # Este código usa tu selección
    with open("entrada.csv", newline="", encoding="utf-8") as f_in:
        lector = csv.DictReader(f_in)
        with open("ejercicio.csv", "w", newline="", encoding="utf-8") as f_out:
            escritor = csv.DictWriter(f_out, fieldnames=mis_campos)
            escritor.writeheader()
            for reg in lector:
                escritor.writerow(seleccionar(reg, mis_campos))

    print("Archivo ejercicio.csv creado. Verifica abajo ↓")
    return (mis_campos,)


@app.cell
def _(mo):
    # Verificación automática
    def verificar_ejercicio():
        esperado = ["producto", "precio"]

        try:
            with open("ejercicio.csv", encoding="utf-8") as f:
                lineas = f.readlines()
                if not lineas:
                    return mo.md("⏳ El archivo está vacío. Ejecuta la celda anterior.")
                obtenido = lineas[0].strip().split(",")
        except FileNotFoundError:
            return mo.md("⏳ Archivo no encontrado. Ejecuta la celda anterior primero.")

        if obtenido == esperado:
            # Mostrar el contenido completo
            with open("ejercicio.csv", encoding="utf-8") as f:
                contenido = f.read()

            return mo.md(f"""
## ✅ ¡Excelente!

Las columnas son exactamente `producto, precio`.

**Tu resultado:**
```
{contenido}```

**Lo que practicaste:**
- Seleccionar solo algunas columnas (descartar las demás)
- El poder del dict comprehension para filtrar claves
            """)
        else:
            return mo.md(f"""
## ❌ Todavía no...

| Esperado | Obtenido |
|----------|----------|
| `{esperado}` | `{obtenido}` |

**Revisa**: ¿Tu lista `mis_campos` contiene solo `"producto"` y `"precio"`?
            """)

    verificar_ejercicio()
    return (verificar_ejercicio,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## ¿Y ahora qué?

    Ya sabemos:
    - **Copiar** registros (tubería nula)
    - **Seleccionar** columnas (elegir y reordenar)

    En la siguiente lección: **`filtrar`** — elegir qué *filas* procesar.

    La tubería crece:
    ```
    origen → [seleccionar] → destino     ← Hoy
    origen → [filtrar] → destino         ← Próximo
    origen → [filtrar → seleccionar] → destino  ← Combinando
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
