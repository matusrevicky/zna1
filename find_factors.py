# Uloha: naprogramovat algoritmus podla clanku: Factorization of matrices with grades str 6, FIND-FACTORS

# Poznamka: kody su pisane tak, aby sa lahko debugovali a boli co najnazornejsie, nie najoptimalnejsie Poznamka2:
# funguje na fuzzy, Algoritmus nenajde vsetky formalne concepty ale factor concepty, hlada sa minimalne pokrytie
# mnoziny...

import copy
import pprint
from utils.base_methods import load_fuzzy, arrowUp, arrowDown, fuzzy_and


def select_attribute_that_maximazes_U(df, D, possible_fuzzy_values, U):
    # postupne sa v D = [0,0,0,0,0] dosadzaju vacsie fuzzy hodnoty
    # napr. D=[0.5,0,0,0,0], D=[0,0.5,0,0,0],..., D=[0,0,0,0,0.5], D=[1,0,0,0,0],..., D=[0,0,0,0,1]
    # stale sa robi uzaver(sipka hore dole) a fuzzy konjunkcia(lukasievicz) a konjunkcia sa porovnava s hodnotami v
    # povodnej tabulke, ale iba na tych poziciach ktore su v U (nepokryte vrcholy)
    # vyberie sa to D, ktore po uzavere pokryje najviac zatial nepokrytych prvkov
    maximum = -1000
    for stuff in range(1, len(possible_fuzzy_values)):
        for idx, element in enumerate(D):
            D_copy = copy.deepcopy(D)
            set_to_maximaze = set()
            index_of_old_value = possible_fuzzy_values.index(D[idx])
            if index_of_old_value + stuff < len(possible_fuzzy_values):
                D_copy[idx] = possible_fuzzy_values[index_of_old_value + stuff]
                D_down = arrowDown(df, D_copy)
                D_down_up = arrowUp(df, D_down)
                # print("D_copy", D_copy)

                for i, j in U:
                    if df.iloc[i][j] <= fuzzy_and(D_down[i], D_down_up[j]):
                        set_to_maximaze.add((i, j))
                if len(set_to_maximaze) > maximum:
                    maximum = len(set_to_maximaze)
                    j_final = idx
                    a = D_copy[idx]

    # pp.pprint(list_of_sets)
    # print(maximum, (j_final, a))
    return maximum, (j_final, a)


# Prejdem cely dataframe a vratim suradnice vsetkych nenulovych bodov
def coordinates_of_non_zero(df):
    set_of_coordinates = set()
    for i, row in enumerate(df.index):
        for j, column in enumerate(df.columns):
            value = df.loc[row][column]
            if value != 0:
                set_of_coordinates.add((i, j))
    return set_of_coordinates


def up_down_D(df, D, bracket_j_a_bracket):
    # napr. ak vstup D = [0,0,0,0,0] (j,a) = (0,0.5),
    # najprv D_copy = [0.5,0,0,0,0]
    D_copy = copy.deepcopy(D)
    D_copy[bracket_j_a_bracket[0]] = bracket_j_a_bracket[1]
    # spravi sa uzaver
    D_down = arrowDown(df, D_copy)
    D_down_up = arrowUp(df, D_down)

    return D_down_up


def find_factors(df, possible_fuzzy_values):
    # pseudokod z clanku
    U = coordinates_of_non_zero(df)
    # F je mnozina fuzzy formalnych konceptov
    F = set()
    while U:
        D = [0 for i in range(len(df.columns))]
        V = 0
        D_and_a_j_size, bracket_j_a_bracket = select_attribute_that_maximazes_U(df, D, possible_fuzzy_values, U)
        while D_and_a_j_size > V:
            V = D_and_a_j_size
            D = up_down_D(df, D, bracket_j_a_bracket)
            D_and_a_j_size, bracket_j_a_bracket = select_attribute_that_maximazes_U(df, D, possible_fuzzy_values, U)

        C = arrowDown(df, D)
        F.add((tuple(C), tuple(D)))
        for i, j in copy.deepcopy(U):
            if df.iloc[i][j] <= fuzzy_and(C[i], D[j]):
                U.remove((i, j))

    return F


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=1, sort_dicts=False)
    data = load_fuzzy("data_files/olympic.csv")
    possible_fuzzy_values = [0, 0.25, 0.5, 0.75, 1]

    concepts = find_factors(data, possible_fuzzy_values)
    pp.pprint(concepts)

    # Priklad z clanku
    # {((0.5, 1.0, 1.0, 0.5, 0.75),
    #   (1.0, 1, 0.75, 0.75, 0.5, 1, 0.5, 0.25, 0.25, 0.5)),
    #  ((0.75, 0.5, 0.75, 1.0, 0.5),
    #   (0.5, 0.5, 0.75, 1, 0.75, 0.5, 0.75, 0.25, 0.5, 1.0)),
    #  ((0.75, 0.5, 1, 0.75, 0.75),
    #   (0.75, 0.75, 0.75, 0.75, 1.0, 0.75, 0.5, 0.25, 0.25, 0.75)),
    #  ((0.75, 0.75, 1, 0.75, 0.25),
    #   (0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 1.0, 0.25, 0.25, 0.75)),
    #  ((1.0, 0.75, 0.25, 0.5, 0.25),
    #   (0.5, 1.0, 1.0, 1.0, 0.75, 1.0, 0.75, 0.75, 1.0, 0.75)),
    #  ((1.0, 0.75, 0.75, 0.5, 1),
    #   (0.5, 0.75, 0.5, 0.5, 0.75, 1.0, 0.25, 0.5, 0.25, 0.75)),
    #  ((1.0, 1, 0.25, 0.5, 0.25),
    #   (0.5, 1.0, 0.75, 0.75, 0.5, 1.0, 0.75, 0.5, 1.0, 0.5))}