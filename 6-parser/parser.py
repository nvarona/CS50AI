# File: parser.py
# Author: Natxo Varona
# Date: 22/09/2024
# Description: Desarrollar una IA para analizar oraciones y extraer frases nominales.
#
# He implementado las dos funciones que faltaban en el programa y con las caracteristicas descritas en el enunciado:
# preprocess(sentence) y np_chunk(tree)
#
# Algunas notas sobre las implementaciones:
# La función preprocess tiene que convertir una oración en una lista de palabras en minúsculas,
# eliminando las que no contienen caracteres alfabéticos (para quitar puntuación o números)
#
# La función np_check() debe encontrar y devolver las frases nominales ("NP") en el árbol.
# Una "chunk" de frase nominal es una subárbol con la etiqueta "NP" que no contiene otros subárboles con "NP"
#
# Ejecucion: $ python3 parser.py <directorio/archivo.txt>
#
# El resto del código va debajo de aquí ---------------------------------------

import nltk
import sys
import string

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det AdjP N | NP PP | Adj NP | NP Conj NP | N N | Det N PP
VP -> V | V NP | V NP PP | V PP | Adv VP | VP Adv | VP Conj VP | V NP NP
PP -> P NP | P Det N PP
AdjP -> Adj | Adj AdjP
AdvP -> Adv | Adv AdvP
TempP -> P NP
"""

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never" | "home"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were" | "walk" | "came"
"""

print("Entrenando ...")
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read().strip() # Eliminar espacios en blanco y saltos de línea

    # Otherwise, get sentence as input
    else:
        s = input("Oración: ")

    # Convert input into list of words
    s = preprocess(s)
    print("Oración preprocesada:", s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(f"Error: {e}")
        # Identificar las palabras que no están en la gramática
        unknown_words = [word for word in s if word not in grammar.productions()]
        if unknown_words:
            print(f"Palabras no reconocidas en la gramática: {', '.join(unknown_words)}")
        return
    if not trees:
        print("No se pudo analizar la oración.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        print("Fragmentos de frases nominales")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Convertir la oración a minúsculas
    sentence = sentence.lower()

    # Eliminar el punto final si existe
    sentence = sentence.rstrip('.,!?')

    # Manejar casos especiales
    # sentence = sentence.replace("sat down", "sat_down")

    # Dividir la oración en palabras
    words = sentence.split()

    # Filtrar palabras que no contienen al menos un carácter alfabético
    filtered_words = [word for word in words if any(c.isalpha() for c in word)]

    return filtered_words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    for subtree in tree.subtrees():
        # Si el subárbol tiene la etiqueta "NP"
        if subtree.label() == "NP":
            # Verificar si este NP contiene otros NPs (frases nominales)
            if not any(child.label() == "NP" for child in subtree if isinstance(child, nltk.Tree)):
                chunks.append(subtree)

    return chunks

if __name__ == "__main__":
    main()
