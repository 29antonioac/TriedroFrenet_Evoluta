# TriedroFrenet_Evoluta
Pequeño programa que para una curva en el espacio calcula su Triedo de Frenet y su evoluta

A partir de la parametrización de una curva en función de **t**, un número de puntos y el inicio y fin del intervalo,
dibujaremos usando OpenGL dicha curva con su Triedro de Frenet y su evoluta.

## GUI

He creado una pequeña GUI para los principiantes. Si tienes python por defecto para ejecutar archivos .py,
sólo debes hacer doble click en **GUI.py**. En otro caso, ejecuta en tu consola de comandos

```
python /ruta/del/archivo/GUI.py
```

Sigue los pasos y dibujarás sin problemas :).

## CLI

Si te gusta más la línea de comandos, ejecuta directamente **TriedroFrenet_Evoluta.py** de esta manera:

```
python /ruta/del/archivo/TriedroFrenet_Evoluta.py <x(t)> <y(t)> <z(t)> <número de puntos> <inicio> <fin>
```

## Dentro del programa

Una vez ejecutado y con la curva en pantalla, tenemos estos controles:

- **N/M** para controlar la velocidad de la animación.
- **E** para dibujar la evoluta.
