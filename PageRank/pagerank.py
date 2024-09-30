import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    # corpus = crawl(sys.argv[1])
    corpus = {'1': {'2'}, '2': {'1', '3'}, '3': {'2', '4'}, '4': {'2'}}
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
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilities = dict()

    if len(corpus[page]) == 0:
        for key in corpus:
            probabilities[key] = 1 / len(corpus)
        return probabilities
    else:
        corpus_length = len(corpus[page])

        damping_probability = damping_factor / corpus_length
        random_probability = (1 - damping_factor) / (corpus_length)

        for key in corpus:
            probabilities[key] = random_probability

    for key, values in corpus.items():
        if key == page:
            for value in values:
                probabilities[value] += damping_probability

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    estimated_page_rank = dict()

    keys = list(corpus.keys())
    next_page = random.choice(keys)

    for key in keys:
        if key == next_page:
            estimated_page_rank[key] = 0.0001
        else:
            estimated_page_rank[key] = 0

    for i in range(n - 1):
        probabilities = transition_model(corpus, next_page, damping_factor)
        keys = list(probabilities.keys())
        weights = list(probabilities.values())
        next_page = random.choices(keys, weights=weights, k=1)[0]
        estimated_page_rank[next_page] += 0.0001
    
    return estimated_page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    estimated_page_rank = dict()

    keys = list(corpus.keys())
    for key in keys:
        estimated_page_rank[key] = 1 / len(keys)


    # if the corpus contains a page with no links, adds all pages as links
    for key, value in corpus.items():
        if not value:
            for page in keys:
                corpus[key].add(page)

    # loops through till returned
    while True:
        convergence = True
        # loops through the pages in the corpus
        for key1 in corpus:
            total = 0
            # loops again through the corpus
            for key2, value2 in corpus.items():
                # if the current page from first loop is linked to by the page in the second loop
                if key1 in value2:
                    # adds the pages probability divided by the amount of link on the page
                    total += estimated_page_rank[key2] / len(value2)
            #   times the sum of all pages that link to current page probabilities by the damping factor
            total *= damping_factor
            # adds random page factor
            total += (1 - damping_factor) / len(keys)
            # if the change is above the threshold convergence has not been reached
            if abs(estimated_page_rank[key1] - total) > 0.001:
                convergence = False
            
            estimated_page_rank[key1] = total

        # if convergence is reached break the infinite loop
        if convergence:
            break

    return estimated_page_rank


if __name__ == "__main__":

    main()
