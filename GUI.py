#!/usr/bin/python

from easygui import *
import sys
import TriedroFrenet_Evoluta

if __name__ == "__main__":

    msgbox("Hola! Este programa dibuja una curva en R^3 junto a su Triedro de Frenet y su evoluta.")

    while 1:

        correcto = False

        while not correcto:

            x_t = enterbox("Introduce la función x(t)", "Función x(t)")
            if x_t is None: sys.exit(-1)

            y_t = enterbox("Introduce la función y(t)", "Función y(t)")
            if y_t is None: sys.exit(-1)

            z_t = enterbox("Introduce la función z(t)", "Función z(t)")
            if z_t is None: sys.exit(-1)

            num_puntos = enterbox("Introduce el número de muestras", "Número de muestras")
            if num_puntos is None: sys.exit(-1)

            inicio = enterbox("Introduce el inicio del intervalo", "Inicio del intervalo")
            if inicio is None: sys.exit(-1)

            final = enterbox("Introduce final del intervalo", "Final del intervalo")
            if final is None: sys.exit(-1)

            if x_t is "" or y_t is "" or z_t is "" or num_puntos is "" or inicio is "" or final is "":
                correcto = False
                msgbox("Te has dejado algún dato sin introducir")
            else:
                correcto = True

        mensaje = "Confirma que los datos introducidos son correctos:"
        mensaje += "\nx(t) = " + x_t
        mensaje += "\ny(t) = " + y_t
        mensaje += "\nz(t) = " + z_t

        mensaje += "\nNúmero de muestras = " + num_puntos

        mensaje += "\nInicio del intervalo = " + inicio
        mensaje += "\nFinal del intervalo = " + final


        titulo = "Confirma los datos"
        

        # Muestra un diálogo de confirmación
        # Si acepta, formar lista de argumentos y lanzar el programa
        # Si no, volver a pedir datos

        if ccbox(mensaje, titulo):
            argumentos = ["./TriedroFrenet_Evoluta", x_t, y_t, z_t, num_puntos, inicio, final]
            TriedroFrenet_Evoluta.main(argumentos)
