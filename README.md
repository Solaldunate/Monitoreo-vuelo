# Monitoreo de vuelos de Nueva York (2013)

Práctica de validación de datos y detección de cambios con Evidently. El CSV de la práctica contiene 36.000 registros repartidos en tres lotes de 12.000. Se analizan las demoras de salida y llegada, en minutos, y la distancia, en millas. Fuente de los datos de vuelos: [nycflights13](https://nycflights13.tidyverse.org/).

## Ejecutar la práctica

Desde la carpeta del proyecto, con Python 3.12:

```powershell
python -m pip install -r requirements.txt
python simular.py igual
python monitorear.py
```

Abre `public/index.html` para ver las medias y acceder al informe de Evidently. Para repetir la comparación, sustituye `igual` por `cambio` o `error` en el comando de simulación y vuelve a ejecutar `monitorear.py`.

| Escenario | Datos comparados | Resultado esperado |
| --- | --- | --- |
| `igual` | La referencia y una copia exacta. | La validación pasa y Evidently no detecta cambios. |
| `cambio` | La referencia y el lote `nuevo`. | La validación pasa. El informe permite ver en qué variables Evidently detecta cambios. |
| `error` | La referencia y una copia con una distancia de −100 millas en el primer registro. | La validación falla antes de generar un informe nuevo. |

## Qué demuestran las pruebas

1. Una distancia negativa incumple una regla de calidad. Una distribución de demoras distinta puede ser válida. Una demora negativa indica que el vuelo salió o llegó antes de lo previsto.
2. `datos/referencia.csv` se obtiene siempre del lote `referencia`. Usar el mismo lote como base permite comparar cada escenario con los mismos valores.
3. En `cambio` se usa el lote `nuevo`. La demora media de salida pasa de 9,88 a 21,35 minutos y la de llegada de 6,01 a 16,64 minutos. Se mantienen las tres columnas y las 12.000 filas por lote. El informe de Evidently determina qué cambios superan su umbral.
4. GitHub Actions puede terminar correctamente aunque Evidently detecte cambios, porque el flujo publica el informe de cualquier lote que pase la validación.
5. Una distancia inválida hace fallar el paso de validación. Como la publicación depende de ese paso, GitHub Actions omite el despliegue y Pages conserva el último informe válido.
6. Las pruebas comparan distribuciones de datos. Para medir la precisión de un modelo harían falta sus predicciones y los resultados observados.

## Demostración en GitHub

En el repositorio, selecciona **Settings → Pages → Source → GitHub Actions**. El flujo `Vuelos NYC - Evidently y Pages` se ejecuta al subir cambios a `main`.

Para demostrar los escenarios, genera el lote actual con `simular.py` y sube el cambio de `datos/actual.csv` en un commit por escenario. En **Actions**, comprueba que los lotes válidos se publiquen y que el inválido bloquee la publicación. Termina restaurando `igual` y verifica que Pages publique el informe corregido.
