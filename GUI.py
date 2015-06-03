#!/usr/bin/python

from easygui import *
import sys

if __name__ == "__main__":

    msgbox("Hola! Este programa dibuja una curva en R^3 junto a su Triedro de Frenet y su evoluta.")

    while 1:
        
        correcto = False

        while not correcto:
            
            x_t = enterbox("Introduce la función x(t)", "Función x(t)")
            y_t = enterbox("Introduce la función y(t)", "Función y(t)")
            z_t = enterbox("Introduce la función z(t)", "Función z(t)")

            num_puntos = enterbox("Introduce el número de muestras", "Número de muestras")

            inicio = enterbox("Introduce el inicio del intervalo", "Inicio del intervalo")
            final = enterbox("Introduce final del intervalo", "Final del intervalo")
            
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
        falta = False

        if not falta and not ccbox(mensaje, titulo):     # show a Continue/Cancel dialog
                pass  # user chose Cancel
        else:
                sys.exit(0)           # user chose Continue
