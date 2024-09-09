# File: degrees.py
# Author: Natxo Varona
# Date: 17/08/2024
# Description: Escriba un programa que determine cuántos “grados de separación” hay entre dos actores.
#
# He implementado las tres funciones que faltaban en el modulo:
# shortest_path()
#
# Requirements: Python 3.9 o superior
# Dependencies: csv, sys, collections, util y heapq
#
# License: MIT License (o la licencia que consideres apropiada)
#
# Change log:
#
# Ejecucion: $ python3 degress.py large
#
# El resto del código va debajo de aquí ---------------------------------------

import csv
import sys
import heapq

from collections import deque
from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

# Función original BFS (Breadth-First Search)
def shortest_path_bfs(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Inicializar la cola para BFS --------------------------------------
    queue = deque([(source, [])])
    visited = set()

    while queue:
        current_person, path = queue.popleft()

        # Marcar el nodo como visitado
        visited.add(current_person)

        # Obtener todas las conexiones de la persona actual
        for movie_id, person_id in neighbors_for_person(current_person):
            if person_id == target:
                return path + [(movie_id, person_id)]

            if person_id not in visited:
                queue.append((person_id, path + [(movie_id, person_id)]))

    # Si no se encuentra el camino
    return None

# Implementación DFS (Depth-First Search)
def shortest_path_dfs(source, target):
    def dfs(current_person, path, visited):
        if current_person == target:
            return path
        visited.add(current_person)
        for movie_id, person_id in neighbors_for_person(current_person):
            if person_id not in visited:
                result = dfs(person_id, path + [(movie_id, person_id)], visited)
                if result:
                    return result
        return None

    return dfs(source, [], set())

# Implementación GBFS (Greedy Best-First Search)
def shortest_path_gbfs(source, target):
    def heuristic(person):
        # Esta es una heurística simple. En un caso real, podrías usar una mejor estimación.
        return 1 if person != target else 0

    heap = [(heuristic(source), source, [])]
    visited = set()

    while heap:
        _, current_person, path = heapq.heappop(heap)
        if current_person == target:
            return path
        visited.add(current_person)
        for movie_id, person_id in neighbors_for_person(current_person):
            if person_id not in visited:
                new_path = path + [(movie_id, person_id)]
                heapq.heappush(heap, (heuristic(person_id), person_id, new_path))

    return None

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data ...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name Actor 1: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name Actor 2: "))
    if target is None:
        sys.exit("Person not found.")

    #path = shortest_path_bfs(source, target)
    path = shortest_path_dfs(source, target)
    #path = shortest_path_gbfs(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

if __name__ == "__main__":
    main()
