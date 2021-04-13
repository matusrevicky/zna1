# Uloha: CDA.pdf algoritmus str 56, NextNeighbours
# Poznamka: kody su pisane tak, aby sa lahko debugovali a boli co najnazornejsie, nie najoptimalnejsie
# Poznamka2: v skutocnosti funguje len s 0 a 1, nie fuzzy

import pprint
import copy
import networkx as nx
import matplotlib.pyplot as plt

from utils.base_methods import arrowDown, arrowUp, load_fuzzy

# ak by bolo fuzzy treba upravit, teraz iba menim nuly na jednotky
def replace_one_zero_in_y(df, Y, y):
    Y_copy = []
    for element in Y:
        Y_copy.append(element)
    index_of_old_value = y[0]
    Y_copy[index_of_old_value] = 1
    return Y_copy


def nextNeighbours(df):
    # C:= {(G,G')}
    C = set()
    only_ones_rows = [1 for i in range(len(df.index))]
    arrow_up_result = arrowUp(df, only_ones_rows)
    candidate = (tuple(only_ones_rows), tuple(arrow_up_result))
    C.add(candidate)
    # E:= empty set
    E = set()
    # currentLevel := {(G,G')}
    currentLevel = copy.deepcopy(C)
    # while
    while bool(currentLevel):
        nextLevel = set()
        for (X, Y) in currentLevel:
            lowerNeighbours = findLowerNeighbours(df, (X, Y))
            for (X1, Y1) in lowerNeighbours:
                if (X1, Y1) not in C:
                    C.add((X1, Y1))
                    nextLevel.add((X1, Y1))
                E.add(((X1, Y1), (X, Y)))
        currentLevel = copy.deepcopy(nextLevel)
        # currentLevel = currentLevel- set(candidate)
    return C, E


def findLowerNeighbours(df, concept_candidate):
    candidates = set()
    elements_equal_to_zero = []
    for idx, attribute_value in enumerate(concept_candidate[1]):
        if attribute_value == 0:
            elements_equal_to_zero.append((idx, attribute_value))

    for y in elements_equal_to_zero:
        replaced = replace_one_zero_in_y(df, concept_candidate[1], y)
        minimum_for_every_row = arrowDown(df, replaced)
        minimum_for_every_column = arrowUp(df, minimum_for_every_row)
        arrowUpDown = (tuple(minimum_for_every_row), tuple(minimum_for_every_column))
        if arrowUpDown not in candidates:
            candidates.add(arrowUpDown)

    final_candidates = maximally_general_candidates(candidates)
    return final_candidates


# funguje len s 0 a 1, nie fuzzy, nadmnozina pohlti podmnoziny... napr [0,1,1,0] pohlti [0,1,0,0]
def maximally_general_candidates(candidates):
    final_candidates = copy.deepcopy(candidates)
    for i in candidates:
        for j in candidates:
            i_idxs = set()
            j_idxs = set()
            idx = 0
            is_remove = True
            for x, y in zip(i[0], j[0]):
                if i[0] == j[0]:
                    is_remove = False
                    continue
                if x == 1:
                    i_idxs.add(idx)
                if y == 1:
                    j_idxs.add(idx)
                idx = idx + 1

            # print("iids",i_idxs)
            # print("jids",j_idxs)
            # print("i",i)
            # print("j",j)
            # print(len(final_candidates))
            # print("****************")

            if i_idxs.issubset(j_idxs) and is_remove:
                final_candidates.discard(i)
    # print("end of one iteration*************************************")
    return final_candidates


def tuple_to_string(node):
    title = ''
    for idx, i in enumerate(node):
        if i == 1:
            title = title + str(idx + 1)
    return title


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=1, sort_dicts=False)
    data = load_fuzzy("data_files/intersection.csv")

    vertices, edges = nextNeighbours(data)
    print("nodes")
    pp.pprint(vertices)
    print("edges")
    pp.pprint(edges)
    # print(len(edges))

    # Odtial nadol je uz len vykreslenie grafu tak ako je v clanku na str. 14
    nodes_list = []
    for node in vertices:
        string = tuple_to_string(node[0])
        nodes_list.append(string)
        # nodes_list.append(node[0])

    edges_list = []
    for node in edges:
        edges_list.append((tuple_to_string(node[0][0]), tuple_to_string(node[1][0])))
        # edges_list.append((node[0][0],node[1][0]))

    # interaktivny graf
    from networkx_viewer import Viewer
    G = nx.Graph()
    G.add_nodes_from(nodes_list)
    G.add_edges_from(edges_list)
    # nx.draw(G, with_labels=True)
    # plt.show()
    app = Viewer(G)
    app.mainloop()

    # nodes
    # {((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
    #  ((0, 0, 0, 0, 0, 0, 1), (1, 0, 0, 0, 1, 0, 1, 0, 1)),
    #  ((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0)),
    #  ((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0)),
    #  ((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0)),
    #  ((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0)),
    #  ((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0)),
    #  ((0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 1, 0, 0, 1, 0)),
    #  ((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0)),
    #  ((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0)),
    #  ((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0)),
    #  ((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0)),
    #  ((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0)),
    #  ((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0)),
    #  ((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0)),
    #  ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0))}
    # edges
    # {(((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
    #   ((0, 0, 0, 0, 0, 0, 1), (1, 0, 0, 0, 1, 0, 1, 0, 1))),
    #  (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
    #   ((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0))),
    #  (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
    #   ((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0))),
    #  (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
    #   ((0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 1, 0, 0, 1, 0))),
    #  (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
    #   ((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0))),
    #  (((0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1, 1, 1)),
    #   ((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0))),
    #  (((0, 0, 0, 0, 0, 0, 1), (1, 0, 0, 0, 1, 0, 1, 0, 1)),
    #   ((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0))),
    #  (((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0)),
    #   ((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0))),
    #  (((0, 0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 1, 0, 0)),
    #   ((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0))),
    #  (((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0)),
    #   ((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0))),
    #  (((0, 0, 0, 1, 0, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0, 0)),
    #   ((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0))),
    #  (((0, 0, 0, 1, 0, 1, 1), (1, 0, 0, 0, 1, 0, 1, 0, 0)),
    #   ((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0))),
    #  (((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0)),
    #   ((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0))),
    #  (((0, 0, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0)),
    #   ((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0))),
    #  (((0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 1, 0, 0)),
    #   ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0))),
    #  (((0, 0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 1, 0, 0, 1, 0)),
    #   ((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0))),
    #  (((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0)),
    #   ((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0))),
    #  (((0, 1, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1, 0, 0, 0)),
    #   ((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0))),
    #  (((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0)),
    #   ((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0))),
    #  (((0, 1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 1, 1, 0, 0, 0)),
    #   ((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0))),
    #  (((0, 1, 0, 1, 1, 0, 0), (0, 0, 1, 0, 1, 0, 0, 0, 0)),
    #   ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0))),
    #  (((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0)),
    #   ((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0))),
    #  (((1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 1, 0)),
    #   ((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0))),
    #  (((1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 1, 0)),
    #   ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0))),
    #  (((1, 1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 1, 1, 0, 0, 0)),
    #   ((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0))),
    #  (((1, 1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 1, 0, 0, 0)),
    #   ((1, 1, 1, 1, 1, 1, 1), (0, 0, 0, 0, 1, 0, 0, 0, 0)))}
