# najde vsetky formalne concepty, zlozitost 2^n, iba preskumanie vsetkych moznosti a sipka hore, dole
# funguje s fuzzy

import pprint
from itertools import product

from utils.base_methods import arrowDown, arrowUp, load_fuzzy


def all_repeat(array, rno):
    return list(product(array, repeat=rno))


def for_given_combinations_do_fuzzy_implication(df, possible_values):
    formal_concepts = []
    for possible_attribute_values in possible_values:
        # print("*************************************************************************")
        minimum_for_every_row = arrowDown(df, possible_attribute_values)
        # print('minimum_for_every_row_after_fuzzy_implication', minimum_for_every_row)
        minimum_for_every_column = arrowUp(df, minimum_for_every_row)
        # print('minimum_for_every_column_after_fuzzy_implication', minimum_for_every_column, possible_attribute_values)
        formal_concepts.append((tuple(minimum_for_every_row), tuple(minimum_for_every_column)))

    return set(formal_concepts)


def naive_formal_concepts(df, possible_Y_values):
    possible_values = all_repeat(possible_Y_values, len(df.columns))
    formal_concepts = for_given_combinations_do_fuzzy_implication(df, possible_values)
    return formal_concepts


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=1, sort_dicts=False)
    data = load_fuzzy("data_files/data_from_article.csv")
    # naivne riesenie
    possible_Y_values = [0.0, 0.5, 1.0]
    formal_concepts = naive_formal_concepts(data, possible_Y_values)

    pp.pprint(formal_concepts)

    #  Pre vsetky moznosti sa spravi fuzzy implikacia
    # {((0.5, 0.5, 0.0), (1, 1.0, 1.0, 1, 1)),
    #  ((0.5, 0.5, 0.5), (0.5, 0.5, 1.0, 1, 1)),
    #  ((0.5, 1, 0.0), (1, 1.0, 1.0, 1, 0.5)),
    #  ((0.5, 1, 0.5), (0.5, 0.5, 1.0, 1, 0.5)),
    #  ((1.0, 0.5, 0.0), (1.0, 0.5, 0.5, 1.0, 1.0)),
    #  ((1, 0.5, 0.5), (0.5, 0.5, 0.5, 1.0, 1.0)),
    #  ((1, 0.5, 1.0), (0.0, 0.0, 0.5, 0.5, 1.0)),
    #  ((1.0, 1.0, 0.0), (1.0, 0.5, 0.5, 1.0, 0.5)),
    #  ((1, 1, 0.5), (0.5, 0.5, 0.5, 1.0, 0.5)),
    #  ((1, 1, 1.0), (0.0, 0.0, 0.5, 0.5, 0.5))}
