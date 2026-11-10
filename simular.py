import argparse
from pathlib import Path
import pandas as pd

DATOS = Path(__file__).resolve().parent / "datos"
COLUMNAS = ["demora_salida_min", "demora_llegada_min", "distancia_millas"]

def simular(escenario):
    datos = pd.read_csv(DATOS / "vuelos_nyc_2013.csv")
    ref = datos.loc[datos.lote == "referencia", COLUMNAS]
    ref.to_csv(DATOS / "referencia.csv", index=False)
    actual = datos.loc[datos.lote == "nuevo", COLUMNAS].copy() if escenario == "cambio" else ref.copy()
    if escenario == "error":
        actual.iloc[0, actual.columns.get_loc("distancia_millas")] = -100
    actual.to_csv(DATOS / "actual.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("escenario", choices=["igual", "cambio", "error"])
    simular(parser.parse_args().escenario)
