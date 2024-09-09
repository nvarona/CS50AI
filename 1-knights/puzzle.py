# File: puzzle.py
# Author: Natxo Varona (nvarona@hotmail.com)
# Date: 24/07/2024
# Description: Añade conocimientos a las bases de conocimientos knowledge0, knowledge1,
# knowledge2, y knowledge3 para resolver los siguientes acertijos, rellenar las base de datos.
# He puesto en castellano los textos que se imprimen en pantalla.
#
# Requirements: Python 3.9 o superior
# Dependencies: logic.py
#
# License: MIT License (o la licencia que consideres apropiada)
#
# Change log:
#
# Ejecucion: $ python3 puzzle.py
#
# El resto del código va debajo de aquí ---------------------------------------
#

from logic import *

# Símbolos globales
AKnight = Symbol("A es un caballero")
AKnave = Symbol("A es un bribón")
BKnight = Symbol("B es un caballero")
BKnave = Symbol("B es un bribón")
CKnight = Symbol("C es un caballero")
CKnave = Symbol("C es un bribón")

# Acertijo 0
knowledge0 = And(
    # A es un caballero o un bribón, pero no ambos
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # Si A es un caballero, su afirmación es verdadera; si es un bribón, es falsa
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Acertijo 1
knowledge1 = And(
    # A y B son caballeros o bribones, pero no ambos
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # Si A es un caballero, su afirmación es verdadera; si es un bribón, es falsa
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Acertijo 2
knowledge2 = And(
    # A y B son caballeros o bribones, pero no ambos
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # Si A es un caballero, su afirmación es verdadera; si es un bribón, es falsa
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # Si B es un caballero, su afirmación es verdadera; si es un bribón, es falsa
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Acertijo 3
knowledge3 = And(
    # A, B y C son caballeros o bribones, pero no ambos
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    # A dijo "Soy un caballero" o "Soy un bribón"
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    # Si B es un caballero, sus afirmaciones son verdaderas; si es un bribón, son falsas
    Implication(BKnight, And(Implication(AKnight, AKnave), CKnave)),
    Implication(BKnave, Not(And(Implication(AKnight, AKnave), CKnave))),
    # Si C es un caballero, su afirmación es verdadera; si es un bribón, es falsa
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")

if __name__ == "__main__":
    main()
