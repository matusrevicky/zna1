import pprint

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from find_factors import find_factors
from lattice import lattice
from naive_concepts import naive_formal_concepts
from rice_siff import rice_siff, fuzzyfy
from utils.base_methods import load_fuzzy


def load_and_change_to_fuzzy(csv_file_name, amount_of_rows=3):
    use_cols = ['course_id', 'price', 'num_subscribers', 'num_reviews', 'num_lectures', 'content_duration']
    data = pd.read_csv(csv_file_name,
                       skiprows=[i for i in range(1, 98)],
                       nrows=amount_of_rows,
                       usecols=use_cols,
                       index_col=0,
                       )
    for i in use_cols:
        if i == 'course_id':
            pass
        else:
            max = data[i].max()
            data[i] = data[i].map(lambda x: fuzify(x, max)).astype('float64')

    data.rename({'price': 'is_price_high', 'num_subscribers': 'is_many_subscribers', 'num_reviews': 'is_many_reviews',
                 'num_lectures': 'is_many_lectures', 'content_duration': 'is_content_long'}, axis=1, inplace=True)
    return data


def fuzify(x, max):
    normalized = x / max
    if 0 <= normalized < 0.375:
        return 0
    # if 0.125 <= normalized < 0.375:
    #     return 0.25
    if 0.375 <= normalized < 0.875:
        return 0.5
    # if 0.625 <= normalized < 0.875:
    #     return 0.75
    if 0.875 <= normalized <= 1:
        return 1


if __name__ == '__main__':
    data = load_and_change_to_fuzzy("data_files/udemy_courses.csv", 100)

    possible_Y_val = [0, 0.5, 1]
    Y = [1 for i in range(len(data.columns))]

    # concepts = naive_formal_concepts(data, possible_Y_val)
    # concepts = find_factors(data, possible_Y_val)
    # concepts = rice_siff(data)

    concepts, lattice = lattice(data, possible_Y_val)
    print(len(concepts))
    # interaktivny graf
    from networkx_viewer import Viewer

    G = nx.Graph(lattice)
    # funguje vo verzii decorator 4.4.2
    nx.draw(G, with_labels=True)
    plt.show()
    #
    pp = pprint.PrettyPrinter(indent=1, sort_dicts=False)
    pp.pprint(concepts)
