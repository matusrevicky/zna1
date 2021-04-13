# Uloha: CDA.pdf algoritmus str 54
# Poznamka: kody su pisane tak, aby sa lahko debugovali a boli co najnazornejsie, nie najoptimalnejsie
# Poznamka2: v skutocnosti funguje len s 0 a 1, nie fuzzy, najde vsetky formalne koncepty
import pprint

from utils.base_methods import arrowDown, arrowUp, load_fuzzy
import numpy as np
import copy


def make_closure_df_attributes(df, atribute_values):
    minimum_for_every_row = arrowDown(df, atribute_values)
    minimum_for_every_column = arrowUp(df, minimum_for_every_row)
    formal_concept_candidate = (tuple(minimum_for_every_row), tuple(minimum_for_every_column))
    return formal_concept_candidate


# def o_intersection(df):
#     #  start ****** zodpoveda riadku C:={(M',M)}
#     C = set()
#     # musim si pripravit pole samych jednotiek o velkosti poctu atributov
#     # napr. predmety v ktorych su vsetci dobry
#     only_ones = [1 for i in range(len(df.columns))]
#     # fuzzy uzaver
#     formal_concept_candidate = make_closure_df_attributes(df, only_ones)
#     C.add(formal_concept_candidate)
#     #  end ****** zodpoveda riadku C:={(M',M)}
#
#     #  start ****** zodpoveda riadku for each g in G
#     for i, row in enumerate(df.index):
#         g = df.loc[row].values
#         for (X,Y) in copy.deepcopy(C):
#             # arrowDown_g = arrowUp(df, arrowDown(df, g))
#             Inters = np.minimum(Y, g)
#             formal_concept_C = make_closure_df_attributes(df, Inters)
#             C.add(formal_concept_C)
#     return C

def object_intersection(df):
    #  start ****** zodpoveda riadku C:={(M',M)}
    C = []
    # musim si pripravit pole samych jednotiek o velkosti poctu atributov
    # napr. predmety v ktorych su vsetci dobry
    only_ones = [1 for i in range(len(df.columns))]
    # fuzzy uzaver
    formal_concept_candidate = make_closure_df_attributes(df, only_ones)
    C.append(formal_concept_candidate)
    #  end ****** zodpoveda riadku C:={(M',M)}

    #  start ****** zodpoveda riadku for each g in G
    for i, row in enumerate(df.index):
        g = df.loc[row].values
        idx = 0
        while True:
            # arrowDown_g = arrowUp(df, arrowDown(df, g))
            if idx >= len(C):
                break
            Inters = np.minimum(C[idx][1], g)
            formal_concept_C = make_closure_df_attributes(df, Inters)
            if formal_concept_C not in C:
                C.append(formal_concept_C)
            idx = idx + 1

    return C


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=1, sort_dicts=False)
    data = load_fuzzy("data_files/intersection.csv")
    result = object_intersection(data)
    pp.pprint(object_intersection(data))

    # for (X, Y) in result:
    #     for idx, i in enumerate(X):
    #         if i == 1:
    #             print(idx + 1, end='')
    #     print(" ", Y)
    #
    # print(set(result))
    #
    # print(arrowDown(data,[1, 0, 0, 0, 1, 0, 1, 0, 0]))
