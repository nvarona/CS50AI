# File: pagerank.py
# Author: Natxo Varona
# Date: 08/08/2024
# Description: He implementado las tres funciones que faltaban:
# transition_model(), sample_pagerank() y iterate_pagerank().
#
# Aquí dejo una breve explicación de cada funcion que he programado:
# transition_model: Calcula la distribución de probabilidad para la siguiente página a visitar,
#                   considerando el factor de amortiguación y los enlaces de la página actual.
# sample_pagerank: Estima los valores de PageRank mediante muestreo, visitando páginas según el
#                  modelo de transición y contando las visitas.
# iterate_pagerank: Calcula los valores de PageRank iterativamente hasta que convergen, utilizando
#                   la fórmula de PageRank.
#
# El resto del código va debajo de aquí ---------------------------------------

import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()
    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}
    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page. With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}
    total_pages = len(corpus)

    # Probability of randomly choosing any page
    random_prob = (1 - damping_factor) / total_pages

    # Add random probability to all pages
    for p in corpus:
        distribution[p] = random_prob

    # If the current page has no outgoing links, distribute damping factor evenly
    if len(corpus[page]) == 0:
        for p in corpus:
            distribution[p] += damping_factor / total_pages
    else:
        # Add additional probability for pages linked from the current page
        for link in corpus[page]:
            distribution[link] += damping_factor / len(corpus[page])

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pagerank[current_page] += 1
        distribution = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(distribution.keys()), weights=list(distribution.values()))[0]

    # Normalize pagerank values
    total_samples = sum(pagerank.values())
    return {page: rank / total_samples for page, rank in pagerank.items()}

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    pagerank = {page: 1 / total_pages for page in corpus}

    while True:
        new_pagerank = {}
        max_change = 0

        for page in corpus:
            new_rank = (1 - damping_factor) / total_pages
            for linking_page, links in corpus.items():
                if page in links:
                    new_rank += damping_factor * pagerank[linking_page] / len(links)
                elif not links:
                    new_rank += damping_factor * pagerank[linking_page] / total_pages

            max_change = max(max_change, abs(new_rank - pagerank[page]))
            new_pagerank[page] = new_rank

        pagerank = new_pagerank

        if max_change < 0.001:
            break

    # Normalize pagerank values
    total_rank = sum(pagerank.values())
    return {page: rank / total_rank for page, rank in pagerank.items()}

if __name__ == "__main__":
    main()
