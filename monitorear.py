import csv
from pathlib import Path
import math
import os
import sys

def validar(ruta):
    with ruta.open(newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        if lector.fieldnames != ["demora_salida_min", "demora_llegada_min", "distancia_millas"]:
            sys.exit(f"{ruta}: columnas inesperadas")
        filas = []
        for fila in lector:
            valores = {}
            for campo in lector.fieldnames:
                try:
                    numero = float(fila[campo])
                except (ValueError, TypeError):
                    numero = math.nan
                if not math.isfinite(numero) or (campo == "distancia_millas" and numero <= 0):
                    sys.exit(f"{ruta}, fila {lector.line_num}, {campo}: valor invalido {fila[campo]}")
                valores[campo] = numero
            filas.append(valores)
    if len(filas) < 100:
        sys.exit(f"{ruta}: menos de 100 vuelos")
    return filas

def main():
    ref = validar(Path("datos/referencia.csv"))
    act = validar(Path("datos/actual.csv"))
    os.environ.setdefault("EVIDENTLY_DO_NOT_TRACK", "1")
    import pandas as pd
    from evidently import DataDefinition, Dataset, Report
    from evidently.presets import DataDriftPreset

    ref, act = pd.DataFrame(ref), pd.DataFrame(act)
    definicion = DataDefinition(numerical_columns=list(ref.columns))
    resultado = Report([DataDriftPreset()]).run(
        current_data=Dataset.from_pandas(act, data_definition=definicion),
        reference_data=Dataset.from_pandas(ref, data_definition=definicion),
    )
    salida = Path("public")
    salida.mkdir(exist_ok=True)
    resultado.save_html(str(salida / "comparacion.html"))
    medias = pd.DataFrame({"Referencia": ref.mean(), "Actual": act.mean()})
    commit = os.getenv("GITHUB_SHA", "local")
    (salida / "index.html").write_text(
        '<!doctype html><html lang="es"><meta charset="utf-8"><h1>Vuelos NYC 2013</h1>'
        f'<p>Referencia: {len(ref)} vuelos. Actual: {len(act)} vuelos.</p>'
        + medias.round(2).to_html()
        + f'<p>Commit: {commit}</p><a href="comparacion.html">Ver informe de Evidently</a>',
        encoding="utf-8",
    )

if __name__ == "__main__":
    main()
