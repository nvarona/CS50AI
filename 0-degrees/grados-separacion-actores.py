import csv
import sys
from collections import deque

class GradosSeparacion:
    def __init__(self, archivo_personas, archivo_peliculas):
        self.personas = {}
        self.peliculas = {}
        self.cargar_datos(archivo_personas, archivo_peliculas)

    def cargar_datos(self, archivo_personas, archivo_peliculas):
        with open(archivo_personas, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.personas[row["id"]] = {
                    "name": row["name"],
                    "movies": set()
                }

        with open(archivo_peliculas, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.peliculas[row["id"]] = {
                    "title": row["title"],
                    "stars": set()
                }
                for persona_id in row["stars"].split(","):
                    self.personas[persona_id]["movies"].add(row["id"])
                    self.peliculas[row["id"]]["stars"].add(persona_id)

    def encontrar_actor(self, nombre):
        for persona_id, persona in self.personas.items():
            if persona["name"].lower() == nombre.lower():
                return persona_id
        return None

    def encontrar_conexion(self, inicio, fin):
        if inicio == fin:
            return []

        visitados = set()
        cola = deque([(inicio, [])])

        while cola:
            (nodo, path) = cola.popleft()
            if nodo not in visitados:
                visitados.add(nodo)

                for pelicula_id in self.personas[nodo]["movies"]:
                    for actor_id in self.peliculas[pelicula_id]["stars"]:
                        if actor_id == fin:
                            return path + [(nodo, pelicula_id, actor_id)]
                        if actor_id not in visitados:
                            cola.append((actor_id, path + [(nodo, pelicula_id, actor_id)]))

        return None

    def imprimir_conexion(self, conexion):
        if conexion is None:
            print("No se encontró conexión.")
            return

        print(f"{len(conexion)} grados de separación.")
        for i, (actor1, pelicula, actor2) in enumerate(conexion, 1):
            nombre_actor1 = self.personas[actor1]["name"]
            nombre_actor2 = self.personas[actor2]["name"]
            titulo_pelicula = self.peliculas[pelicula]["title"]
            print(f"{i}: {nombre_actor1} y {nombre_actor2} protagonizaron {titulo_pelicula}")

def main():
    if len(sys.argv) != 2:
        sys.exit("Uso: python grados.py [conjunto_datos]")

    conjunto_datos = sys.argv[1]
    archivo_personas = f"{conjunto_datos}/people.csv"
    archivo_peliculas = f"{conjunto_datos}/movies.csv"

    print("Cargando datos...")
    grafo = GradosSeparacion(archivo_personas, archivo_peliculas)
    print("Datos cargados.")

    while True:
        nombre1 = input("Nombre: ").strip()
        if not nombre1:
            break
        actor1 = grafo.encontrar_actor(nombre1)
        if actor1 is None:
            print("Actor no encontrado.")
            continue

        nombre2 = input("Nombre: ").strip()
        if not nombre2:
            break
        actor2 = grafo.encontrar_actor(nombre2)
        if actor2 is None:
            print("Actor no encontrado.")
            continue

        conexion = grafo.encontrar_conexion(actor1, actor2)
        grafo.imprimir_conexion(conexion)

if __name__ == "__main__":
    main()
