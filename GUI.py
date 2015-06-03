#!/usr/bin/python

from easygui import *
import sys
import TriedroFrenet_Evoluta

if __name__ == "__main__":
    # Mensaje de bienvenida
    bienvenida = "Hola! Este programa dibuja una curva en R^3 junto a su Triedro de Frenet y su evoluta."
    bienvenida += "\n\nPuedes usar todo tipo de funciones matemáticas gracias a Sympy."
    bienvenida += "\n\nAlgunos ejemplos son: sin(t), cos(t), tan(t), abs(t), la potencia **, integrate(expr,liminf,limsup)..."
    bienvenida += "\n\nEso sí, ¡escribe todo en función de t!"
    bienvenida += "\n\nEl código (el cual es libre) se encuentra en mi perfil de GitHub @analca3"
    msgbox(bienvenida, "Bienvenido", "Aceptar")

    # Condición para la ejecución de la GUI
    corriendo = False
    while not corriendo:

        # Condición para controlar la introducción de los datos
        correcto = False
        valorCampos = []
        while not correcto:
            mensaje = "Introduce la curva a dibujar en función de t"
            titulo = "Introduce la curva"
            nombreCampos = ["x(t)","y(t)","z(t)","Número de muestras","Inicio del intervalo","Final del intervalo"]
            valorCampos = multenterbox(mensaje,titulo,nombreCampos,valorCampos)

            # Si se ha pulsado cancelar, salir
            # Si todos los datos están introducidor, seguir
            # Si no, volver a pedir datos
            if valorCampos is None:
                sys.exit(-1)
            elif all(valorCampos):
                correcto = True
            else:
                correcto = False
                msgbox("Te has dejado algún dato sin introducir")

        mensaje = "Confirma que los datos introducidos son correctos:"
        mensaje += "\nx(t) = " + valorCampos[0]
        mensaje += "\ny(t) = " + valorCampos[1]
        mensaje += "\nz(t) = " + valorCampos[2]

        mensaje += "\nNúmero de muestras = " + valorCampos[3]

        mensaje += "\nInicio del intervalo = " + valorCampos[4]
        mensaje += "\nFinal del intervalo = " + valorCampos[5]


        titulo = "Confirma los datos"
        opciones = ("Perfecto!", "Corregir")

        # Mostrar un diálogo de confirmación
        # Si acepta, formar lista de argumentos y lanzar el programa
        # Si no, volver a pedir datos

        if ccbox(mensaje, titulo, opciones):
            corriendo = True

            # Añadir el nombre del programa para que funcione igual que directamente desde la CLI
            argumentos = ["./TriedroFrenet_Evoluta"] + valorCampos
            TriedroFrenet_Evoluta.main(argumentos)
