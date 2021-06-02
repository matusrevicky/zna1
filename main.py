import pprint
import time

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from find_factors import find_factors
from lattice import lattice
from naive_concepts import naive_formal_concepts
from rice_siff import rice_siff, fuzzyfy
from utils.base_methods import load_fuzzy, arrowDown, fuzzy_and, arrowUp


def load_and_change_to_fuzzy(csv_file_name, amount_of_rows=3):
    use_cols = ['course_id', 'price', 'num_subscribers', 'num_reviews', 'num_lectures', 'level', 'content_duration']
    data = pd.read_csv(csv_file_name,
                       # skiprows=[i for i in range(1, 98)],
                       nrows=amount_of_rows,
                       usecols=use_cols,
                       index_col=0,
                       )

    for i in use_cols:
        if i == 'course_id':
            pass
        elif i == 'level':
            data[i] = data[i].map(lambda x: fuzify_level(x)).astype('float64')
        else:
            max = data[i].max()
            data[i] = data[i].map(lambda x: fuzify(x, max)).astype('float64')
            # data[i] = pd.qcut(data[i], q=3, labels=[0, 0.5, 1]).astype('float64')

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


def fuzify_level(x):
    if x == 'Beginner Level':
        return 0
    elif x == 'Intermediate Level':
        return 0.5
    elif x == 'Expert Level':
        return 1


def two_matrix_union(A, B):
    # A_num = np.array(A)
    # B_num = np.array(B)
    final = np.maximum(A, B)
    return final


def factors_on_my_dataset_nice_print(data, possible_Y_val, csv_file_name, rows):
    start = time.time()
    use_cols = ['course_title']
    data_names = pd.read_csv(csv_file_name,
                             # skiprows=[i for i in range(1, 98)],
                             nrows=rows,
                             usecols=use_cols,
                             )

    concepts = find_factors(data, possible_Y_val)
    print('Total amount of concepts using find factors:', len(concepts))
    for concept in concepts:
        for i, con in enumerate(concept[1]):
            print(data.columns[i] + ':', con, end=', ')
        print()

    for concept in concepts:
        for i, con in enumerate(concept[1]):
            print(data.columns[i] + ':', con, end=', ')
        print()

        print('amount of rows', np.count_nonzero(concept[0]))
        for i, con in enumerate(concept[0]):
            if con != 0:
                val = data_names.iloc[[i]]
                print(val.to_string(header=False), con)
        print()

    end = time.time()
    print('factor creation duration:', end - start)


def lattice_on_my_dataset_nice_print(data, possible_Y_val, csv_file_name, rows):
    start = time.time()
    use_cols = ['course_title']
    data_names = pd.read_csv(csv_file_name,
                             # skiprows=[i for i in range(1, 98)],
                             nrows=rows,
                             usecols=use_cols,
                             )
    concepts, lattice_to_draw = lattice(data, possible_Y_val)

    f = open("results/lattice_result_fuzzyfied.txt", "a", encoding='UTF-8')

    full_concepts = set()
    for con in concepts:
        full_concepts.add((tuple(arrowDown(data, con)), con))

    f.write('Total amount of concepts using find factors:' + str(len(concepts)) + '\n')
    for concept in full_concepts:
        for i, con in enumerate(concept[1]):
            f.write(data.columns[i] + ': ' + str(con))
        f.write('\n')

        f.write('amount of rows ' + str(np.count_nonzero(concept[0]))+ '\n')
        for i, con in enumerate(concept[0]):
            if con != 0:
                val = data_names.iloc[[i]]
                f.write(val.to_string(header=False) + str(con) + '\n')
        f.write('\n')

    end = time.time()
    f.write('lattice duration: ' + str(end - start))

    f.close()

    G = nx.Graph(lattice_to_draw)
    # funguje vo verzii decorator 4.4.2
    nx.draw(G, with_labels=True)
    plt.show()


if __name__ == '__main__':
    csv_name = "data_files/udemy_courses_enhanced.csv"
    rows = 1750
    data = load_and_change_to_fuzzy(csv_name, rows)
    possible_Y_val = [0, 0.5, 1]
    Y = [1 for i in range(len(data.columns))]

    # uncomment to run cca. 431.7125794887543 seconds
    factors_on_my_dataset_nice_print(data, possible_Y_val, csv_name, rows)

    # uncomment to run cca. 7000 seconds
    # lattice_on_my_dataset_nice_print(data, possible_Y_val, csv_name, rows)


