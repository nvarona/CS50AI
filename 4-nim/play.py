# File: play.py & nim.py
# Author: Natxo Varona
# Date: 17/08/2024
# Description: Desarrollar una IA que aprenda a jugar a Nim mediante aprendizaje de refuerzo.
#
# He implementado las tres funciones que faltaban en el modulo nim.py:
# get_q_value(), update_q_value(), best_future_reward() y choose_action()
#
# Requirements: Python 3.9 o superior
# Dependencies: nim.py
#
# License: MIT License (o la licencia que consideres apropiada)
#
# Change log:
#
# Ejecucion: $ python3 play.py
#
# El resto del código va debajo de aquí ---------------------------------------

from nim import train, play

ai = train(10000)
play(ai)
